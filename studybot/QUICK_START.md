# 🚀 Quick Start - Defense Ready

**Get project running in 2 minutes before your exam defense.**

## Prerequisites
- Python 3.8+ installed
- Telegram Bot Token (from @BotFather)
- Internet connection for APIs

## ⚡ Express Setup

### Step 1: Install Dependencies (30 sec)
```bash
cd c:\Users\acer\studybot
pip install -r requirements.txt
```

### Step 2: Configure .env (30 sec)
```bash
copy .env.example .env
```

Edit `.env` and add:
```env
TELEGRAM_TOKEN=your_token_here
OPENWEATHER_API_KEY=your_api_key_here
```

**Get keys:**
- Bot token: Write @BotFather in Telegram → `/newbot`
- OpenWeather: https://openweathermap.org/api → Sign up → Copy key

### Step 3: Setup Database (30 sec)
```bash
python manage.py migrate
```

**That's it! Ready to run.**

---

## 🎬 Run for Defense

### Terminal 1: Start Bot
```bash
python manage.py runbot
```

Expected output:
```
Starting bot...
[INFO] Loaded handlers
Bot is polling...
```

### Terminal 2: Start Web Interface
```bash
python manage.py runserver
```

Expected output:
```
Starting development server at http://127.0.0.1:8000/
```

---

## ✅ Verify Everything Works

1. **Send `/start` to bot in Telegram**
   - Should see welcome message with menu buttons
   
2. **Open admin**: http://127.0.0.1:8000/admin/
   - Should see login page (use superuser credentials if created)
   
3. **Test one command**: Send `/weather Almaty` to bot
   - Should get real weather data

If all 3 work → **You're ready! 🎯**

---

## 📖 Documentation

For detailed information, see:

- **[README.md](README.md)** - Full project overview
- **[EXAM_REQUIREMENTS.md](EXAM_REQUIREMENTS.md)** - Proof of compliance (100/100)
- **[DEFENSE_GUIDE.md](DEFENSE_GUIDE.md)** - Live demo steps
- **[SUBMISSION_CHECKLIST.md](SUBMISSION_CHECKLIST.md)** - Complete checklist

---

## 🐛 Common Issues

| Problem | Fix |
|---------|-----|
| Bot not starting | Check `TELEGRAM_TOKEN` in .env |
| Admin page 404 | Run `python manage.py runserver` in another terminal |
| Weather/Country no data | Verify API keys in .env and internet connection |
| Port 8000 in use | Use `python manage.py runserver 8080` |
| Database error | Run `python manage.py migrate` |

---

## 🎯 Demo Sequence (3 min)

1. Show `/start` → Main menu
2. Click "Lessons" → Show lesson navigation
3. Click "Progress" → Show progress bar
4. Send `/weather Almaty` → Real API data
5. Click "Admin" link in chat → Show admin panel
6. Open http://127.0.0.1:8000/history → Show query history

**Done! Exam ready. 🚀**

---

## 📞 Need Help?

**Before exam**:
- Check DEFENSE_GUIDE.md for troubleshooting
- Verify all commands work with test data
- Practice the demo 2-3 times

**During exam**:
- If bot freezes, restart: `Ctrl+C` then rerun
- If API slow, mention caching optimizes 2nd request
- Be ready to show code if asked

---

**Status**: ✅ **EXAM READY**

Good luck! 🎓
