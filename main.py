#!/usr/bin/env python3
"""
News Aggregator - Main Entry Point
Fetches, filters, and summarizes tech and investment news
"""

import click
import os
import json
from datetime import datetime
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown

from src.aggregator import RSSFetcher
from src.summarizer import AISummarizer
from src.filters import ContentFilter
from src.models import db, Article, init_db

# Load environment variables
load_dotenv()

console = Console()


@click.group()
def cli():
    """News Aggregator - Tech & Investment News"""
    pass


@cli.command()
@click.option('--max-per-source', default=10, help='Maximum articles per source')
@click.option('--max-summarize', default=20, help='Maximum articles to summarize (cost control)')
@click.option('--category', type=click.Choice(['tech', 'investment', 'all']), default='all', help='Category to fetch')
def fetch(max_per_source, max_summarize, category):
    """Fetch and process latest news articles"""
    console.print("\n[bold cyan]News Aggregator - Fetching Articles[/bold cyan]\n")

    # Initialize database
    db.create_tables()

    # Step 1: Fetch articles
    console.print("[yellow]Step 1/4:[/yellow] Fetching articles from RSS feeds...")
    fetcher = RSSFetcher()

    if category == 'all':
        articles = fetcher.fetch_all(max_per_source=max_per_source)
    else:
        articles = fetcher.fetch_by_category(category, max_per_source=max_per_source)

    console.print(f"  ✓ Fetched {len(articles)} articles\n")

    # Step 2: Filter articles
    console.print("[yellow]Step 2/4:[/yellow] Filtering content...")
    content_filter = ContentFilter()
    filtered_articles = content_filter.filter_articles(articles)
    console.print(f"  ✓ Filtered to {len(filtered_articles)} quality articles\n")

    # Step 3: Summarize articles
    console.print(f"[yellow]Step 3/4:[/yellow] Summarizing top {min(max_summarize, len(filtered_articles))} articles...")

    if max_summarize == 0 or not os.getenv("ANTHROPIC_API_KEY") or os.getenv("ANTHROPIC_API_KEY") == "your_anthropic_api_key_here":
        if not os.getenv("ANTHROPIC_API_KEY") or os.getenv("ANTHROPIC_API_KEY") == "your_anthropic_api_key_here":
            console.print("  [yellow]⚠ ANTHROPIC_API_KEY not set. Skipping summarization.[/yellow]")
        else:
            console.print("  [yellow]Skipping summarization (max_summarize=0).[/yellow]")
        summarized_articles = filtered_articles
    else:
        try:
            summarizer = AISummarizer()
            summarized_articles = summarizer.summarize_batch(filtered_articles, max_articles=max_summarize)
            # Add remaining articles without summaries
            if len(filtered_articles) > max_summarize:
                summarized_articles.extend(filtered_articles[max_summarize:])
            console.print(f"  ✓ Summarized {min(max_summarize, len(filtered_articles))} articles\n")
        except Exception as e:
            console.print(f"  [red]Error during summarization: {e}[/red]")
            console.print("  [yellow]Continuing without summaries...[/yellow]\n")
            summarized_articles = filtered_articles

    # Step 4: Save to database
    console.print("[yellow]Step 4/4:[/yellow] Saving to database...")
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

    console.print(f"  ✓ Saved {saved_count} new articles (skipped {duplicate_count} duplicates)\n")
    console.print(f"[bold green]✓ Fetch complete![/bold green] Run 'python main.py view' to see articles.\n")


