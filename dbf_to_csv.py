import os
import pandas as pd
from datetime import date
from dbfread import DBF

def read_dbf(file_path,encoding):
    """
    Reads a DBF file and returns a pandas DataFrame.

    Args:
        file_path (str): The path to the DBF file.

    Returns:
        pd.DataFrame: Data from the DBF file as a DataFrame.
    """
    table = DBF(file_path, load=True, encoding=encoding, ignore_missing_memofile=True)
    df = pd.DataFrame(iter(table))
    return df

def write_csv(df, file_path,encoding):
    """
    Writes a DataFrame to a CSV file.

    Args:
        df (pd.DataFrame): The DataFrame to write to CSV.
        file_path (str): The path to save the CSV file.
    """
    df.to_csv(file_path, sep=';', encoding=encoding, index=False)

def main(dbf_folder, csv_folder, file_name,encoding):
    """
    Main function to handle the reading of a DBF file, checking if a corresponding
    CSV exists and is up-to-date, and writing to a CSV file if necessary.

    Args:
        dbf_folder (str): The directory path where the DBF files are located.
        csv_folder (str): The directory path where the CSV files should be saved.
        file_name (str): The base name of the file (without extension).
    """
    dbf_file_path = os.path.join(dbf_folder, f'{file_name}.dbf')
    csv_file_path = os.path.join(csv_folder, f'{file_name}.csv')

    if os.path.exists(csv_file_path):
        print(f"The file at {csv_file_path} exists.")
        modification_time = os.path.getmtime(csv_file_path)
        modification_date = date.fromtimestamp(modification_time)
        print(f"CSV modification date: {modification_date}")

        today_date = date.today()
        print(f"Today's date: {today_date}")
        
        if modification_date != today_date:
            # If the CSV file is not from today, update it from the DBF file.
            print(f"Updating the CSV file: {csv_file_path}")
            df = read_dbf(dbf_file_path,encoding)
            write_csv(df, csv_file_path,encoding)
    else:
        print(f"The file at {csv_file_path} does not exist. Creating new CSV.")
        df = read_dbf(dbf_file_path,encoding)
        write_csv(df, csv_file_path,encoding)

    # Load the DataFrame from the updated or new CSV file.
    df = pd.read_csv(csv_file_path, encoding=encoding, on_bad_lines='skip', sep=';')
    

if __name__ == "__main__":
    
    main(dbf_folder='path/to/dbf/folder', csv_folder='path/to/csv/folder', file_name='filename',encoding='latin-1')
