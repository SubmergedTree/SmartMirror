import logging

def setup_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler('logfile.log')
    handler.setLevel(logging.INFO) 
    formatter = logging.Formatter('%(filename)s - %(threadName)s - %(funcName)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)   
    logger.addHandler(handler)
    return logger

Logger = setup_logger()

    
