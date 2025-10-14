from typing import List, Dict
from difflib import SequenceMatcher
import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ContentFilter:
    """Filter and deduplicate news articles"""

    def __init__(self, similarity_threshold: float = 0.75):
        """
        Initialize content filter

        Args:
            similarity_threshold: Threshold for considering articles as duplicates (0-1)
        """
        self.similarity_threshold = similarity_threshold

        # Common clickbait patterns
        self.clickbait_patterns = [
            r"you won't believe",
            r"shocking",
            r"this one trick",
            r"number \d+ will",
            r"what happens next",
            r"doctors hate",
            r"click here",
            r"this is why",
            r"the reason is",
        ]

        # Low quality indicators
        self.low_quality_keywords = [
            "sponsored",
            "advertisement",
            "paid promotion",
        ]

    def is_clickbait(self, title: str) -> bool:
        """Check if article title is clickbait"""
        title_lower = title.lower()

        for pattern in self.clickbait_patterns:
            if re.search(pattern, title_lower):
                logger.debug(f"Clickbait detected: {title}")
                return True

        return False

    def is_low_quality(self, article: Dict) -> bool:
        """Check if article is low quality"""
        title = article.get("title", "").lower()
        content = article.get("content", "").lower()
        description = article.get("description", "").lower()

        combined_text = f"{title} {content} {description}"

        for keyword in self.low_quality_keywords:
            if keyword in combined_text:
                logger.debug(f"Low quality content detected: {article.get('title', '')}")
                return True

        # Check if content is too short
        if len(content) < 100 and len(description) < 100:
            logger.debug(f"Content too short: {article.get('title', '')}")
            return True

        return False

    def calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts (0-1)"""
        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()

    def find_duplicates(self, articles: List[Dict]) -> List[int]:
        """
        Find duplicate articles in the list

        Returns:
            List of indices of duplicate articles to remove
        """
        duplicates = set()
        n = len(articles)

        for i in range(n):
            if i in duplicates:
                continue

            article1 = articles[i]
            title1 = article1.get("title", "")
            url1 = article1.get("url", "")

            for j in range(i + 1, n):
                if j in duplicates:
                    continue

                article2 = articles[j]
                title2 = article2.get("title", "")
                url2 = article2.get("url", "")

                # Check URL similarity (same article)
                if url1 == url2:
                    duplicates.add(j)
                    logger.debug(f"Duplicate URL found: {url1}")
                    continue

                # Check title similarity
                title_similarity = self.calculate_similarity(title1, title2)
                if title_similarity >= self.similarity_threshold:
                    duplicates.add(j)
                    logger.debug(f"Similar titles found: '{title1}' vs '{title2}' (similarity: {title_similarity:.2f})")

        logger.info(f"Found {len(duplicates)} duplicate articles out of {n}")
        return list(duplicates)

    def filter_articles(self, articles: List[Dict]) -> List[Dict]:
        """
        Filter articles by removing duplicates, clickbait, and low-quality content

        Returns:
            Filtered list of articles
        """
        logger.info(f"Starting filtering process for {len(articles)} articles")

        # First pass: remove clickbait and low quality
        filtered = []
        removed_count = 0

        for article in articles:
            if self.is_clickbait(article.get("title", "")):
                removed_count += 1
                article["is_filtered"] = True
                article["filter_reason"] = "clickbait"
                continue

            if self.is_low_quality(article):
                removed_count += 1
                article["is_filtered"] = True
                article["filter_reason"] = "low_quality"
                continue

            article["is_filtered"] = False
            filtered.append(article)

        logger.info(f"Removed {removed_count} clickbait/low-quality articles")

        # Second pass: remove duplicates
        duplicate_indices = self.find_duplicates(filtered)

        final_filtered = []
        for i, article in enumerate(filtered):
            if i in duplicate_indices:
                article["is_filtered"] = True
                article["is_duplicate"] = True
            else:
                article["is_duplicate"] = False
                final_filtered.append(article)

        logger.info(f"Final filtered count: {len(final_filtered)} articles")
        return final_filtered

    def rank_articles(self, articles: List[Dict]) -> List[Dict]:
        """
        Rank articles by relevance score

        Returns:
            Sorted list of articles (highest relevance first)
        """
        sorted_articles = sorted(
            articles,
            key=lambda x: x.get("relevance_score", 50),
            reverse=True
        )

        logger.info(f"Ranked {len(sorted_articles)} articles")
        return sorted_articles


if __name__ == "__main__":
    # Test the filter
    test_articles = [
        {
            "title": "You Won't Believe What Happened to Tech Stocks Today!",
            "content": "Something amazing happened...",
            "url": "http://example.com/1"
        },
        {
            "title": "Apple Announces New iPhone 15",
            "content": "Apple has announced the new iPhone 15 with improved camera and battery life. The device features a new A17 chip and will be available starting September.",
            "url": "http://example.com/2"
        },
        {
            "title": "Apple Announces New iPhone 15 Model",
            "content": "In a major announcement, Apple unveiled the iPhone 15 with enhanced features including better camera and longer battery.",
            "url": "http://example.com/3"
        },
        {
            "title": "Sponsored: Buy This Product Now",
            "content": "This is a paid advertisement for a product.",
            "url": "http://example.com/4"
        },
    ]

    filter = ContentFilter()
    filtered = filter.filter_articles(test_articles)

    print(f"\nOriginal: {len(test_articles)} articles")
    print(f"Filtered: {len(filtered)} articles")
    print("\nFiltered articles:")
    for article in filtered:
        print(f"  - {article['title']}")
