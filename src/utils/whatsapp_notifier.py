"""
WhatsApp Notifier using Twilio API
Sends news summaries to WhatsApp
"""

import os
from twilio.rest import Client
from typing import List, Dict
import json


class WhatsAppNotifier:
    """Send news summaries via WhatsApp using Twilio"""

    def __init__(self):
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.from_whatsapp = os.getenv("TWILIO_WHATSAPP_FROM")  # e.g., "whatsapp:+14155238886"
        self.to_whatsapp = os.getenv("TWILIO_WHATSAPP_TO")  # e.g., "whatsapp:+1234567890"

        if not all([self.account_sid, self.auth_token, self.from_whatsapp, self.to_whatsapp]):
            raise ValueError("Missing Twilio credentials in .env file")

        self.client = Client(self.account_sid, self.auth_token)

    def format_article(self, article: Dict, index: int, compact: bool = False) -> str:
        """Format a single article for WhatsApp"""
        if compact:
            # Ultra-compact format for fitting more articles
            lines = [f"\n*{index}. {article['title'][:80]}*"]
            lines.append(f"⭐{article['relevance_score']} | {article['source']}")

            if article.get('summary'):
                # Truncate summary to 150 chars
                summary = article['summary'][:150]
                if len(article['summary']) > 150:
                    summary += "..."
                lines.append(summary)

            lines.append(f"🔗 {article['url']}")
            lines.append("")

        else:
            # Standard format with more detail
            lines = [f"\n*[{index}] {article['title']}*"]
            lines.append(f"📰 {article['source']} | ⭐ {article['relevance_score']}/100")

            if article.get('subtopic'):
                lines.append(f"🏷️ {article['subtopic']}")

            if article.get('summary'):
                lines.append(f"\n{article['summary']}")

            if article.get('key_points'):
                try:
                    points = json.loads(article['key_points'])
                    if points:
                        lines.append("\n*Key Points:*")
                        for point in points[:3]:  # Limit to 3 points for brevity
                            lines.append(f"• {point}")
                except:
                    pass

            lines.append(f"\n🔗 {article['url']}")
            lines.append("-" * 40)

        return "\n".join(lines)

    def format_summary(self, articles: List[Dict], category: str = "all", compact: bool = False) -> str:
        """Format all articles into a WhatsApp message"""
        header = f"📰 *Daily News - {category.upper()}*\n"
        header += f"📊 {len(articles)} articles"

        # Calculate average relevance
        avg_relevance = sum(a.get('relevance_score', 50) for a in articles) / len(articles) if articles else 0
        header += f" | ⭐ Avg: {avg_relevance:.0f}/100\n"

        if not compact:
            header += f"{'=' * 40}\n"

        # Format articles
        article_texts = [self.format_article(a, i+1, compact=compact) for i, a in enumerate(articles)]

        full_message = header + "".join(article_texts)

        return full_message

    def send_message(self, message: str) -> bool:
        """Send a message via WhatsApp"""
        try:
            # WhatsApp messages have a 1600 character limit
            max_length = 1500
            messages = []

            if len(message) <= max_length:
                messages.append(message)
            else:
                # Split by newlines to preserve article boundaries
                lines = message.split('\n')
                current_msg = ""

                for line in lines:
                    # Check if adding this line would exceed limit
                    if len(current_msg) + len(line) + 1 < max_length:
                        current_msg += line + '\n'
                    else:
                        # Save current message and start new one
                        if current_msg:
                            messages.append(current_msg.strip())
                        current_msg = "📰 *Continued...*\n\n" + line + '\n'

                # Add remaining content
                if current_msg:
                    messages.append(current_msg.strip())

            # Send all message parts
            for i, msg in enumerate(messages):
                response = self.client.messages.create(
                    from_=self.from_whatsapp,
                    body=msg,
                    to=self.to_whatsapp
                )
                print(f"Message {i+1}/{len(messages)} sent: {response.sid}")

            return True

        except Exception as e:
            print(f"Error sending WhatsApp message: {e}")
            return False

    def send_daily_digest(self, articles: List[Dict], category: str = "all", limit: int = 20, compact: bool = True) -> bool:
        """Send daily digest of top articles

        Args:
            articles: List of article dicts
            category: 'tech', 'investment', or 'all'
            limit: Number of top articles to send (default 20)
            compact: Use compact format to fit more articles (default True)
        """
        # Sort by relevance and take top N
        sorted_articles = sorted(
            articles,
            key=lambda x: x.get('relevance_score', 0),
            reverse=True
        )[:limit]

        message = self.format_summary(sorted_articles, category, compact=compact)

        # Calculate estimated message segments
        estimated_segments = (len(message) // 1600) + 1
        print(f"  Message length: {len(message)} chars (~{estimated_segments} segments)")

        return self.send_message(message)

    def send_quick_summary(self, articles: List[Dict]) -> bool:
        """Send a quick summary (titles only)"""
        message = f"📰 *Quick News Update*\n{'=' * 40}\n\n"

        for i, article in enumerate(articles[:10], 1):
            message += f"{i}. {article['title']}\n"
            message += f"   ⭐ {article['relevance_score']}/100 | {article['source']}\n"
            message += f"   🔗 {article['url']}\n\n"

        return self.send_message(message)


if __name__ == "__main__":
    # Test the notifier
    from dotenv import load_dotenv
    load_dotenv()

    notifier = WhatsAppNotifier()

    test_articles = [
        {
            "title": "Test Article 1",
            "source": "TechCrunch",
            "relevance_score": 85,
            "subtopic": "AI",
            "summary": "This is a test summary of the article.",
            "key_points": json.dumps(["Point 1", "Point 2", "Point 3"]),
            "url": "https://example.com/article1"
        }
    ]

    notifier.send_daily_digest(test_articles)
