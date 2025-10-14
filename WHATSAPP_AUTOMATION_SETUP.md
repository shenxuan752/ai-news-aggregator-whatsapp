# WhatsApp Automation Setup Guide

This guide will help you set up daily automated news digests sent to your WhatsApp.

## 📋 Prerequisites

- Twilio account (for WhatsApp messaging)
- WhatsApp-enabled phone number
- Python environment (already set up)

## Step 1: Set Up Twilio WhatsApp (15 minutes)

### 1.1 Create Twilio Account

1. Go to [https://www.twilio.com/try-twilio](https://www.twilio.com/try-twilio)
2. Sign up for a free account
3. Verify your phone number

### 1.2 Enable WhatsApp Sandbox

1. In Twilio Console, go to **Messaging** → **Try it out** → **Send a WhatsApp message**
2. Follow instructions to join the WhatsApp Sandbox:
   - Send `join <your-sandbox-code>` to the Twilio WhatsApp number
   - Example: Send "join yellow-mountain" to +1 415 523 8886
3. You'll receive a confirmation on WhatsApp

### 1.3 Get Your Credentials

From the Twilio Console, find:
- **Account SID** (starts with AC...)
- **Auth Token** (click to reveal)
- **WhatsApp From Number** (usually +1 415 523 8886)
- **Your WhatsApp Number** (your verified phone number)

## Step 2: Configure Environment Variables

### 2.1 Update .env File

Add your Twilio credentials to `.env`:

```bash
# Twilio WhatsApp Configuration
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
TWILIO_WHATSAPP_TO=whatsapp:+15551234567  # Your phone number
```

**Important:**
- Use format `whatsapp:+<country_code><phone_number>`
- No spaces or dashes in phone numbers
- Include country code (e.g., +1 for US)

Example:
```
TWILIO_WHATSAPP_TO=whatsapp:+12065551234
```

## Step 3: Install Twilio Package

```bash
source venv/bin/activate
pip install twilio==9.3.7
```

## Step 4: Test WhatsApp Integration

### 4.1 Test Manual Send

```bash
python3 -c "
from src.utils import WhatsAppNotifier
from dotenv import load_dotenv
import json

load_dotenv()

notifier = WhatsAppNotifier()

test_article = {
    'title': 'Test: News Aggregator Setup',
    'source': 'System Test',
    'relevance_score': 100,
    'subtopic': 'Setup',
    'summary': 'This is a test message to verify WhatsApp integration is working correctly.',
    'key_points': json.dumps(['Setup complete', 'WhatsApp working', 'Ready for automation']),
    'url': 'https://example.com/test'
}

notifier.send_daily_digest([test_article], limit=1)
print('Test message sent!')
"
```

You should receive a WhatsApp message within seconds.

### 4.2 Test Daily Digest Script

```bash
python3 daily_digest.py
```

This will:
1. Fetch latest news
2. Summarize articles
3. Send top 5 to WhatsApp

## Step 5: Set Up Daily Automation with Cron

### 5.1 Make Script Executable

```bash
chmod +x daily_digest.py
```

### 5.2 Get Full Path

```bash
pwd
# Copy the full path, e.g., /Users/a90362/Documents/D/AI_Project/claude-code/00-News-Aggregator-Oct2025
```

### 5.3 Edit Crontab

```bash
crontab -e
```

### 5.4 Add Cron Job

Add this line (adjust path and time):

```bash
# Daily news digest at 8:00 AM
0 8 * * * cd /Users/a90362/Documents/D/AI_Project/claude-code/00-News-Aggregator-Oct2025 && /Users/a90362/Documents/D/AI_Project/claude-code/00-News-Aggregator-Oct2025/venv/bin/python3 daily_digest.py >> /Users/a90362/Documents/D/AI_Project/claude-code/00-News-Aggregator-Oct2025/logs/digest.log 2>&1
```

**Cron Schedule Examples:**
```bash
# 8:00 AM daily
0 8 * * *

# 8:00 AM and 6:00 PM daily
0 8,18 * * *

# 8:00 AM on weekdays only
0 8 * * 1-5

# Every 2 hours from 8 AM to 8 PM
0 8-20/2 * * *
```

### 5.5 Create Log Directory

```bash
mkdir -p logs
```

### 5.6 Verify Cron Job

```bash
crontab -l
```

## Step 6: Customize Your Digest

Edit `daily_digest.py` to customize:

```python
# Configuration (lines 105-109)
MAX_PER_SOURCE = 10        # Articles per source
MAX_SUMMARIZE = 20         # Articles to summarize with AI
CATEGORY = 'all'           # 'tech', 'investment', or 'all'
WHATSAPP_LIMIT = 5         # Top N articles in WhatsApp
```

## 📱 WhatsApp Message Format

Your daily digest will include:

```
📰 *Daily News Digest - ALL*
========================================
📊 5 articles
⭐ Avg Relevance: 78/100

*[1] Article Title*
📰 Source | ⭐ 85/100
🏷️ Topic

Summary text here...

*Key Points:*
• Point 1
• Point 2
• Point 3

🔗 https://article-url.com
----------------------------------------
[Article 2...]
```

## 🔧 Troubleshooting

### WhatsApp Not Receiving Messages

1. **Check Sandbox Status**
   - Re-send `join <sandbox-code>` to Twilio WhatsApp number
   - Sandbox expires after 72 hours of inactivity

2. **Verify .env Configuration**
   ```bash
   python3 -c "import os; from dotenv import load_dotenv; load_dotenv(); print('SID:', os.getenv('TWILIO_ACCOUNT_SID')[:10]); print('TO:', os.getenv('TWILIO_WHATSAPP_TO'))"
   ```

3. **Check Twilio Console**
   - Go to Messaging → Logs
   - Check for error messages

### Cron Job Not Running

1. **Check Cron Logs**
   ```bash
   cat logs/digest.log
   ```

2. **Test Manually**
   ```bash
   cd /full/path/to/project
   ./daily_digest.py
   ```

3. **Verify Python Path**
   ```bash
   which python3
   # Use full path in crontab
   ```

### Message Too Long

The script automatically splits long messages. If issues persist:
- Reduce `WHATSAPP_LIMIT` in `daily_digest.py`
- Edit `src/utils/whatsapp_notifier.py` to show fewer key points

## 💰 Costs

### Twilio Free Trial
- $15.50 credit
- WhatsApp messages: ~$0.005 per message
- **~3,000 messages free**

### After Trial
- WhatsApp: $0.005 per message
- Daily digest (1-2 messages): ~$0.01/day = **$3.60/year**

## 🚀 Production Setup (Optional)

For production WhatsApp (not sandbox):

1. **Apply for WhatsApp Business API**
   - Twilio Console → Messaging → WhatsApp → Request Access
   - Requires business verification (1-2 weeks)

2. **Get Dedicated WhatsApp Number**
   - Buy a Twilio phone number (~$1-2/month)
   - Enable WhatsApp on it

3. **Update .env**
   ```
   TWILIO_WHATSAPP_FROM=whatsapp:+15551234567
   ```

## 📊 Monitor Your Automation

### Check Last Run
```bash
tail -20 logs/digest.log
```

### View Database Stats
```bash
python3 main.py stats
```

### Test Specific Time
```bash
# Run digest manually
python3 daily_digest.py
```

## ✅ Success Checklist

- [ ] Twilio account created
- [ ] WhatsApp sandbox joined
- [ ] Credentials added to .env
- [ ] Twilio package installed
- [ ] Test message received
- [ ] daily_digest.py runs successfully
- [ ] Cron job added and verified
- [ ] Logs directory created
- [ ] First automated message received

## 🎉 You're All Set!

Your news aggregator will now automatically:
1. Fetch news every morning
2. Filter and summarize with AI
3. Send top 5 articles to WhatsApp
4. Log all activity

**Enjoy your automated news digest!** 📰📱
