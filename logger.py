import logging

def setup_logger():
    print("setup logger")
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler('logfile.log')
    handler.setLevel(logging.INFO) 
    formatter = logging.Formatter('%(levelname)s - (filename)s - %(threadName)s - %(funcName)s - %(message)s')
    handler.setFormatter(formatter)   
    logger.addHandler(handler)
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(formatter)
    logger.addHandler(consoleHandler)
    return logger

Logger = setup_logger() # TODO: Refactor to logger instead of Logger

    
