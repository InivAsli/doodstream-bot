# doodstream-bot
Telegram bot for doodstream
# 🤖 DoodStream Telegram Bot

Bot Telegram untuk mengelola akun DoodStream.

## Features
- 📁 List semua video
- 📤 Upload via URL
- 📊 Lihat statistik akun
- 🔗 Dapatkan link download

## Deployment di Render.com

### 1. Setup Environment Variables:
Di Render dashboard, tambah 3 variables. 

### 2. Deploy:
1. Connect GitHub repository ke Render
2. New Web Service
3. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python main.py`
4. Deploy

## Security
- ✅ Credentials aman di Environment Variables
- ✅ Tidak ada token di source code
- ✅ GitHub repository bersih

## License
MIT
