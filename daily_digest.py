#!/usr/bin/env python3
"""
Daily News Digest Script
Fetches news, summarizes, and sends to WhatsApp
Run this script via cron for daily automation
"""

import sys
from datetime import datetime
from dotenv import load_dotenv

from src.aggregator import RSSFetcher
from src.summarizer import AISummarizer
from src.filters import ContentFilter
from src.models import db, Article
from src.utils import WhatsAppNotifier

# Load environment variables
load_dotenv()


def fetch_and_save_articles(max_per_source=10, max_summarize=20, category='all'):
    """Fetch, filter, summarize and save articles"""
    print(f"\n[{datetime.now()}] Starting daily news fetch...")

    # Initialize database
    db.create_tables()

    # Step 1: Fetch articles
    print(f"Step 1/4: Fetching articles from RSS feeds...")
    fetcher = RSSFetcher()

    if category == 'all':
        articles = fetcher.fetch_all(max_per_source=max_per_source)
    else:
        articles = fetcher.fetch_by_category(category, max_per_source=max_per_source)

    print(f"  ✓ Fetched {len(articles)} articles")

    # Step 2: Filter articles
    print(f"Step 2/4: Filtering content...")
    content_filter = ContentFilter()
    filtered_articles = content_filter.filter_articles(articles)
    print(f"  ✓ Filtered to {len(filtered_articles)} quality articles")

    # Step 3: Summarize articles
    print(f"Step 3/4: Summarizing top {min(max_summarize, len(filtered_articles))} articles...")

    try:
        summarizer = AISummarizer()
        summarized_articles = summarizer.summarize_batch(filtered_articles, max_articles=max_summarize)
        # Add remaining articles without summaries
        if len(filtered_articles) > max_summarize:
            summarized_articles.extend(filtered_articles[max_summarize:])
        print(f"  ✓ Summarized {min(max_summarize, len(filtered_articles))} articles")
    except Exception as e:
        print(f"  Error during summarization: {e}")
        summarized_articles = filtered_articles

    # Step 4: Save to database
    print(f"Step 4/4: Saving to database...")
    session = db.get_session()

    saved_count = 0
    duplicate_count = 0

    for article_data in summarized_articles:
        # Check if article already exists
        existing = session.query(Article).filter_by(url=article_data['url']).first()

        if existing:
            duplicate_count += 1
            continue

        article = Article(
            title=article_data.get('title'),
            url=article_data.get('url'),
            source=article_data.get('source'),
            category=article_data.get('category'),
            subtopic=article_data.get('subtopic', ''),
            description=article_data.get('description', ''),
            content=article_data.get('content', ''),
            summary=article_data.get('summary', ''),
            key_points=article_data.get('key_points', ''),
            relevance_score=article_data.get('relevance_score', 50),
            published_date=article_data.get('published_date'),
            author=article_data.get('author', ''),
            is_duplicate=article_data.get('is_duplicate', False),
            is_filtered=article_data.get('is_filtered', False)
        )

        session.add(article)
        saved_count += 1

    session.commit()
    session.close()

    print(f"  ✓ Saved {saved_count} new articles (skipped {duplicate_count} duplicates)")

    return summarized_articles[:max_summarize]  # Return summarized articles for WhatsApp


def send_whatsapp_digest(articles, category='all', limit=20, compact=True):
    """Send digest to WhatsApp

    Args:
        articles: List of article dicts
        category: 'tech', 'investment', or 'all'
        limit: Number of articles to send (default 20)
        compact: Use compact format (default True for efficiency)
    """
    print(f"\nSending WhatsApp digest...")

    try:
        notifier = WhatsAppNotifier()
        success = notifier.send_daily_digest(
            articles,
            category=category,
            limit=limit,
            compact=compact
        )

        if success:
            print(f"  ✓ WhatsApp digest sent successfully!")
        else:
            print(f"  ✗ Failed to send WhatsApp digest")

        return success

    except Exception as e:
        print(f"  ✗ Error sending WhatsApp: {e}")
        return False


def main():
    """Main function to run daily digest"""
    # Configuration
    MAX_PER_SOURCE = 10
    MAX_SUMMARIZE = 20
    CATEGORY = 'all'  # 'tech', 'investment', or 'all'
    WHATSAPP_LIMIT = 20  # Top 20 articles in WhatsApp (compact format)
    WHATSAPP_COMPACT = True  # Use compact format to fit more articles

    try:
        # Fetch and save articles
        articles = fetch_and_save_articles(
            max_per_source=MAX_PER_SOURCE,
            max_summarize=MAX_SUMMARIZE,
            category=CATEGORY
        )

        # Send to WhatsApp
        if articles:
            send_whatsapp_digest(
                articles,
                category=CATEGORY,
                limit=WHATSAPP_LIMIT,
                compact=WHATSAPP_COMPACT
            )
        else:
            print("No new articles to send")

        print(f"\n✓ Daily digest complete at {datetime.now()}")
        return 0

    except Exception as e:
        print(f"\n✗ Error in daily digest: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
