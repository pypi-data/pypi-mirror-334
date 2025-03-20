# T_utils 📦

> **A Python package providing utility functions and reusable components to simplify interactions and enhance functionality across various applications.**

## 📑 Table of Contents
- [Overview](#overview)
- [Installation](#installation)
- [Usage Example](#usage-example)
- [API Documentation](#api-documentation)
- [License](#license)

## Overview
This package provides a base class for utility functions, along with commonly used modules and tools to enhance efficiency.
            
It also includes reusable components with built-in methods for frequent operations, making development more streamlined and consistent.

## Installation
```bash
  pip install t-utils-kit
```

## Usage Example
For detailed examples, please refer to our
            [quick start page](https://www.notion.so/thoughtfulautomation/T-utils-15ff43a78fa4803291eaccfc030d9c11).

### 
## API Documentation

---

## Const_utils
### Module: `t_utils.const_utils`

_Constants Module.

This module manages environment variables and imports for running RPA tasks.
It checks the environment to determine whether the process is running locally
or in production, and retrieves relevant work item data from Robocorp's WorkItems
API if not running locally.

Imports:
    os: Provides access to environment variables.
    WorkItems (from RPA.Robocorp.WorkItems): Used to interact with work items in Robocorp's RPA framework.
        Import is attempted and handled if not available.
_


---

## Datetime_utils
### Module: `t_utils.datetime_utils`

_Module for all methods related to datetime._

- **Class:** `Timer`
  > A Timer utility to track elapsed time and manage time-based operations.

    The Timer class provides methods and properties to check whether a duration has elapsed,
    reset the timer, and increment the duration dynamically.

    Attributes:
        duration (float): The total duration the timer runs before expiring.
        start (float): The time the timer was started or last reset.

    Methods:
        reset(): Resets the timer to start counting from the current time.
        increment(increment: Union[int, float] = 0): Increases the timer's duration by a specified amount.
        expired: Checks if the timer has expired.
        not_expired: Checks if the timer is still active.
        at: Returns the elapsed time since the timer started or was reset.
    
  - **Method:** `increment`
    > Increases the timer's duration by a specified amount.

        Args:
            increment (Union[int, float]): The number of seconds to add to the timer's duration. Defaults to 0.
        
  - **Method:** `reset`
    > Resets the timer to start counting from the current time.
- **Function:** `parse_datetime_from_string`
  > Parses a datetime object from a string using dateutil.parser.

    :param date_string: The string containing the datetime information.
    :return: A datetime object if parsing is successful, or None if parsing fails.
    

---

## Excel_utils
### Module: `t_utils.excel_utils`

_Module for all methods related to Excel files._

- **Function:** `concat_excel_files`
  > Concatenate multiple Excel files with identical columns into one.

    Args:
        files_list (list of str): List of file paths to Excel files.
        output_file (str, optional): Path to save the concatenated result.

    Returns:
        pd.DataFrame: Combined DataFrame from all files with identical columns.
    

---

## Exception_utils
### Module: `t_utils.exception_utils`

_Repeatable exception class._

- **Class:** `RepeatableExceptionCounter`
  > Keeps track of how many times the same exception is thrown in a row.
  - **Method:** `new_exception`
    > Handle a new exception. If it's the same as the previous one, increase the counter.

---

## File_utils
### Module: `t_utils.file_utils`

_Module for all methods related to folders and files handling._

- **Function:** `copy_file_to_folder`
  > Copies a single file to the specified directory.

    If the destination directory does not exist, it will be created automatically.
    This function ensures the integrity of the file by only copying it if the source
    is a valid file.

    Args:
        src_file (Union[str, Path]): The path to the source file to be copied.
        dst_folder (Union[str, Path]): The path to the target directory where the file will be copied.

    Returns:
        None

    Raises:
        FileNotFoundError: If the source file does not exist.
        OSError: If there is an issue creating the directory or copying the file.

    Example:
        copy_file_to_folder("example.txt", "backup_folder")
    
- **Function:** `copy_files_from_folder_to_folder`
  > Copies all files from the source directory to the destination directory.

    This function ensures that all files in the source directory are copied to the
    destination directory. If the destination directory does not exist, it will
    be created automatically. Subdirectories within the source directory are ignored.

    Args:
        src_folder (Union[str, Path]): The path to the directory containing the files to be copied.
        dst_folder (Union[str, Path]): The path to the target directory where files will be copied.
        extensions (Union[List[str], None]): File extension to filter by (e.g., [".txt"]). Optional.
        filter_word (Union[str, None]): A word that filenames should contain. Optional.

    Returns:
        None

    Raises:
        FileNotFoundError: If the source directory does not exist.
        PermissionError: If there are permission issues accessing the directories or files.

    Example:
        copy_files_from_folder_to_folder("source_folder", "destination_folder")
    
- **Function:** `create_folder_if_not_exist`
  > Creates a directory if it does not already exist.

    This function checks whether the specified directory exists. If not, it creates
    the directory along with any necessary intermediate directories.

    Args:
        folder_path (Union[str, Path]): The path of the folder to check or create.

    Returns:
        None
    
- **Function:** `create_or_clean_folder`
  > Creates a new folder or cleans an existing folder.

    This function checks if the specified directory exists:
    - If it exists, it removes all its contents (files and subdirectories).
    - If it does not exist, it creates the directory.

    Args:
        folder_path (Path): Path to the directory to be created or cleaned.

    Returns:
        None

    Raises:
        OSError: If there is an issue deleting files or creating the directory.

    Example:
        create_or_clean_folder(Path("output_folder"))
    
- **Function:** `create_time_based_file_name`
  > Create a file name with the current date time.

    Args:
        base_name (str): the file name
        extension (str): the file type
        date_formate (str): the format of datetime default value is %Y%m%d_%H%M%S

    Returns:
        str: The generated filename
    
- **Function:** `delete_file`
  > Delete folder.

    Args:
        file_path (Path): Path to file to be deleted.
    
- **Function:** `delete_folder`
  > Delete folder.

    Args:
        folder_path (Path): Path to folder
    
- **Function:** `is_file_open`
  > Verifies if given file is opened by other program.

    Args:
        file_path Union[str, Path]: File system path.

    Returns:
        Boolean.
    
- **Function:** `is_folder_empty`
  > Check if the given folder is empty, excluding the '__pycache__' directory.

    Args:
        file_path (Union[str, Path]): The path of the folder to check.

    Returns:
        bool: True if the folder is empty (ignoring '__pycache__'), False otherwise.

    Raises:
        ValueError: If the provided path does not exist or is not a directory.
    
- **Function:** `list_files_in_folder`
  > List all files in a directory with optional filters for extension, word containment, and regex.

    Args:
        folder_path (Union[str, Path]): Path to the directory to list files from.
        extensions (List[str]): File extensions to filter by (e.g., [".txt", ".csv"]). Optional.
        filter_word (Union[str, None]): A word that filenames should contain. Optional.
        regex (Union[str, None]): A regex pattern that filenames should match. Optional.
        recursive (bool): Whether to include files in subdirectories recursively. Defaults to True.

    Returns:
        List[str]: A list of file paths matching the specified criteria.
    
- **Function:** `move_file_to_folder`
  > Moves a file from one location to another.

    If the destination directory does not exist, it is created automatically.
    If a file already exists at the destination path, it will be overwritten.

    Args:
        src_path (str): The full path to the source file to be moved.
        dst_path (str): The full path to the destination file.

    Returns:
        None

    Raises:
        FileNotFoundError: If the source file does not exist.
        Exception: For any other errors during the move operation.

    Example:
        move_file("source_folder/example.txt", "destination_folder/example.txt")
    
- **Function:** `move_files_from_folder_to_folder`
  > Moves all files from the source directory to the destination directory.

    This function ensures that all files in the source directory are moved to the
    destination directory. If the destination directory does not exist, it will
    be created automatically. Subdirectories within the source directory are ignored.

    Args:
        src_folder (Union[str, Path]): The path to the directory containing the files to be moved.
        dst_folder (Union[str, Path]): The path to the target directory where files will be moved.
        extensions (Union[List[str], None]): File extension to filter by (e.g., [".txt"]). Optional.
        filter_word (Union[str, None]): A word that filenames should contain. Optional.
        recursive (bool): Whether to include files in subdirectories recursively. Defaults to True.

    Returns:
        None

    Raises:
        FileNotFoundError: If the source directory does not exist.
        PermissionError: If there are permission issues accessing the directories or files.

    Example:
        move_files_from_folder_to_folder("source_folder", "destination_folder")
    
- **Function:** `rename_file`
  > Rename the downloaded file with the new filename.

    Args:
        original_file (Union[str, Path]): The path to the original file.
        new_filename (str): The new filename.

    Returns:
        str: The path to the renamed file.
    
- **Function:** `wait_until_file_exist`
  > Waits until a file with the specified name or matching a regex pattern is found in a directory.

    This function monitors a directory for the presence of a file matching the specified
    `file_identifier`. It waits up to `wait_time` seconds and returns the full path of
    the matched file if found. If no file is found within the timeout, it raises an AssertionError.

    Args:
        folder_path (Union[Path, str]): The path to the directory to monitor.
        file_identifier (str): The name of the file or a regex pattern to match.
        is_regex (bool, optional): Whether to treat `file_identifier` as a regex pattern. Defaults to False.
        wait_time (int, optional): Maximum time to wait (in seconds). Defaults to 30.

    Returns:
        str: The full path of the matched file.

    Raises:
        AssertionError: If the file is not found within the specified wait time.

    Example:
        # Wait for a specific file:
        wait_until_file_downloads("/downloads", "example.txt")

        # Wait for a file matching a regex pattern:
        wait_until_file_downloads("/downloads", r"^report_\\d{4}\\.csv$", is_regex=True)
    
- **Function:** `wait_until_file_is_written`
  > Wait until a file is no longer being written to.

    Args:
        file_path (Union[str, Path]): The path to the file.
        wait_time (int): The maximum time to wait in seconds. Default is 10.

    Returns:
        bool: True if the file is no longer being written to, False otherwise.
    
- **Function:** `zip_files`
  > Creates a ZIP archive containing the specified list of files.

    Args:
        output_zip (Union[str, Path]): The file path where the ZIP output will be created.
        files_list (List[str]): A list of file paths to include in the ZIP archive.
        zip_filename (str): The name of the ZIP file to be created.

    Returns:
        None

    Raises:
        FileNotFoundError: If any file in the files_list does not exist.
        OSError: If there is an issue creating the ZIP file or writing to it.

    Example:
        zip_files("archive.zip", ["file1.txt", "file2.txt", "file3.txt"])

    Notes:
        - Each file is added to the ZIP archive with its basename (i.e., without directory structure).
        - If the target archive path already exists, it will be overwritten.
    
- **Function:** `zip_folder`
  > Create a zip archive for the entire folder with optional filters for files.

    Args:
        folder_path (Union[str, Path]): Path to the folder to zip.
        output_zip (Union[str, Path]): Path to save the resulting zip file. Defaults to "output.zip".
        extensions (List[str]): List of file extensions to include in the zip. Defaults to None (no filtering).
        contains_filter (str): Filter to include only files whose names contain this string. Defaults to "" (no filter).
        recursively (bool): Whether to include files in subdirectories recursively. Defaults to True.
        regex (Union[str, None]): A regex pattern that filenames should match. Optional.

    Returns:
        Path: The path to the created zip file.
    

---

## Logger_utils
### Module: `t_utils.logger_utils`

_Module for logger._

- **Class:** `CustomFormatter`
  > CustomFormatter class.
  - **Method:** `format`
    > Override 'format' method.

---

## Num_utils
### Module: `t_utils.num_utils`

_Module for all methods related to numbers._

- **Function:** `parse_numbers_from_string`
  > Parses numbers from a given string, handling integers, floats, and numbers with commas as decimal points.

    This function removes non-numeric characters (except for commas, dots, and hyphens), replaces commas
    between digits with periods (to handle decimal numbers in some locales), and extracts both integers
    and floating-point numbers from the string.

    Args:
        input_string (str): The input string containing potential numbers to be parsed.

    Returns:
        List[Union[int, float]]: A list of parsed numbers (either integers or floats).

    Example:
        input_string = "The price is 10.5, and -3.2 was deducted, also 2,000 is a large number."
        parse_numbers_from_string(input_string)
        # Returns: [10.5, -3.2, 2000]
    

---

## Robocloud_utils
### Module: `t_utils.robocloud_utils`

_Constants Module._


---

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
