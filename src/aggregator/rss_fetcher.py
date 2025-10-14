import feedparser
import yaml
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RSSFetcher:
    """Fetches articles from RSS feeds"""

    def __init__(self, sources_file: str = None):
        if sources_file is None:
            sources_file = Path(__file__).parent.parent.parent / "config" / "sources.yaml"

        self.sources_file = sources_file
        self.sources = self._load_sources()

    def _load_sources(self) -> Dict:
        """Load RSS sources from YAML file"""
        try:
            with open(self.sources_file, "r") as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Error loading sources file: {e}")
            return {"technology": [], "investment": []}

    def fetch_feed(self, url: str, source_name: str, category: str) -> List[Dict]:
        """Fetch and parse a single RSS feed"""
        articles = []

        try:
            logger.info(f"Fetching feed from {source_name} ({url})")
            feed = feedparser.parse(url)

            if feed.bozo:
                logger.warning(f"Feed parsing issue for {source_name}: {feed.bozo_exception}")

            for entry in feed.entries:
                article = self._parse_entry(entry, source_name, category)
                if article:
                    articles.append(article)

            logger.info(f"Fetched {len(articles)} articles from {source_name}")

        except Exception as e:
            logger.error(f"Error fetching feed from {source_name}: {e}")

        return articles

    def _parse_entry(self, entry, source_name: str, category: str) -> Optional[Dict]:
        """Parse a single feed entry into article format"""
        try:
            # Extract published date
            published_date = None
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                published_date = datetime(*entry.published_parsed[:6])
            elif hasattr(entry, "updated_parsed") and entry.updated_parsed:
                published_date = datetime(*entry.updated_parsed[:6])

            # Extract description/summary
            description = ""
            if hasattr(entry, "summary"):
                description = entry.summary
            elif hasattr(entry, "description"):
                description = entry.description

            # Extract content
            content = ""
            if hasattr(entry, "content"):
                content = " ".join([c.value for c in entry.content])

            # Author
            author = entry.get("author", "")

            article = {
                "title": entry.get("title", "No Title"),
                "url": entry.get("link", ""),
                "source": source_name,
                "category": category,
                "description": description,
                "content": content if content else description,
                "published_date": published_date,
                "author": author,
            }

            return article

        except Exception as e:
            logger.error(f"Error parsing entry: {e}")
            return None

    def fetch_all(self, max_per_source: int = 20) -> List[Dict]:
        """Fetch articles from all configured sources"""
        all_articles = []

        # Fetch technology sources
        for source in self.sources.get("technology", []):
            articles = self.fetch_feed(
                url=source["url"],
                source_name=source["name"],
                category=source["category"]
            )
            all_articles.extend(articles[:max_per_source])

        # Fetch investment sources
        for source in self.sources.get("investment", []):
            articles = self.fetch_feed(
                url=source["url"],
                source_name=source["name"],
                category=source["category"]
            )
            all_articles.extend(articles[:max_per_source])

        logger.info(f"Total articles fetched: {len(all_articles)}")
        return all_articles

    def fetch_by_category(self, category: str, max_per_source: int = 20) -> List[Dict]:
        """Fetch articles from a specific category only"""
        articles = []

        category_key = "technology" if category == "tech" else category
        for source in self.sources.get(category_key, []):
            fetched = self.fetch_feed(
                url=source["url"],
                source_name=source["name"],
                category=source["category"]
            )
            articles.extend(fetched[:max_per_source])

        return articles


if __name__ == "__main__":
    # Test the fetcher
    fetcher = RSSFetcher()
    articles = fetcher.fetch_all(max_per_source=5)

    print(f"\nFetched {len(articles)} articles")
    if articles:
        print("\nSample article:")
        print(f"Title: {articles[0]['title']}")
        print(f"Source: {articles[0]['source']}")
        print(f"Category: {articles[0]['category']}")
        print(f"URL: {articles[0]['url']}")
