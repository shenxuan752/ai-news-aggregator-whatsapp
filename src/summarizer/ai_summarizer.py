import os
import json
from typing import Dict, List, Optional
from anthropic import Anthropic
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AISummarizer:
    """AI-powered article summarizer using Claude API"""

    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-5-sonnet-20241022"):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")

        self.client = Anthropic(api_key=self.api_key)
        self.model = model

    def summarize_article(self, article: Dict) -> Dict:
        """
        Summarize a single article and extract key information

        Returns a dict with:
        - summary: concise 2-3 sentence summary
        - key_points: list of 3-5 bullet points
        - subtopic: detected subtopic
        - relevance_score: 0-100 score
        """
        title = article.get("title", "")
        content = article.get("content", article.get("description", ""))
        category = article.get("category", "")

        if not content or len(content) < 50:
            logger.warning(f"Skipping article with insufficient content: {title}")
            return {
                "summary": title,
                "key_points": [],
                "subtopic": "",
                "relevance_score": 30
            }

        prompt = self._create_summarization_prompt(title, content, category)

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                temperature=0,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            result_text = response.content[0].text
            result = self._parse_response(result_text)

            logger.info(f"Successfully summarized: {title[:50]}...")
            return result

        except Exception as e:
            logger.error(f"Error summarizing article '{title}': {e}")
            return {
                "summary": title,
                "key_points": [],
                "subtopic": "",
                "relevance_score": 50
            }

    def _create_summarization_prompt(self, title: str, content: str, category: str) -> str:
        """Create the prompt for Claude"""
        # Truncate content if too long (to manage token costs)
        max_content_length = 3000
        if len(content) > max_content_length:
            content = content[:max_content_length] + "..."

        return f"""You are a news analysis assistant. Analyze the following {category} article and provide:

1. A concise 2-3 sentence summary focusing on the most important information
2. 3-5 key bullet points highlighting the main facts, figures, or takeaways
3. The specific subtopic (e.g., "AI/ML", "Cloud Computing", "Stock Market", "IPO", etc.)
4. A relevance score from 0-100 (based on importance and actionability for professionals)

Title: {title}

Content: {content}

Return your response in this exact JSON format:
{{
  "summary": "Your 2-3 sentence summary here",
  "key_points": ["Point 1", "Point 2", "Point 3"],
  "subtopic": "Specific subtopic",
  "relevance_score": 85
}}

Only return the JSON, no additional text."""

    def _parse_response(self, response_text: str) -> Dict:
        """Parse Claude's JSON response"""
        try:
            # Extract JSON from response (in case there's extra text)
            start_idx = response_text.find("{")
            end_idx = response_text.rfind("}") + 1

            if start_idx == -1 or end_idx == 0:
                raise ValueError("No JSON found in response")

            json_str = response_text[start_idx:end_idx]
            result = json.loads(json_str)

            # Validate required fields
            required_fields = ["summary", "key_points", "subtopic", "relevance_score"]
            for field in required_fields:
                if field not in result:
                    result[field] = "" if field != "key_points" else []
                    if field == "relevance_score":
                        result[field] = 50

            return result

        except Exception as e:
            logger.error(f"Error parsing Claude response: {e}")
            logger.debug(f"Response text: {response_text}")
            return {
                "summary": "",
                "key_points": [],
                "subtopic": "",
                "relevance_score": 50
            }

    def summarize_batch(self, articles: List[Dict], max_articles: int = 10) -> List[Dict]:
        """
        Summarize multiple articles

        Args:
            articles: List of article dictionaries
            max_articles: Maximum number of articles to process (to control costs)

        Returns:
            List of articles with added summary information
        """
        summarized = []

        for i, article in enumerate(articles[:max_articles]):
            logger.info(f"Summarizing article {i+1}/{min(len(articles), max_articles)}")

            summary_data = self.summarize_article(article)

            # Add summary data to article
            article["summary"] = summary_data["summary"]
            article["key_points"] = json.dumps(summary_data["key_points"])  # Store as JSON string
            article["subtopic"] = summary_data["subtopic"]
            article["relevance_score"] = summary_data["relevance_score"]

            summarized.append(article)

        return summarized


if __name__ == "__main__":
    # Test the summarizer
    from dotenv import load_dotenv
    load_dotenv()

    summarizer = AISummarizer()

    test_article = {
        "title": "OpenAI Launches GPT-5 with Revolutionary Capabilities",
        "content": "OpenAI has announced the launch of GPT-5, their latest language model. The new model shows significant improvements in reasoning, coding, and multimodal understanding. CEO Sam Altman stated that GPT-5 represents a major leap forward in AI capabilities, with improved accuracy and reduced hallucinations. The model will be available through their API starting next month.",
        "category": "tech"
    }

    result = summarizer.summarize_article(test_article)
    print("\nSummary Result:")
    print(json.dumps(result, indent=2))
