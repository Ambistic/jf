def dump_dict_to_string(**kwargs) -> str:
    """
    Dumps a dictionary (inferred from kwargs) into a formatted string with keys in alphabetical order.
    
    :param kwargs: Dictionary with keys as strings and values as int or float.
    :return: Formatted string in the pattern <key><value>_<key2><value2>_...
    """
    for key, value in kwargs.items():
        if not isinstance(value, (int, float)):
            raise ValueError(f"Invalid value for key '{key}': Expected an int or float, got {type(value).__name__}")
    
    sorted_items = sorted(kwargs.items())  # Sort dictionary items by key
    formatted_pairs = [f"{key}{round(value, 6)}" for key, value in sorted_items]
    return "_".join(formatted_pairs)
