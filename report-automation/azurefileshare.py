from azure.storage.fileshare import ShareDirectoryClient, ShareFileClient
from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError
from dotenv import load_dotenv
from os import getenv
import logging
import common
from datetime import datetime
from os import path


common.logger_config()


@common.log_function_call
def fileshare_client(fileshare_connstr, fileshare_name, dir, mode, file_path=''):
    """
    Establish file client base on which type of object we are interacting with
    """
    if mode == 'dir':
        dir_client = ShareDirectoryClient.from_connection_string(conn_str=fileshare_connstr,
                                                                       share_name=fileshare_name,
                                                                       directory_path=dir)
        return dir_client
    elif mode == 'file':
        if file_path == '':
            logging.critical('File path is not provded')
            raise ValueError('File path is not provded')
        try:
            file_client = ShareFileClient.from_connection_string(conn_str=fileshare_connstr,
                                                                 share_name=fileshare_name, directory_path=dir,
                                                                 file_path=file_path)
            return file_client
        except TypeError:
            logging.critical(TypeError)
    else:
        raise ValueError('Mode is not correct, please choose: "dir" or "file"')
    
@common.log_function_call
def create_subdir(dir_client, dir_path):
    """
    Create sub directory in azure file share
    """
    path_combine = ''
    for dir in dir_path.split():
        path_combine += f"{dir}/"
        if dir == '.':
            continue
        try:
            dir_client.create_subdirectory(path_combine)
        except ResourceExistsError as err:
            if err.status_code == '409':
                logging.warning(err.message)
                continue
    return True
    
@common.log_function_call
def download_file(dir_client: ShareDirectoryClient, cloud_source_file, local_dest_file):
    """
    Download from file from Azure file share
    """
    # TODO: check if file exist for download
    dest_path = common.check_path_exist(local_dest_file, generate_file_name=True)
    try:
        with open(cloud_source_file, "wb") as file_handle:
            data = dir_client.download_file()
            data.readinto(dest_path)
        return dest_path
    except Exception as err:
        logging.critical(err)
        return ''

@common.log_function_call
def upload_file(dir_client: ShareDirectoryClient, cloud_dest_file, local_source_file):
    """
    Upload local file to AzureFileShare
    """
    # Check subdir existence, if not create them
    dest_path_parts = path.split(cloud_dest_file)
    create_subdir(dir_client, dest_path_parts[0])
    # Upload the file to destination
    file_client = dir_client.create_file(cloud_dest_file)
    with open(local_source_file, "rb") as data:
        try:
            file_client.upload_file(data)
            return cloud_dest_file
        except ResourceExistsError as err:
            if err.status_code == '409':
                logging.warning(err.message)
                # Rename the file with timestamp appended
                new_cloud_dest_file = common.generate_file_name(cloud_dest_file)
                file_client = dir_client.create_file(new_cloud_dest_file)
                file_client.upload_file(data)
                return new_cloud_dest_file
            

if __name__ == '__main__':
    load_dotenv()
    dir_client = fileshare_client(getenv('SA_CONN_STR'), getenv('FS_NAME'), dir='./', 
                                  mode='dir')
    dir_path = './hihi2/aaa/cac'
    a = create_subdir(dir_client, dir_path)
    print('cac')
    