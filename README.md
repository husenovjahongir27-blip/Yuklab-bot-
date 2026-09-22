# Facebook Video Yuklovchi Telegram Bot

Foydalanuvchi Facebook video havolasini yuborsa, bot videoni yuklab olib,
Telegram orqali qaytarib beradi.

## 1. Telegram bot yaratish

1. Telegram'da **@BotFather** ga yozing.
2. `/newbot` buyrug'ini yuboring, nom va username tanlang.
3. BotFather sizga **token** beradi (masalan `123456:ABC-DEF...`) — uni saqlab qo'ying.

## 2. Kodni Render.com'ga joylash (bepul)

Render'da bepul tarif faqat **Web Service** turini qo'llab-quvvatlaydi (alohida
"Background Worker" bepul emas). Shuning uchun `bot.py` ichiga kichik health-check
server qo'shilgan — bu Render talab qiladigan portni tinglaydi, botning o'ziga
ta'sir qilmaydi.

1. https://render.com saytiga GitHub hisobingiz bilan kiring.
2. **New → Web Service** ni tanlang va reponi ulang.
3. Sozlamalar:
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python bot.py`
   - **Instance Type**: Free
4. **Environment** bo'limiga o'ting va qo'shing:
   - `BOT_TOKEN` = BotFather'dan olgan tokeningiz
5. **Create Web Service** tugmasini bosing — Render avtomatik deploy qiladi.

### Muhim: botni "uxlab qolishdan" saqlash

Render'ning bepul tarifi 15 daqiqa faoliyatsizlikdan keyin xizmatni "uxlatib
qo'yadi" — shu payt bot Telegram xabarlariga javob bermay qoladi. Buning oldini
olish uchun bepul **UptimeRobot** (https://uptimerobot.com) xizmatidan
foydalaning:

1. UptimeRobot'da ro'yxatdan o'ting.
2. Yangi **HTTP(s) monitor** yarating.
3. URL sifatida Render bergan manzilni kiriting (masalan
   `https://sizning-bot.onrender.com`).
4. Tekshirish oralig'ini **5-10 daqiqa**ga qo'ying.

Shunda UptimeRobot har necha daqiqada botni "uyg'otib" turadi va u doimo
ishlab turadi.

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
