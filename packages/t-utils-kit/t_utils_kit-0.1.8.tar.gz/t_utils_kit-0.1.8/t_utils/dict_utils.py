"""Module for all methods related to dictionaries."""


def check_nested_keys(data: dict, keys: list) -> bool:
    """Checks if all keys are present in the nested dictionary.

    Args:
        data (dict): The nested dictionary to check.
        keys (list): A list of keys representing the path to check in the dictionary.

    Returns:
        bool: True if all keys are present in the nested dictionary, False otherwise.
    """
    if not isinstance(data, dict):
        raise ValueError("The given data should be a dictionary.")
    if not isinstance(keys, list):
        raise ValueError("The keys should be provided as a list.")

    current_dict = data
    for key in keys:
        if not isinstance(current_dict, dict):
            return False
        try:
            current_dict = current_dict[key]
        except KeyError:
            return False
    return True
