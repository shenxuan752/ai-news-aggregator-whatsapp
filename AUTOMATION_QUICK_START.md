# WhatsApp Automation - Quick Start

## 🚀 3-Step Setup (15 minutes)

### Step 1: Get Twilio Account (5 min)
1. Sign up: https://www.twilio.com/try-twilio
2. Go to: Messaging → Try WhatsApp
3. Send "join <code>" to their WhatsApp number
4. Get your credentials from console

### Step 2: Configure (2 min)
Add to `.env`:
```bash
TWILIO_ACCOUNT_SID=ACxxxxx...
TWILIO_AUTH_TOKEN=xxxxx...
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
TWILIO_WHATSAPP_TO=whatsapp:+1YOUR_PHONE
```

### Step 3: Test & Automate (8 min)
```bash
# Install Twilio
pip install twilio

# Test it
python3 daily_digest.py

# Add to cron (runs at 8 AM daily)
crontab -e
```

Add this line:
```bash
0 8 * * * cd /FULL/PATH/TO/PROJECT && ./venv/bin/python3 daily_digest.py >> logs/digest.log 2>&1
```

## ✅ Done!

You'll now receive:
- 📱 Daily WhatsApp digest at 8 AM
- 📰 Top 5 articles with summaries
- ⭐ Highest relevance news only
- 🔗 Direct links to full articles

## 💰 Cost
- Free trial: $15.50 credit (~3,000 messages)
- After: ~$0.01/day = $3.60/year

## 📖 Full Guide
See `WHATSAPP_AUTOMATION_SETUP.md` for complete instructions
