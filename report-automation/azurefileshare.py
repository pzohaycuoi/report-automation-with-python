from azure.storage.fileshare import ShareDirectoryClient, ShareFileClient
from dotenv import load_dotenv
from os import getenv
import logging
import common


common.logger_config()
load_dotenv() # delete after testing


@common.log_function_call
def fileshare_client(fileshare_connstr, fileshare_name, dir, mode):
    """

    """
    if mode == 'dir':
        dir_client = ShareDirectoryClient.from_connection_string(conn_str=fileshare_connstr,
                                                                       share_name=fileshare_name,
                                                                       directory_path=dir)
        return dir_client
    elif mode == 'file':
        file_client = ShareFileClient.from_connection_string(conn_str=fileshare_connstr,share_name=fileshare_name,directory_path=dir)
        return file_client
    else:
        raise ValueError('Mode is not correct, please choose: "dir" or "file"')
  

# def create_subdir(dir_client, dir_path, dir_name):
  # TODO implement logic for this


@common.log_function_call
def download_file(file_client: ShareFileClient, dest_file):
    # TODO download file from azure file share
    """
    Download from file from Azure file share
    """
    with open(dest_file, "wb") as file_handle:
    data = file_client.download_file()




file_client = azsfs.ShareDirectoryClient.from_connection_string(conn_str=getenv('SA_CONN_STR'), share_name=getenv('FS_NAME'),directory_path='./')