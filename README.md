# News Aggregator - Technology & Investment

An AI-powered news aggregator that filters, summarizes, and presents relevant technology and investment news to save your time.

## Features

- **Multi-source Aggregation**: Fetches news from multiple RSS feeds
- **AI-Powered Summarization**: Uses Claude API to generate concise summaries
- **Smart Filtering**: Removes duplicates and low-quality content
- **Topic Categorization**: Automatically categorizes into Tech and Investment topics
- **CLI Interface**: Simple command-line interface to view and manage news

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env and add your API keys
```

4. Initialize the database:
```bash
python -m src.models.database
```

## Usage

### Fetch latest news:
```bash
python main.py fetch
```

### View news:
```bash
python main.py view --category tech
python main.py view --category investment
python main.py view --all
```

### Run continuous updates:
```bash
python main.py run
```

## Project Structure

```
00-News-Aggregator-Oct2025/
├── src/
│   ├── aggregator/      # RSS feed fetching
│   ├── summarizer/      # AI summarization
│   ├── filters/         # Content filtering
│   ├── models/          # Database models
│   └── utils/           # Utility functions
├── tests/               # Unit tests
├── config/              # Configuration files
├── data/                # Database and cache
├── main.py              # Entry point
└── requirements.txt     # Dependencies
```

## Configuration

Edit `config/sources.yaml` to add or remove news sources.

## License

MIT
