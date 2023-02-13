import logging
import logging.config
import os.path
import time
import inspect
from datetime import datetime


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


@log_function_call
def generate_file_name(file_path):
    """
    Genereate file name with timestamp appended,
    If arg is path, return a path with new file name
    Else if arg is a file name, return only new file name
    """
    if len(os.path.split(file_path)) > 1:
        file_name == '' and file_path != '':
        path_parts = os.path.split(file_path)
        dir_path = path_parts[0]
        file_name = path_parts[1]
        file_name_parts = os.path.splitext(file_name)
        time_stamp = datetime.now().strftime('%d%m%y-%H%M%S')
        new_file_name = f"{file_name_parts[0]}-{time_stamp}{file_name_parts[1]}"
        new_path = os.path.join(dir_path, new_file_name)
        return new_path
    else:
        file_name_parts = os.path.splitext(file_name)
        time_stamp = datetime.now().strftime('%d%m%y-%H%M%S')
        new_file_name = f"{file_name_parts[0]}-{time_stamp}{file_name_parts[1]}"
        return new_file_name


@log_function_call
def check_path_exist(path, generate_file_name=bool):
    """
    Check path existence
    mode = False: Check path existence only, return bool for result
    mode = True: Check path existence for file path, generate new file path with
    timestamp in filename part, return new path
    """
    if path.exists(path):
        if generate_file_name is True:
            new_path = generate_file_name(path)    
            return new_path
        elif generate_file_name is False:
            return True
    else:
        if generate_file_name is True:
            return path
        elif generate_file_name is False:
            return False