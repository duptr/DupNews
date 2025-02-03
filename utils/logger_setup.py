import os
import logging

# Function that configures logging
def setup_logging():
    """Logging configuration"""
    # Determine the path of the log file
    log_file = os.path.join(os.path.dirname(__file__), "news_summarizer.log")
    # Configure logging settings
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    # Return the logger object
    return logging.getLogger(__name__)

# Create a global logger object
logger = setup_logging()
