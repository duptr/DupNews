import asyncio
import aiohttp
import feedparser
import datetime
from processors.text_cleaner import clean_html, preprocess_text
from processors.batch_processor import process_batch
from langdetect import detect

# Asynchronous function that fetches a single RSS feed
async def fetch_feed(session, url):
    
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=20)) as response:
            return await response.text(), url
    except (aiohttp.ClientError, asyncio.TimeoutError) as e:
        from utils.logger_setup import logger
        logger.error(f"RSS fetch error ({url}): {str(e)[:100]}")
        return None, url

# Function that filters news from the last 24 hours
def filter_recent_articles(entries):
    
    now = datetime.datetime.now(datetime.timezone.utc)
    return sorted(
        (
            entry for entry in entries
            if entry.get('published_parsed') and 
            (now - datetime.datetime(*entry.published_parsed[:6], tzinfo=datetime.timezone.utc)).days == 0
        ),
        key=lambda x: datetime.datetime(*x.published_parsed[:6], tzinfo=datetime.timezone.utc),
        reverse=True
    )

# Function that filters news by topic
def filter_by_topic(entries, topics):
    
    search_fields = ['title', 'summary', 'description']
    return [
        entry for entry in entries
        if any(
            any(topic.lower() in (entry.get(field, '') or '').lower() for field in search_fields)
            for topic in topics
        )
    ]

# Asynchronous function that processes a single RSS feed
async def process_feed(session, url, topics, tokenizer, translate_flag, dest_lang, summarizer):
    
    from utils.logger_setup import logger
    
    try:
        content, source = await fetch_feed(session, url)
        if not content:
            return []

        # Parse the RSS content
        parsed = feedparser.parse(content)
        entries = filter_by_topic(filter_recent_articles(parsed.entries), topics)
        
        # Language detection
        if entries:
            sample_text = entries[0].get('title', '') + ' ' + entries[0].get('summary', '')
            detected_lang = detect(sample_text)
        else:
            detected_lang = 'en'

        # Determine batch size
        batch_size = 4
        return [
            result 
            for i in range(0, len(entries), batch_size)
            for result in await process_batch(
                entries[i:i+batch_size], 
                source, 
                tokenizer,
                translate_flag,
                dest_lang,
                summarizer,
                detected_lang
            )
        ]
    except Exception as e:
        logger.error(f"Error processing {url}: {str(e)[:200]}")
        return []