import asyncio
import datetime
from processors.text_cleaner import clean_html, preprocess_text
from processors.text_translator import translate_texts
from utils.logger_setup import setup_logging

# Initialize the logger with the setup function
logger = setup_logging()

# Asynchronous function that processes a batch
async def process_batch(batch, source, tokenizer, translate_flag, dest_lang, summarizer, detected_lang='en'):
    try:
        # Lists to store valid texts and entries
        valid_texts = []
        valid_entries = []
        for item in batch:
            # HTML cleaning process
            cleaned_text = clean_html(item.get('summary', ''))
            # Preprocess the text and check if it is valid
            if preprocess_text(cleaned_text, tokenizer):
                valid_texts.append(cleaned_text)
                valid_entries.append(item)
        
        # If there are no valid texts, return an empty list
        if not valid_texts:
            return []

        # Calculate text lengths and determine dynamic maximum length
        text_lengths = [len(tokenizer.tokenize(text)) for text in valid_texts]
        dynamic_max_len = max(min(int(max(text_lengths)*0.6), 100), 30)
        
        # Perform summarization asynchronously
        batch_summaries = await asyncio.to_thread(
            summarizer,
            valid_texts,
            max_length=dynamic_max_len,
            min_length=max(int(dynamic_max_len*0.3), 15),
            truncation=True
        )

        # Dictionary to store translation data
        translated_data = {}
        # If translation flag is active and target language is different from detected language, perform translation
        if translate_flag and dest_lang != detected_lang:
            translate_inputs = [item['title'] for item in valid_entries] + [s['summary_text'] for s in batch_summaries]
            translations = await translate_texts(translate_inputs, dest_lang, detected_lang)
            translated_data = {
                "titles": translations[:len(valid_entries)],
                "summaries": translations[len(valid_entries):]
            }

        # Return processed data
        return [{
            "title": valid_entries[i]['title'],
            "summary": batch_summaries[i]['summary_text'],
            "source": source,
            "date": datetime.datetime(*valid_entries[i].published_parsed[:6]).strftime('%Y-%m-%d %H:%M:%S'),
            "link": valid_entries[i].get('link', ''),
            "translated_title": translated_data.get("titles", [""])[i] if translate_flag else "",
            "translated_summary": translated_data.get("summaries", [""])[i] if translate_flag else ""
        } for i in range(len(valid_entries))]
    
    # In case of error, log the error and return an empty list
    except Exception as e:
        logger.error(f"Batch processing error: {str(e)[:200]}")
        return []