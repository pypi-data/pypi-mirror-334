"""Module for all methods related to Excel files."""

import pandas as pd


def concat_excel_files(files_list: list, output_file: str = "") -> pd.DataFrame:
    """Concatenate multiple Excel files with identical columns into one.

    Args:
        files_list (list of str): List of file paths to Excel files.
        output_file (str, optional): Path to save the concatenated result.

    Returns:
        pd.DataFrame: Combined DataFrame from all files with identical columns.
    """
    dataframes = []
    expected_columns = None

    for file in files_list:
        try:
            df = pd.read_excel(file)
            if expected_columns is None:
                expected_columns = list(df.columns)
            else:
                if list(df.columns) != expected_columns:
                    raise ValueError(f"File {file} has mismatched columns: {list(df.columns)}")

            # Append DataFrame if columns match
            dataframes.append(df)
        except Exception as e:
            raise Exception(f"Error processing file {file}: {e}")
    # Concatenate all DataFrames
    combined_df = pd.concat(dataframes, ignore_index=True)

    if output_file:
        combined_df.to_excel(output_file, index=False)

    return combined_df
