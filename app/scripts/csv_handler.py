import os
import csv
from pathlib import Path

import pandas as pd


def add_quotation_marks(directory: Path, export_file: Path):
    """Enclosed each item in csv file with double quotation mark"""

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

def merge_csv(directory: Path) -> pd.DataFrame:
    """Merge csvs into one dataframe"""
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
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            file_path = directory.joinpath(filename)
            os.remove(file_path)

    return merged_df

def generate_csv_from_dataframe(dataframe: pd.DataFrame, directory: Path):
    """Generate csv file from dataframe"""
    dataframe.to_csv(directory)




