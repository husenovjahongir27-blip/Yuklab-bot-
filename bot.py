import logging
import os
import re
import tempfile

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
import yt_dlp

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Telegram bot API orqali fayl yuborishning standart chegarasi ~50MB
MAX_FILE_SIZE = 50 * 1024 * 1024

FACEBOOK_URL_PATTERN = re.compile(
    r"(https?://(?:www\.|web\.|m\.)?(?:facebook\.com|fb\.watch)/\S+)"
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Salom! Menga Facebook video havolasini yuboring, men uni siz uchun "
        "yuklab beraman.\n\n"
        "Eslatma: fayl hajmi 50MB dan katta bo'lsa, Telegram bot API orqali "
        "yuborib bo'lmaydi."
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text or ""
    match = FACEBOOK_URL_PATTERN.search(text)

    if not match:
        await update.message.reply_text(
            "Iltimos, to'g'ri Facebook video havolasini yuboring "
            "(masalan: https://www.facebook.com/.../videos/...)."
        )
        return

    url = match.group(1)
    status_message = await update.message.reply_text("Video yuklanmoqda, kuting...")

    with tempfile.TemporaryDirectory() as tmp_dir:
        output_template = os.path.join(tmp_dir, "%(id)s.%(ext)s")

        ydl_opts = {
            "outtmpl": output_template,
            "format": "mp4/best",
            "quiet": True,
            "no_warnings": True,
            "noplaylist": True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                file_path = ydl.prepare_filename(info)
        except Exception as exc:
            logger.exception("yt-dlp xatosi: %s", exc)
            await status_message.edit_text(
                "Videoni yuklab bo'lmadi. Havola noto'g'ri, video ochiq "
                "(public) emas, yoki Facebook formatini o'zgartirgan bo'lishi "
                "mumkin."
            )
            return

        if not os.path.exists(file_path):
            await status_message.edit_text("Video fayli topilmadi. Qayta urinib ko'ring.")
            return

        file_size = os.path.getsize(file_path)

        if file_size > MAX_FILE_SIZE:
            await status_message.edit_text(
                "Video hajmi 50MB dan katta, Telegram orqali yuborib bo'lmaydi."
            )
            return

        await status_message.edit_text("Video topildi, yuborilmoqda...")

        try:
            with open(file_path, "rb") as video_file:
                await update.message.reply_video(video=video_file)
            await status_message.delete()
        except Exception as exc:
            logger.exception("Yuborishda xato: %s", exc)
            await status_message.edit_text("Videoni yuborishda xatolik yuz berdi.")


def main() -> None:
    if not BOT_TOKEN:
        raise RuntimeError(
            "BOT_TOKEN muhit o'zgaruvchisi (environment variable) topilmadi."
        )

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Bot ishga tushdi...")
    application.run_polling()


if __name__ == "__main__":
    main()
