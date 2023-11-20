import os
import csv
from pathlib import Path
import logging

import pandas as pd

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

def add_quotation_marks(directory: Path, export_file: Path):
    """Enclosed each item in csv file with double quotation mark"""
    logger.info('Adding double quotes...')

    read_file = directory.joinpath([
        filename  for filename in os.listdir(directory) \
            if filename.endswith('.csv')
        ][0])

    with open(read_file, 'r', encoding='utf-8') as infile, \
        open(export_file, 'w', encoding='utf-8') as outfile:

        csv_read = csv.reader(infile)
        csv_writer = csv.writer(outfile, quoting=csv.QUOTE_ALL)

        for row in csv_read:
            csv_writer.writerow(row)
    logger.info('Removing old unquoted files...')
    os.remove(read_file)
    return export_file

def merge_csv(directory: Path) -> pd.DataFrame:
    """Merge csvs into one dataframe"""
    logger.info('Merging CSV files...')
    merged_df = pd.DataFrame()

    # loop through csv files in directory
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            file_path = directory.joinpath(filename)
            current_df = pd.read_csv(file_path)
            current_df['filename'] = filename
            current_df.to_csv(directory.joinpath(filename))  # overwrite csv add filename column
            merged_df = pd.concat([merged_df, current_df], ignore_index=True)

    # remove source files
    logger.info('Removing source files...')
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            file_path = directory.joinpath(filename)
            os.remove(file_path)

    return merged_df

def generate_csv_from_dataframe(dataframe: pd.DataFrame, directory: Path):
    """Generate csv file from dataframe"""
    logger.info('Generating csv files...')
    dataframe.to_csv(directory)




