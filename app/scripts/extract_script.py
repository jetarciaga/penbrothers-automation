import os
from pathlib import Path
import logging

from selenium import  webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FFService

DIRECTORY = Path(__file__).parents[1]
DRIVER_DIRECTORY = DIRECTORY.joinpath('drivers')
FIREFOX_DRIVER = DRIVER_DIRECTORY.joinpath('geckodriver.exe')

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


class WebDriverContextManager:
    """Driver object"""
    logger.info('Instantiating web driver...')
    def __enter__(self):
        try:
            self.options = Options()
            self.options.add_argument('-headless')
            self.options.set_preference("browser.download.folderList", 2)
            self.options.set_preference("browser.download.manager.showWhenStarting", False)
            self.options.set_preference("browser.download.dir", str(DIRECTORY.joinpath('assets')))
            self.options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-gzip")
            self.driver = webdriver.Firefox(
                service=FFService(executable_path=FIREFOX_DRIVER), options=self.options
            )  # instantiate Browser
            return self.driver
        except Exception:
            logger.exception('Web driver failed to instantiate.')


    def __exit__(self, exc_type, exc_value, traceback):
        logger.info('Closing web driver...')
        self.driver.quit()

