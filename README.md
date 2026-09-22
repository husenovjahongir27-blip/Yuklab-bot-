# Facebook Video Yuklovchi Telegram Bot

Foydalanuvchi Facebook video havolasini yuborsa, bot videoni yuklab olib,
Telegram orqali qaytarib beradi.

## 1. Telegram bot yaratish

1. Telegram'da **@BotFather** ga yozing.
2. `/newbot` buyrug'ini yuboring, nom va username tanlang.
3. BotFather sizga **token** beradi (masalan `123456:ABC-DEF...`) — uni saqlab qo'ying.

## 2. Kodni Railway.app'ga joylash (tavsiya etiladi, bepul)

1. https://railway.app saytiga GitHub hisobingiz bilan kiring.
2. Ushbu papkadagi fayllarni (`bot.py`, `requirements.txt`, `Procfile`) o'zingizning
   yangi GitHub repositoryingizga yuklang.
3. Railway'da **New Project → Deploy from GitHub repo** ni tanlang va shu
   repositoryni ulang.
4. Railway loyihasida **Variables** bo'limiga o'ting va quyidagini qo'shing:
   - `BOT_TOKEN` = BotFather'dan olgan tokeningiz
5. Railway avtomatik ravishda `requirements.txt`ni o'rnatadi va `Procfile`
   asosida botni ishga tushiradi.

## 3. Kompyuteringizda sinab ko'rish (ixtiyoriy)

```bash
pip install -r requirements.txt
export BOT_TOKEN="sizning_tokeningiz"   # Windows: set BOT_TOKEN=...
python bot.py
```

## Muhim eslatmalar

- **Fayl hajmi cheklovi**: Telegram bot API orqali 50MB dan katta faylni
  yuborib bo'lmaydi. Katta videolar uchun local Bot API server kerak bo'ladi
  (murakkabroq sozlash talab qiladi).
- **Facebook o'zgarishlari**: Facebook video sahifalarining tuzilishini
  vaqti-vaqti bilan o'zgartiradi. Agar bot ishlamay qolsa, birinchi navbatda
  `yt-dlp`ni yangilang:
  ```bash
  pip install -U yt-dlp
  ```
- Bot faqat **ochiq (public)** videolarni yuklay oladi — maxfiy (faqat
  do'stlar uchun) videolarni yuklab bo'lmaydi.
- Facebook'ning foydalanish shartlariga (Terms of Service) rioya qiling —
  botni faqat shaxsiy/ta'lim maqsadida ishlatish tavsiya etiladi.
