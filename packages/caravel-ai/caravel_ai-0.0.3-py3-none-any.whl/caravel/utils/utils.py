
def remove_nulls(data):
    """Recursively remove None values and empty dictionaries from a nested structure."""
    if isinstance(data, dict):
        # Recursively clean the dictionary
        cleaned_dict = {k: remove_nulls(v) for k, v in data.items() if v is not None}
        return remove_nulls(cleaned_dict) if cleaned_dict else None  # Remove empty dictionaries
    elif isinstance(data, list):
        # Recursively clean the list
        cleaned_list = [remove_nulls(v) for v in data if v is not None]
        return remove_nulls(cleaned_list) if cleaned_list else None  # Remove empty lists
    else:
        return data

# def remove_nulls(data):
#     """Recursively remove None values and empty dictionaries from a nested structure."""
#     if isinstance(data, dict):
#         cleaned_dict = {k: remove_nulls(v) for k, v in data.items() if v is not None}
#         return cleaned_dict if cleaned_dict else None  # Remove empty dictionaries
#     elif isinstance(data, list):
#         cleaned_list = [remove_nulls(v) for v in data if v is not None]
#         return cleaned_list if cleaned_list else None  # Remove empty lists
#     else:
#         return data