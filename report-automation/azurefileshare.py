from azure.storage.fileshare import ShareDirectoryClient, ShareFileClient
from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError
from dotenv import load_dotenv
from os import getenv
import logging
import common


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
              
    def create_subdir(dir_client, dir_path):
        """
        Create sub directory in azure file share
        """
        path_split = dir_path.split()
        path_combine = ''
        for dir in path_split:
            if dir == '.':
                path_combine = f"{dir}/"
                continue
                dir_client.create_subdirectory(path_combine)
        
    @common.log_function_call
    def _download_file(file_client: ShareFileClient, dest_file):
        # TODO download file from azure file share
        """
        Download from file from Azure file share
        """
        with open(dest_file, "wb") as file_handle:
            data = file_client.download_file()
            
def create_subdir(dir_client, dir_path):
    """
    Create sub directory in azure file share
    """
    path_split = dir_path.split()
    path_combine = ''
    for dir in path_split:
        path_combine += f"{dir}/"
        if dir == '.':
            continue
        try:
            dir_client.create_subdirectory(path_combine)
        except ResourceExistsError as err:
            if err.status_code == '409':
                logging.info(err.message)
                continue
            

if __name__ == '__main__':
    load_dotenv()
    dir_client = fileshare_client(getenv('SA_CONN_STR'), getenv('FS_NAME'), dir='./', 
                                  mode='dir')
    file_client = fileshare_client(getenv('SA_CONN_STR'), getenv('FS_NAME'), dir='./', 
                                  mode='file', file_path='./bet-da-bong.xlsx')
    dir_path = './hihi2/aaa/cac'
    a = create_subdir(dir_client, dir_path)
    print('cac')
    