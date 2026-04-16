# Anime Bot (Telegram)

Bu loyiha Python asosida yozilgan Telegram bot. Unda oddiy kodli video va serial (fon + qismlar) oqimi bor.

## Nimalar tayyor

- `python-telegram-bot` bilan bot skeleton
- `.env` orqali token konfiguratsiyasi
- `/start` komandasi handleri
- `/add <kod>` orqali videoga kod biriktirish
- `/get <kod>` yoki kod yuborish orqali videoni chiqarish
- `/fon <nom> <kod>` bilan serial fon rasmini biriktirish
- `/serial <kod> <qism>` bilan serial qismlarini biriktirish
- Soddalashtirilgan `src` struktura

## Arxitektura oqimi

- `src/app.py` -> bot ishga tushadi
- `src/loader.py` -> sozlamalar va handlerlar ulanadi
- `src/bot/handlers/` -> user bilan ishlaydi
- `src/bot/keyboards/` -> tugmalar
- `src/bot/states/` -> holatlar (bot_data kalitlari va subscription statuslar)

## O'rnatish

1. Virtual muhit yarating va yoqing:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Kutubxonalarni o'rnating:

```powershell
pip install -r requirements.txt
```

3. Konfiguratsiya varianti:

```powershell
copy .env.example .env
```

Bot avval `.env` ni o'qiydi. Agar u bo'lmasa `.env.example` dan ham ishlaydi.
Amaliyotda `.env` tavsiya etiladi, `.env.example` esa namuna sifatida repoda qoladi.

4. Tanlagan faylingiz ichiga token qo'ying (`.env` yoki `.env.example`):

```env
BOT_TOKEN=your_real_bot_token
ADMIN_ID=123456789
CHANNEL_URL=https://t.me/your_channel
```

`ADMIN_ID` ixtiyoriy, lekin tavsiya etiladi. Shu orqali bot sizni xo'jayin sifatida taniydi.
`CHANNEL_URL` bo'lsa, oddiy foydalanuvchiga `/start` da kanal tugmasi chiqadi.

## Ishga tushirish

```powershell
python -m src.main
```

Yangi kirish fayli ham mavjud:

```powershell
python -m src.app
```

## Render ga ulash

Bu bot polling rejimida ishlaydi, shuning uchun Render’da `worker` sifatida deploy qiling.

Kerakli env lar:

- `BOT_TOKEN`
- `ADMIN_ID`
- `CHANNEL_ID`
- `CHANNEL_URL`

Render sozlamalari:

- Build Command: `pip install -r requirements.txt`
- Start Command: `python -m src.app`
- Type: `worker`

Repo ichida tayyor fayllar bor:

- [Procfile](Procfile)
- [render.yaml](render.yaml)

## Kodga video biriktirish

1. Botga video yuboring.
2. O'sha videoga reply qilib buyruq yuboring:

```text
/add 100
```

3. Keyin video olish uchun:

```text
/get 100
```

Yoki shunchaki `100` deb yozsangiz ham bot videoni qaytaradi.

## Serial oqimi

1. Serial fonini saqlash:

```text
(rasmga reply qilib) /fon farsaj 112
```

2. Qismlarni qo'shish:

```text
(videoga reply qilib) /serial 112 1
(videoga reply qilib) /serial 112 2
```

3. Foydalanuvchi `112` yuborsa:
- fon rasmi chiqadi
- nechta qism borligi ko'rsatiladi
- tugmalar orqali qism tanlab videoni oladi

## Keyingi qadamlar

- Anime qidiruv API integratsiyasi
- Inline tugmalar va callback handlerlar
- `help`, `anime`, `top` komandalar
