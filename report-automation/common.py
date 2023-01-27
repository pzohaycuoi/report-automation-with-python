import logging
import logging.config
import os.path


# Set default log configuration file path and log folder
cur_dir = os.path.dirname(__file__)
default_log_config = cur_dir + '/../logconfig.ini'


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
