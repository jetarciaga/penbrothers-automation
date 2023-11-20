import os
from pathlib import Path
import logging

from dotenv import load_dotenv
import paramiko

load_dotenv()

hostname = os.getenv('HOST')
port = os.getenv('PORT')
username = os.getenv('SFTP_USER')
password = os.getenv('SFTP_PASS')

# start set logger block
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    '[%(asctime)s %(levelname)s %(name)s:%(lineno)d]: %(message)s'
)

file_handler = logging.FileHandler(
    Path(__file__).parents[1].joinpath('logs').joinpath('output.log')
)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
# end logger block


class SFTPServerClient:
    """SFTP Client Object."""
    def __init__(self, hostname, port, username, password):
        self.__hostname = hostname
        self.__port = port
        self.__username = username
        self.__password= password
        self.__SSH_CLIENT = paramiko.SSHClient()

    def connect(self):
        logger.info('Connecting to SSH Client')
        try:
            self.__SSH_CLIENT.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.__SSH_CLIENT.connect(
                hostname = self.__hostname,
                port = self.__port,
                username  = self.__username,
                password = self.__password
            )
        except Exception as e:
            logger.exception('Encountered some error')
            raise Exception(e)
        else:
            logger.info(f"Connected to server {self.__hostname}:{self.__port} as {self.__username}" )


    def disconnect(self):
        self.__SSH_CLIENT.close()
        logger.info(f"{self.__username} is disconnected to server "
              f"{self.__hostname}:{self.__port}")

    def get_list_of_files(self, remote_path):
        logger.info('Connecting to sftp...')
        sftp_client = self.__SSH_CLIENT.open_sftp()
        try:
            print(f"list of files {sftp_client.listdir(remote_path)}")
        except Exception as e:
            logger.exception("Error while retrieving list of files")
            raise Exception(e)
        finally:
            sftp_client.close()

    def upload_files(self, remote_file_path, local_file_path):
        logger.info(f"Uploading file {local_file_path} to {remote_file_path}")
        sftp_client = self.__SSH_CLIENT.open_sftp()
        try:
            sftp_client.put(local_file_path, remote_file_path)
            logger.info(f"Uploading file {local_file_path} to {remote_file_path} successful...")
        except Exception:
            logger.exception(f'File {local_file_path} was not found on the local system')
        finally:
            sftp_client.close()

