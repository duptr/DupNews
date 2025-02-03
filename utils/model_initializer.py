from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# Function that initializes the model and tokenizer
def initialize_models(device):
    # Determine the name of the model to be used
    model_name = "facebook/bart-large-cnn"
    # Load the model and move it to the specified device (CPU or GPU)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(device)
    # Load the tokenizer and set the maximum length
    tokenizer = AutoTokenizer.from_pretrained(model_name, model_max_length=1024)
    # Create the summarization pipeline
    summarizer = pipeline(
        "summarization",
        model=model,
        tokenizer=tokenizer,
        device=0 if device == "cuda:0" else -1,
        max_length=100,
        min_length=30,
        num_beams=4,
        length_penalty=2.0,
        no_repeat_ngram_size=3,
    )
    # Return the summarizer and tokenizer
    return summarizer, tokenizer