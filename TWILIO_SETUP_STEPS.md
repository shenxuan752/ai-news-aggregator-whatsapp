# Twilio WhatsApp Setup - Step by Step

## 📱 Step 1: Create Twilio Account

1. **Go to Twilio:** https://www.twilio.com/try-twilio
2. **Sign up** with your email
3. **Verify your email** address
4. **Verify your phone number** (important for WhatsApp)

**You'll get $15.50 in free credits!**

---

## 📲 Step 2: Set Up WhatsApp Sandbox

### 2.1 Access WhatsApp Sandbox

1. In Twilio Console, click **Explore Products** (left sidebar)
2. Select **Messaging**
3. Click **Try it out** → **Send a WhatsApp message**
4. You'll see the WhatsApp Sandbox page

### 2.2 Join the Sandbox

You'll see something like:

```
To join this sandbox, send:
  join yellow-mountain
to WhatsApp number:
  +1 415 523 8886
```

**Action:**
1. Open WhatsApp on your phone
2. Start a new chat with **+1 415 523 8886**
3. Send the message: `join yellow-mountain` (your code will be different)
4. You'll receive: "You are all set!"

✅ **You're now connected to Twilio WhatsApp!**

---

## 🔑 Step 3: Get Your Credentials

### 3.1 Find Your Account SID and Auth Token

1. Go to Twilio Console home: https://console.twilio.com/
2. Look for **Account Info** box on the right side
3. You'll see:
   - **Account SID:** ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   - **Auth Token:** Click "Show" to reveal

**Copy both values!**

### 3.2 Get Your WhatsApp Numbers

