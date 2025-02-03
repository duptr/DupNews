from bs4 import BeautifulSoup
from transformers import AutoTokenizer
# Function that preprocesses the text
def preprocess_text(text, tokenizer):
    
    if not text or len(text.strip()) < 50:
        return None
    tokens = tokenizer.tokenize(text)
    return text if len(tokens) >= 15 else None
# Function that cleans HTML content
def clean_html(text):
    
    return BeautifulSoup(text, "html.parser").get_text()