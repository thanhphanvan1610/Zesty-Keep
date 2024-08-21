import logging

def setup_logging(log_file='app.log', log_level=logging.INFO):
    """Set up logging configuration."""
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),  # Log to console
            logging.FileHandler(log_file)  # Log to file
        ]
    )