**From WhatsApp Number** (Twilio's number):
- Usually: `whatsapp:+14155238886`
- Check on the WhatsApp Sandbox page

**To WhatsApp Number** (Your phone):
- Your phone number in international format
- Example: If your US number is (206) 555-1234
- Format: `whatsapp:+12065551234`

---

## 📝 Step 4: Configure .env File

Now add your credentials to `.env` file:

```bash
# Open .env file
nano .env
```

**Add these lines (replace with your actual values):**

```bash
# Twilio WhatsApp Configuration
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_actual_auth_token_here
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
TWILIO_WHATSAPP_TO=whatsapp:+1YOUR_PHONE_NUMBER
```

**Example:**
```bash
TWILIO_ACCOUNT_SID=AC1234567890abcdef1234567890abcd
TWILIO_AUTH_TOKEN=abcdef1234567890abcdef1234567890
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
TWILIO_WHATSAPP_TO=whatsapp:+12065551234
```

**Save the file** (Ctrl+O, Enter, Ctrl+X)

---

## 📦 Step 5: Install Twilio Package

```bash
source venv/bin/activate
pip install twilio
```

---

## 🧪 Step 6: Test the Setup

### Test 1: Simple Test Message

```bash
python3 -c "
from src.utils import WhatsAppNotifier
from dotenv import load_dotenv
import json

load_dotenv()

notifier = WhatsAppNotifier()

test_article = {
    'title': '✅ Test: WhatsApp Integration Working!',
    'source': 'News Aggregator',
    'relevance_score': 100,
    'subtopic': 'System Test',
    'summary': 'Your news aggregator is successfully connected to WhatsApp. You will receive daily digests here.',
    'key_points': json.dumps(['Setup complete', 'WhatsApp working', 'Ready for daily digests']),
    'url': 'https://example.com/test'
}

print('Sending test message...')
result = notifier.send_daily_digest([test_article], limit=1, compact=True)
print('✓ Test message sent!' if result else '✗ Failed to send')
"
```

**Expected:** You should receive a WhatsApp message within 5-10 seconds!

### Test 2: Full Daily Digest

```bash
python3 daily_digest.py
```

This will:
1. ✅ Fetch latest news
2. ✅ Summarize with AI
3. ✅ Send top 20 articles to WhatsApp
4. ✅ Show message length and segment count

**Check your WhatsApp!** You should receive the full digest.

---

## ⏰ Step 7: Set Up Daily Automation

### 7.1 Get Full Project Path

```bash
pwd
```

Copy the output (e.g., `/Users/a90362/Documents/D/AI_Project/claude-code/00-News-Aggregator-Oct2025`)

### 7.2 Edit Crontab

```bash
crontab -e
```

**Press `i` to enter insert mode**

### 7.3 Add Cron Job

Paste this line (replace `/FULL/PATH/TO/PROJECT` with your actual path):

```bash
0 8 * * * cd /Users/a90362/Documents/D/AI_Project/claude-code/00-News-Aggregator-Oct2025 && /Users/a90362/Documents/D/AI_Project/claude-code/00-News-Aggregator-Oct2025/venv/bin/python3 daily_digest.py >> /Users/a90362/Documents/D/AI_Project/claude-code/00-News-Aggregator-Oct2025/logs/digest.log 2>&1
```

**Press `Esc`, then type `:wq` and press `Enter` to save**

### 7.4 Verify Cron Job

```bash
crontab -l
```

You should see your cron job listed.

### 7.5 Cron Schedule Options

```bash
# 8:00 AM daily
0 8 * * *

# 7:00 AM on weekdays only
0 7 * * 1-5

# 8:00 AM and 6:00 PM daily
0 8,18 * * *

# Every 3 hours from 6 AM to 9 PM
0 6-21/3 * * *
```

---

## ✅ Verification Checklist

- [ ] Twilio account created
- [ ] Phone number verified
- [ ] WhatsApp sandbox joined (sent "join" message)
- [ ] Account SID copied
- [ ] Auth Token copied
- [ ] `.env` file updated with credentials
- [ ] Twilio package installed
- [ ] Test message received on WhatsApp
- [ ] Full digest test successful
- [ ] Cron job added
- [ ] Logs directory exists

---

## 🔧 Troubleshooting

### "Missing Twilio credentials" Error

**Check your .env file:**
```bash
cat .env | grep TWILIO
```

Should show:
```
TWILIO_ACCOUNT_SID=AC...
TWILIO_AUTH_TOKEN=...
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
TWILIO_WHATSAPP_TO=whatsapp:+1...
```

### "Not authorized" Error

- Check Auth Token is correct (no extra spaces)
- Auth Token expires? Re-copy from Twilio Console

### WhatsApp Not Receiving Messages

1. **Sandbox expired?** (72-hour timeout)
   - Re-send `join <code>` to Twilio WhatsApp number

2. **Check Twilio Console:**
   - Go to Monitor → Logs → Messaging
   - Check for error messages

3. **Verify phone number format:**
   ```
   ✅ whatsapp:+12065551234  (correct)
   ❌ whatsapp:+1 206 555 1234  (wrong - has spaces)
   ❌ whatsapp:2065551234  (wrong - missing +1)
   ```

### Cron Job Not Running

1. **Check logs:**
   ```bash
   tail -20 logs/digest.log
   ```

2. **Test manually:**
   ```bash
   cd /full/path/to/project
   ./venv/bin/python3 daily_digest.py
   ```

3. **Check cron is running:**
   ```bash
   sudo launchctl list | grep cron
   ```

---

## 📊 Monitor Your Setup

### Check Last Digest Run
```bash
tail -20 logs/digest.log
```

### View Database Stats
```bash
python3 main.py view --limit 5
python3 main.py stats
```

### Test Send Anytime
```bash
python3 daily_digest.py
```

---

## 💰 Costs Summary

**Free Trial:**
- $15.50 credit
- ~775 days of daily digests (2+ years!)

**After Trial:**
- WhatsApp: $0.005 per message segment
- 20 articles compact: ~4 segments = $0.02/day
- **Annual cost: $7.30**

---

## 🎉 Success!

You're all set! Tomorrow morning at 8 AM, you'll receive:
- 📰 20 top articles
- ⭐ AI-generated summaries
- 🔗 Links to full articles
- 📊 Relevance scores

**Enjoy your automated news digest!** 🚀
