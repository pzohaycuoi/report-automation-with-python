import logging
import logging.config
import os.path


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
        logging.debug(f"Calling function {func.__name__} with args {args} and kwargs {kwargs}")
        result = func(*args, **kwargs)
        logging.debug(f"Function {func.__name__} returned {result}")
        return result
    return wrapper
