from googletrans import Translator
import asyncio
# Create the Translator object
translator = Translator()
# Asynchronous function that translates a list of texts
async def translate_texts(texts, dest_lang, src_lang='en'):
    
    try:
        translations = await asyncio.to_thread(
            translator.translate,
            texts,
            src=src_lang,
            dest=dest_lang
        )
        return [t.text for t in translations]
    except Exception as e:
        from utils.logger_setup import logger
        logger.error(f"Translation error: {str(e)[:200]}")
        return ["Translation Error"] * len(texts)