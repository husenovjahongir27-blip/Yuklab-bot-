import logging
import os
import re
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

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

GENERIC_URL_PATTERN = re.compile(r"(https?://\S+)")

# Foydalanuvchiga qanday saytlarni qo'llab-quvvatlashini ko'rsatish uchun
SUPPORTED_SITES_TEXT = (
    "Facebook, Instagram, TikTok, YouTube, Twitter/X, Pinterest, Reddit va "
    "yana ko'plab boshqa ijtimoiy tarmoqlar"
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Salom! Menga video havolasini yuboring, men uni siz uchun yuklab "
        f"beraman.\n\nQo'llab-quvvatlanadigan tarmoqlar: {SUPPORTED_SITES_TEXT}.\n\n"
        "Eslatma: fayl hajmi 50MB dan katta bo'lsa, Telegram bot API orqali "
        "yuborib bo'lmaydi."
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text or ""
    match = GENERIC_URL_PATTERN.search(text)

    if not match:
        await update.message.reply_text(
            "Iltimos, video havolasini yuboring (masalan Facebook, Instagram, "
            "TikTok, YouTube va h.k.)."
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

        # Ba'zi saytlar (YouTube, Instagram) ayrim videolar uchun login
        # (cookies) talab qiladi. COOKIES_FILE muhit o'zgaruvchisi orqali
        # cookies.txt faylini ko'rsatishingiz mumkin.
        cookies_file = os.environ.get("COOKIES_FILE")
        if cookies_file and os.path.exists(cookies_file):
            ydl_opts["cookiefile"] = cookies_file

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                file_path = ydl.prepare_filename(info)
        except Exception as exc:
            logger.exception("yt-dlp xatosi: %s", exc)
            await status_message.edit_text(
                "Videoni yuklab bo'lmadi. Havola noto'g'ri, video ochiq "
                "(public) emas, yoki bu sayt hali qo'llab-quvvatlanmasligi "
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


class _HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

    def log_message(self, format, *args):  # noqa: A002 - suppress default logging
        pass


def _run_health_server() -> None:
    # Render "Web Service" turi portni tinglashni talab qiladi.
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), _HealthCheckHandler)
    server.serve_forever()


def main() -> None:
    if not BOT_TOKEN:
        raise RuntimeError(
            "BOT_TOKEN muhit o'zgaruvchisi (environment variable) topilmadi."
        )

    threading.Thread(target=_run_health_server, daemon=True).start()

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Bot ishga tushdi...")
    application.run_polling()


if __name__ == "__main__":
    main()
