import os
import logging
from pathlib import Path
from zipfile import ZipFile

DIRECTORY = Path(__file__).parents[2].joinpath('assets')

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

def extract_zip(file_path: Path):
    try:
        logger.info('Extracting zip file...')
        zip_file = os.listdir(file_path)[-1]
        file_to_extract = file_path.joinpath(zip_file)

        with ZipFile(file_to_extract, 'r') as zObject:
            zObject.extractall(file_path)

        os.remove(file_to_extract)
        return file_path

    except Exception as e:
        logger.exception(f'Something went wrong: {e}')

