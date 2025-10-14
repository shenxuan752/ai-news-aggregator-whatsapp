# 📰 AI News Aggregator with WhatsApp Automation

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Powered by Claude](https://img.shields.io/badge/Powered%20by-Claude%20AI-orange.svg)](https://www.anthropic.com/claude)

An intelligent news aggregator that fetches, filters, and summarizes tech & investment news from 12+ sources, then delivers personalized daily digests directly to your WhatsApp. Built with Claude AI for smart summarization and Twilio for WhatsApp integration.

![News Aggregator Demo](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)

## ✨ Features

### 🤖 AI-Powered Intelligence
- **Claude AI Summarization**: Generates concise 2-3 sentence summaries with key points
- **Relevance Scoring**: Automatically scores articles 0-100 for importance
- **Topic Categorization**: Auto-categorizes into tech subtopics (AI, blockchain, cybersecurity, etc.)

### 📱 WhatsApp Automation
- **Daily Digests**: Automated delivery at your preferred time (configurable via cron)
- **Smart Formatting**: Compact format optimized for mobile reading
- **Message Splitting**: Automatically splits into multiple messages to stay under WhatsApp's 1600 char limit
- **Cost Optimized**: ~$7.30/year with free trial covering 2+ years

### 🔍 Smart Content Filtering
- **Duplicate Removal**: Uses SequenceMatcher algorithm to detect near-duplicates
- **Clickbait Detection**: Filters out low-quality content with pattern matching
- **Multi-source**: Aggregates from 12 premium sources (TechCrunch, Bloomberg, Wired, etc.)
- **Quality Control**: Removes articles under 100 characters

### 💾 Data Management
- **SQLite Database**: Persistent storage with SQLAlchemy ORM
- **CLI Interface**: Rich terminal UI with Click framework
- **Statistics Dashboard**: View aggregation stats and trends

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- [Anthropic API Key](https://console.anthropic.com/) (for Claude AI)
- [Twilio Account](https://www.twilio.com/try-twilio) (for WhatsApp, includes $15.50 free credit)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/shenxuan752/ai-news-aggregator-whatsapp.git
cd ai-news-aggregator-whatsapp
```

2. **Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your credentials:
# - ANTHROPIC_API_KEY (get from https://console.anthropic.com/)
# - TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN (get from https://console.twilio.com/)
# - TWILIO_WHATSAPP_FROM, TWILIO_WHATSAPP_TO
```

5. **Initialize database**
```bash
python main.py init
```

6. **Test the setup**
```bash
# Fetch and summarize latest news
python main.py fetch

# View top 10 articles
python main.py view --limit 10

# Send test WhatsApp message
python daily_digest.py
```

### 📖 Detailed Setup Guides
- **[5-Minute Quickstart](QUICKSTART.md)** - Fast setup guide
- **[Twilio WhatsApp Setup](TWILIO_SETUP_STEPS.md)** - Step-by-step WhatsApp configuration
- **[Automation Setup](AUTOMATION_QUICK_START.md)** - Configure daily cron job

## 💻 Usage

### CLI Commands

```bash
# Initialize database
python main.py init

# Fetch latest news from all sources
python main.py fetch

# View articles
python main.py view --category tech --limit 20
python main.py view --category investment --limit 10
python main.py view  # View all

# View statistics
python main.py stats

# Cleanup old articles
python main.py cleanup --days 30
```

### Daily Automation

Set up automated daily digests with cron:

```bash
# Edit crontab
crontab -e

# Add this line for 6 PM daily:
0 18 * * * cd /path/to/ai-news-aggregator-whatsapp && ./venv/bin/python3 daily_digest.py >> logs/digest.log 2>&1
```

Or use the provided setup script:
```bash
bash setup_cron.sh
```

### Manual WhatsApp Digest

```bash
# Send daily digest to WhatsApp (top 20 articles)
python daily_digest.py
```

## 📊 What You'll Receive

**Daily WhatsApp Format:**
```
📰 *Daily News - ALL*
📊 20 articles | ⭐ Avg: 78/100

*1. Article Title Here*
⭐85 | TechCrunch
Summary text with key insights and important
information about the article...
🔗 https://article-url.com

*2. Next Article*
⭐80 | Bloomberg Markets
...
```

**Delivery:** 3-5 WhatsApp messages (automatically split)

## 🏗️ Project Structure

```
ai-news-aggregator-whatsapp/
├── src/
│   ├── aggregator/          # RSS feed fetching
│   │   └── rss_fetcher.py   # Fetches from 12 sources
│   ├── summarizer/          # AI summarization
│   │   └── ai_summarizer.py # Claude API integration
│   ├── filters/             # Content filtering
│   │   └── content_filter.py # Duplicate & clickbait removal
│   ├── models/              # Database models
│   │   ├── article.py       # Article schema
│   │   └── database.py      # SQLAlchemy setup
│   └── utils/               # Utilities
│       └── whatsapp_notifier.py # Twilio WhatsApp API
├── config/
│   └── sources.yaml         # News source configuration
├── main.py                  # CLI entry point
├── daily_digest.py          # Automation script
├── setup_cron.sh            # Cron setup helper
├── requirements.txt         # Python dependencies
└── docs/                    # Documentation
```

## 🔧 Configuration

### News Sources

Edit `config/sources.yaml` to add/remove sources:

```yaml
technology:
  - name: "TechCrunch"
    url: "https://techcrunch.com/feed/"
    category: "tech"
  - name: "Your Source"
    url: "https://example.com/feed.rss"
    category: "tech"
```

### Daily Digest Settings

Edit `daily_digest.py`:

```python
MAX_SUMMARIZE = 20      # Number of articles to summarize
WHATSAPP_LIMIT = 20     # Number to send to WhatsApp
WHATSAPP_COMPACT = True # Use compact format (recommended)
```

### Message Format

Two formats available:

**Compact (default):** ~250 chars/article, fits 20 articles in ~5 messages
**Full:** ~500 chars/article with key points, fits 10 articles in ~5 messages

Edit in `daily_digest.py`:
```python
notifier.send_daily_digest(articles, limit=20, compact=True)
```

## 💰 Cost Breakdown

**Setup:**
- Twilio Free Trial: $15.50 credit
- Anthropic API: Pay as you go

**Daily Costs:**
- WhatsApp: 4 segments × $0.005 = $0.02/day
- Claude AI: 20 summaries × $0.001 = $0.02/day
- **Total: $0.04/day = $14.60/year**

**Free Trial Duration:** ~387 days (over 1 year free!)

## 📈 News Sources

### Technology (6 sources)
- TechCrunch
- The Verge
- Ars Technica
- Hacker News
- MIT Technology Review
- Wired

### Investment (6 sources)
- Bloomberg Markets
- Reuters Business
- Financial Times
- MarketWatch
- Seeking Alpha
- Yahoo Finance

## 🧪 Testing

```bash
# Test RSS fetching
python -c "from src.aggregator import RSSFetcher; print(RSSFetcher().fetch_all())"

# Test AI summarization
python -c "from src.summarizer import AISummarizer; s=AISummarizer(); print(s.summarize_article({'title':'Test','content':'Test content','category':'tech'}))"

# Test WhatsApp (sends test message)
python src/utils/whatsapp_notifier.py
```

## 🐛 Troubleshooting

### WhatsApp Not Receiving Messages

**Issue:** Sandbox expired (72-hour timeout)

**Fix:** Re-join Twilio sandbox
1. Open WhatsApp
2. Message: +1 415 523 8886
3. Send: `join <your-code>`

### Rate Limiting (429 Errors)

Normal behavior - the script automatically retries. With 20 articles, expect 3-5 minutes due to Claude API rate limits.

### Cron Not Running

**Check logs:**
```bash
tail -50 logs/digest.log
```

**Test manually:**
```bash
cd /path/to/project
./venv/bin/python3 daily_digest.py
```

## 📚 Documentation

- [Product Requirements (PRD.md)](PRD.md) - Detailed product specifications
- [Quick Start Guide (QUICKSTART.md)](QUICKSTART.md) - 5-minute setup
- [Twilio Setup (TWILIO_SETUP_STEPS.md)](TWILIO_SETUP_STEPS.md) - WhatsApp configuration
- [Message Format Comparison (MESSAGE_FORMAT_COMPARISON.md)](MESSAGE_FORMAT_COMPARISON.md)
- [Demo Results (DEMO_RESULTS.md)](DEMO_RESULTS.md) - Sample outputs
- [Setup Complete Guide (SETUP_COMPLETE.md)](SETUP_COMPLETE.md) - Post-installation

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **[Anthropic Claude](https://www.anthropic.com/)** - AI summarization
- **[Twilio](https://www.twilio.com/)** - WhatsApp API
- **[Claude Code](https://claude.com/claude-code)** - Development assistant

## 📧 Contact

Xuan Shen - [@shenxuan752](https://github.com/shenxuan752)

Project Link: [https://github.com/shenxuan752/ai-news-aggregator-whatsapp](https://github.com/shenxuan752/ai-news-aggregator-whatsapp)

---

**Built with ❤️ using Claude Code**
