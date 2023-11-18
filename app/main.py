import os
import logging
import time
from pathlib import Path


from dotenv import load_dotenv

from selenium.webdriver.common.by import By

from scripts.extract_script import WebDriverContextManager
from scripts.zip_extract_handler import extract_zip
from scripts.csv_handler import (
    merge_csv,
    generate_csv_from_dataframe,
    add_quotation_marks,
)

load_dotenv()

WEBSITE = f'https://{os.getenv("USER")}:{os.getenv("PASS")}@hiringtest.openarchitectsk12.com'
DIRECTORY = Path(__file__).parents[1]

print(DIRECTORY)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    "[%(asctime)s %(levelname)s %(name)s:%(lineno)d] %(message)s"
)
file_handler = logging.FileHandler(DIRECTORY.joinpath('logs').joinpath('main.log'))
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


def main():

    with WebDriverContextManager() as driver:
        logger.info('this is sample message.')
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

    add_quotation_marks(
        DIRECTORY.joinpath('outputs'),
        DIRECTORY.joinpath('outputs').joinpath('oa_nwea_all.csv')
    )



if __name__ == '__main__':
    main()
