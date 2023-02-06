import logging
import logging.config
import os.path
import time
import inspect


# Set default log configuration file path and log folder
cur_dir = os.path.dirname(__file__)
# default_log_config = cur_dir + '/../logconfig.ini'
default_log_config = 'C:/Users/namng/OneDrive/Code/Python/report-automation-with-python/logconfig.ini'


def logger_config(config_filepath=default_log_config):
    """
    Setup logging configuration
    """
    # check if provided file path exist
    if not os.path.exists(config_filepath):
        print(f"{config_filepath} not exist. Using default configs: {default_log_config}")
        logging.config.fileConfig(default_log_config)
    else:
        try:
            logging.config.fileConfig(config_filepath)
        except Exception as ex:
            print(ex)
            print(f"Error in Logging Configuration. Using default configs: {default_log_config}")
            logging.config.fileConfig(default_log_config)


def log_function_call(func):
    def wrapper(*args, **kwargs):
        file_path = inspect.getfile(func)
        file_name = os.path.basename(file_path)
        logging.debug(f"Calling function {func.__name__} - {file_name}")
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logging.debug(f"Function {func.__name__} - {file_name},run for {end_time-start_time} seconds")
        return result
    return wrapper