@cli.command()
@click.option('--category', type=click.Choice(['tech', 'investment', 'all']), default='all', help='Category filter')
@click.option('--limit', default=10, help='Number of articles to display')
@click.option('--min-score', default=0, help='Minimum relevance score (0-100)')
def view(category, limit, min_score):
    """View aggregated news articles"""
    session = db.get_session()

    # Build query
    query = session.query(Article).filter(Article.is_filtered == False)

    if category != 'all':
        query = query.filter(Article.category == category)

    if min_score > 0:
        query = query.filter(Article.relevance_score >= min_score)

    # Order by relevance score and date
    articles = query.order_by(Article.relevance_score.desc(), Article.published_date.desc()).limit(limit).all()

    if not articles:
        console.print("\n[yellow]No articles found. Run 'python main.py fetch' first.[/yellow]\n")
        session.close()
        return

    # Display articles
    console.print(f"\n[bold cyan]News Aggregator - {category.upper()} News[/bold cyan]")
    console.print(f"Showing top {len(articles)} articles\n")

    for i, article in enumerate(articles, 1):
        # Create panel for each article
        title = f"[bold]{article.title}[/bold]"

        content_parts = []
        content_parts.append(f"[cyan]Source:[/cyan] {article.source}")
        content_parts.append(f"[cyan]Category:[/cyan] {article.category}")

        if article.subtopic:
            content_parts.append(f"[cyan]Topic:[/cyan] {article.subtopic}")

        content_parts.append(f"[cyan]Relevance:[/cyan] {article.relevance_score}/100")

        if article.published_date:
            content_parts.append(f"[cyan]Published:[/cyan] {article.published_date.strftime('%Y-%m-%d %H:%M')}")

        content_parts.append("")

        if article.summary:
            content_parts.append(f"[green]Summary:[/green] {article.summary}")

        if article.key_points:
            try:
                points = json.loads(article.key_points)
                if points:
                    content_parts.append("\n[green]Key Points:[/green]")
                    for point in points:
                        content_parts.append(f"  • {point}")
            except:
                pass

        content_parts.append(f"\n[bold cyan]🔗 Read Full Article:[/bold cyan]")
        content_parts.append(f"[link={article.url}]{article.url}[/link]")
        content_parts.append(f"[dim]Source: {article.source}[/dim]")

        content = "\n".join(content_parts)

        panel = Panel(
            content,
            title=f"[{i}] {title}",
            border_style="blue",
            padding=(1, 2)
        )

        console.print(panel)
        console.print()

    session.close()


@cli.command()
@click.option('--days', default=7, help='Number of days to keep')
def cleanup(days):
    """Clean up old articles from database"""
    from datetime import timedelta

    session = db.get_session()
    cutoff_date = datetime.utcnow() - timedelta(days=days)

    deleted = session.query(Article).filter(Article.fetched_date < cutoff_date).delete()
    session.commit()
    session.close()

    console.print(f"\n[green]✓ Deleted {deleted} articles older than {days} days[/green]\n")


@cli.command()
def init():
    """Initialize the database"""
    console.print("\n[cyan]Initializing database...[/cyan]")
    init_db()
    console.print("[green]✓ Database initialized successfully![/green]\n")


@cli.command()
def stats():
    """Show database statistics"""
    session = db.get_session()

    total = session.query(Article).count()
    tech = session.query(Article).filter(Article.category == 'tech').count()
    investment = session.query(Article).filter(Article.category == 'investment').count()
    filtered = session.query(Article).filter(Article.is_filtered == True).count()

    # Get average relevance score
    from sqlalchemy import func
    avg_score = session.query(func.avg(Article.relevance_score)).scalar() or 0

    # Get article count by source
    from sqlalchemy import func
    sources = session.query(Article.source, func.count(Article.id)).group_by(Article.source).all()

    session.close()

    # Display stats
    console.print("\n[bold cyan]Database Statistics[/bold cyan]\n")

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", justify="right")

    table.add_row("Total Articles", str(total))
    table.add_row("Tech Articles", str(tech))
    table.add_row("Investment Articles", str(investment))
    table.add_row("Filtered Out", str(filtered))
    table.add_row("Average Relevance", f"{avg_score:.1f}/100")

    console.print(table)

    if sources:
        console.print("\n[bold cyan]Articles by Source[/bold cyan]\n")
        source_table = Table(show_header=True, header_style="bold magenta")
        source_table.add_column("Source", style="cyan")
        source_table.add_column("Count", justify="right")

        for source, count in sorted(sources, key=lambda x: x[1], reverse=True):
            source_table.add_row(source, str(count))

        console.print(source_table)

    console.print()


if __name__ == "__main__":
    cli()
