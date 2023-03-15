from os import getenv, path
import logging
import common
from azure.storage.fileshare import ShareDirectoryClient, ShareFileClient
from azure.core.exceptions import ResourceExistsError
from dotenv import load_dotenv


common.logger_config()


@common.log_function_call
def fileshare_client(fileshare_connstr, fileshare_name, directory,
                     mode, file_path=''):
    """
    Establish file client base on which type of object we are interacting with
    """
    if mode == 'dir':
        dir_client = ShareDirectoryClient.from_connection_string(
            conn_str=fileshare_connstr, share_name=fileshare_name,
            directory_path=directory)
        return dir_client

    if mode == 'file':
        if file_path == '':
            logging.critical('File path is not provded')
            raise ValueError('File path is not provded')
        try:
            file_client = ShareFileClient.from_connection_string(
                conn_str=fileshare_connstr, share_name=fileshare_name,
                directory_path=directory, file_path=file_path)
            return file_client
        except TypeError as err:
            logging.critical(TypeError)
            raise err
    else:
        raise ValueError('Mode is not correct, please choose: "dir" or "file"')


@common.log_function_call
def create_subdir(dir_client, dir_path):
    """
    Create sub directory in azure file share
    """
    path_combine = ''
    for directory in dir_path.split('/'):
        path_combine += f"{directory}/"
        if path_combine == './':
            continue
        try:
            dir_client.create_subdirectory(path_combine)
        except ResourceExistsError as err:
            if err.status_code == '409':
                logging.warning(err.message)
                continue
    return path_combine


@common.log_function_call
def download_file(cloud_source_file, local_dest_file):
    """
    Download from file from Azure file share
    """
    # TODO: check if file exist for download
    dest_path = common.check_path_exist(local_dest_file, avoid_duplicate=True)
    file_client = fileshare_client(
        getenv('SA_CONN_STR_2'), getenv('FS_NAME'), directory='./',
        mode='file', file_path=cloud_source_file)
    try:
        with open(dest_path, 'w+b') as file_handle:
            data = file_client.download_file()
            data.readinto(file_handle)
        return dest_path
    except Exception as err:
        raise err


@common.log_function_call
def upload_file(dir_client: ShareDirectoryClient, cloud_dest_file,
                local_source_file):
    """
    Upload local file to AzureFileShare
    """
    # Check subdir existence, if not create them
    dest_path_parts = path.split(cloud_dest_file)
    create_subdir(dir_client, dest_path_parts[0])
    # Upload the file to destination
    file_client = fileshare_client(getenv('SA_CONN_STR_2'),
                                   getenv('FS_NAME'),
                                   directory='./', mode='file',
                                   file_path=cloud_dest_file)
    # Check if local_source_file exist
    real_local_filepath = common.convert_to_realpath(local_source_file)
    if common.check_path_exist(real_local_filepath):
        with open(real_local_filepath, "rb") as data:
            try:
                # TODO: ISSUES: upload file using ShareFileClient does not
                # throw 409 Which make the file overwritten
                file_client.upload_file(data)
                return cloud_dest_file
            except ResourceExistsError as err:
                if err.status_code == '409':
                    logging.warning(err.message)
                    # Rename the file with timestamp appended
                    new_cloud_dest_file = common.generate_file_name(
                        cloud_dest_file)
                    file_client = dir_client.create_file(new_cloud_dest_file)
                    file_client.upload_file(data)
                    return new_cloud_dest_file
    else:
        logging.error("local source file not exist: %s", real_local_filepath)
        # TODO: do something here


if __name__ == '__main__':
    load_dotenv()
    client = fileshare_client(getenv('SA_CONN_STR'), getenv('FS_NAME'),
                              directory='./', mode='dir')
    cloud_dir_path = "./EA/test/12345678/2022/12/"
    local_filepath = '../template/Book1.xlsx'
    cloud_filepath = "./EA/test/12345678/2022/12/test.xlsx"
    cloud_new_dir_path = upload_file(client, cloud_filepath, local_filepath)
    download_file_fileshare = download_file(
        getenv('CLOUD_TEMPLATE_PATH'), '../template/test.xlsx')
    print(cloud_new_dir_path)
