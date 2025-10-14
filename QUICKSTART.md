# Quick Start Guide

## Setup (5 minutes)

### 1. Install Dependencies

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### 2. Configure API Key (Optional but Recommended)

For AI-powered summarization, you need an Anthropic API key:

```bash
# Copy the example env file
cp .env.example .env

# Edit .env and add your API key
# Get your key from: https://console.anthropic.com/
```

Edit `.env`:
```
ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
```

**Note:** The aggregator works without an API key, but you won't get AI summaries.

### 3. Initialize Database

```bash
python3 main.py init
```

## Basic Usage

### Fetch News

```bash
# Fetch tech news only (3 articles per source, no summaries)
python3 main.py fetch --category tech --max-per-source 3 --max-summarize 0

# Fetch all news with AI summaries (requires API key)
python3 main.py fetch --max-summarize 10

# Fetch investment news
python3 main.py fetch --category investment
```

### View Articles

```bash
# View top 10 articles
python3 main.py view

# View tech articles only
python3 main.py view --category tech --limit 5

# View high-relevance articles (when you have AI summaries)
python3 main.py view --min-score 70
```

### Check Statistics

```bash
python3 main.py stats
```

### Clean Up Old Articles

```bash
# Delete articles older than 7 days
python3 main.py cleanup --days 7
```

## Recommended Workflow

### Without API Key (Free)

```bash
# 1. Fetch latest news without AI summaries
python3 main.py fetch --max-per-source 5 --max-summarize 0

# 2. View articles
python3 main.py view --limit 10
```

### With API Key (Best Experience)

```bash
# 1. Fetch and summarize top articles
python3 main.py fetch --max-per-source 10 --max-summarize 20

# 2. View high-quality summarized articles
python3 main.py view --min-score 60
```

## Customization

### Add/Remove News Sources

Edit `config/sources.yaml` to customize your news sources:

```yaml
technology:
  - name: "Your Source Name"
    url: "https://example.com/feed.rss"
    category: "tech"
```

### Adjust Filtering

Edit `src/filters/content_filter.py` to customize:
- Clickbait detection patterns
- Similarity threshold for duplicates
- Low-quality content filters

## Troubleshooting

### No articles shown
Run `python3 main.py fetch` first to populate the database.

### API key errors
Make sure your `.env` file has the correct `ANTHROPIC_API_KEY` value.

### Feed parsing warnings
Some RSS feeds may have issues. The aggregator will log warnings but continue with other sources.

### Database errors
If you encounter database issues, you can reinitialize:
```bash
rm data/news_aggregator.db
python3 main.py init
```

## Daily Usage Pattern

```bash
# Morning: Fetch latest news
python3 main.py fetch --max-summarize 15

# View top stories
python3 main.py view --limit 10

# Weekly: Clean up old articles
python3 main.py cleanup --days 7
```

## Cost Management

AI summarization costs money (Claude API). To control costs:

1. **Limit summarization**: Use `--max-summarize 10` instead of processing all articles
2. **Fetch without summaries**: Use `--max-summarize 0` for free aggregation
3. **Batch processing**: Fetch once per day instead of multiple times

**Estimated costs:** ~$0.01-0.05 per 20 articles summarized (varies by article length)

## Next Steps

- Read the full [README.md](README.md) for detailed information
- Review the [PRD.md](PRD.md) for project requirements and roadmap
- Customize news sources in `config/sources.yaml`
- Set up a cron job for automatic daily fetching
