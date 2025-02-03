import asyncio
import aiohttp
import multiprocessing
import torch
import os
from utils.config_loader import load_config
from utils.logger_setup import setup_logging
from utils.model_initializer import initialize_models
from processors.rss_feed_processor import process_feed
from utils.database import save_news
from utils.database import get_all_news

# Main asynchronous function
async def main():
    # Initialize the logger with the setup function
    logger = setup_logging()
    
    try:
        # Ask the user if they want to translate the news
        translate_choice = input("Do you want to translate the news? (Y/N): ").strip().lower()
        translate_flag = translate_choice == 'y'
        dest_lang = 'tr'
        
        # If translation is desired, get the target language code
        if translate_flag:
            dest_lang = input("Please enter the target language code (e.g., tr, fr, de): ").strip().lower()
            if len(dest_lang) != 2:
                print("Invalid language code! Default Turkish (tr) will be used.")
                dest_lang = 'tr'

        # Determine the device (use GPU if available, otherwise CPU)
        device = "cuda:0" if torch.cuda.is_available() else "cpu"
        logger.info(f"Working environment: {device}")
        
        # Initialize the models
        summarizer, tokenizer = initialize_models(device)
        # Load the configuration file
        config = load_config()
        
        # Create an asynchronous HTTP session
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(limit=100),
            timeout=aiohttp.ClientTimeout(total=30)
        ) as session:
            # Create tasks for RSS URLs
            tasks = [
                process_feed(
                    session, 
                    url, 
                    config['topics'], 
                    tokenizer,
                    translate_flag,
                    dest_lang,
                    summarizer
                ) for url in config['rss_urls']
            ]
            # Run all tasks asynchronously and collect the results
            results = await asyncio.gather(*tasks)
            # Combine all articles into a single list
            all_articles = [article for sublist in results for article in sublist]
        # If there are articles, write them to a file
        if all_articles:
            output_path = os.path.join(os.path.dirname(__file__), "NEWS.txt")
            with open(output_path, 'w', encoding='utf-8') as f:
                for idx, article in enumerate(all_articles, 1):
                    f.write(f"\n=== News {idx} ===")
                    f.write(f"\nTitle: {article['title']}")
                    f.write(f"\nSummary: {article['summary']}")
                    f.write(f"\nDate: {article['date']}")
                    f.write(f"\nLink: {article['link']}\n")
                    f.write(f"\nTranslation:\n")
                    if translate_flag:
                        f.write(f"{dest_lang.upper()} Title: {article['translated_title']}\n")
                        f.write(f"{dest_lang.upper()} Summary: {article['translated_summary']}\n")
                    f.write(f"\nSource: {article['source']}")
                    f.write("\n" + "="*50 + "\n")

                    # Save the news to the database
                    save_news(
                        title=article['title'],
                        link=article['link'],
                        summary=article['summary'],
                        date=article['date'],
                        translation_title=article.get('translated_title', ''),
                        translation_summary=article.get('translated_summary', ''),
                        source=article['source']
                    )

            # Log the number of articles found and print the output file path
            logger.info(f"{len(all_articles)} news found!")
            print(f"File is ready!")
        else:
            # Log and print that no new news was found
            logger.info("Didn't find any new news!")
            print("Didn't find any new news!")
            
    except Exception as e:
        # Log the error and print an error message
        logger.exception(f"Critical error: {str(e)[:200]}")
        print("An unexpected error occurred! Look log file for details.")


news = get_all_news()
for n in news:
    print(n)

# Run the main function
if __name__ == '__main__':
    multiprocessing.freeze_support()
    asyncio.run(main())