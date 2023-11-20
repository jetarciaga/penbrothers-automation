import os
import logging
from pathlib import Path
import threading

from dotenv import load_dotenv

from selenium.webdriver.common.by import By

from scripts.extract_script import WebDriverContextManager
from scripts.zip_extract_handler import extract_zip
from scripts.csv_handler import (
    merge_csv,
    generate_csv_from_dataframe,
    add_quotation_marks,
)
from scripts.sftp_upload_handler import SFTPServerClient

load_dotenv()

# start set logger block
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    '[%(asctime)s %(levelname)s %(name)s:%(lineno)d]: %(message)s'
)

file_handler = logging.FileHandler(
    Path(__file__).parent.joinpath('logs').joinpath('output.log')
)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
# end logger block

WEBSITE = f'https://{os.getenv("USER")}:{os.getenv("PASS")}@hiringtest.openarchitectsk12.com'
DIRECTORY = Path(__file__).parent

def main():

    sftp = SFTPServerClient(
        os.getenv('HOST'),
        os.getenv('PORT'),
        os.getenv('SFTP_USER'),
        os.getenv('SFTP_PASS')
    )

    logger.info('Connecting to web driver...')
    with WebDriverContextManager() as driver:

        driver.get(WEBSITE)

        element = driver.find_element(By.XPATH, ".//p[@id='verify-me']")
        code = element.text

        input_element = driver.find_element(By.XPATH, ".//input[@name='verify']")
        input_element.send_keys(code)

        download_button = driver.find_element(By.XPATH, ".//input[@value='Download']")
        download_button.click()

    extract_zip((DIRECTORY.joinpath('assets')))
    dataframe = merge_csv(DIRECTORY.joinpath('assets'))

    generate_csv_from_dataframe(
        dataframe,
        DIRECTORY.joinpath('outputs').joinpath('merged_data.csv')
    )

    path_to_merged_csv = add_quotation_marks(
        DIRECTORY.joinpath('outputs'),
        DIRECTORY.joinpath('outputs').joinpath('oa_nwea_all.csv')
    )

    sftp.connect()
    print('Uploading file please wait...')
    sftp.upload_files(f'/{path_to_merged_csv.stem}.csv', path_to_merged_csv)
    print('Uploading success!')
    sftp.disconnect()

    os.remove(DIRECTORY.joinpath('outputs').joinpath(path_to_merged_csv))



if __name__ == '__main__':
    main()
