import os
import json

data_folder = 'data'
def clean_and_stringify_json_files(data_folder):
    """
    Cleans and formats JSON files in the specified folder by removing products 
    that do not contain valid technical specifications and re-saving the cleaned data.
    
    This function reads each JSON file in the given folder, filters out products 
    that either lack the 'technical_specs' field or have an empty dictionary for it, 
    and then re-saves the cleaned product data back into the original file in a 
    formatted JSON string with an indentation of 4 spaces.

    Parameters
    ----------
    data_folder : str
        Path to the folder containing JSON files to be cleaned.

    Returns
    -------
    None
        The function modifies and overwrites existing JSON files in place. 
        No value is returned.

    Workflow
    --------
    1. Iterate through all files in the specified folder.
    2. For each file ending with '.json', load its contents.
    3. Remove any product entries that do not have the 'technical_specs' field 
       or where 'technical_specs' is an empty dictionary.
    4. Convert the cleaned data back to a JSON string with proper formatting.
    5. Write the cleaned and formatted string back into the same file.

    Examples
    --------
    Assume that the 'Data' folder contains multiple JSON files, each representing 
    product data with fields such as 'title', 'price', 'technical_specs', etc.
    This function will clean and reformat the data within each file.
    
    >>> clean_and_stringify_json_files('data')
    
    The above call will clean all JSON files in the 'data' folder, removing products 
    without valid 'technical_specs', and save the cleaned data.

    """
    for filename in os.listdir(data_folder):
        if filename.endswith('.json'):
            file_path = os.path.join(data_folder, filename)

            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

            cleaned_data = []
            for product in data:
                if 'technical_specs' in product and product['technical_specs'] != {}:
                    cleaned_data.append(product)

            json_string = json.dumps(cleaned_data, ensure_ascii=False, indent=4)

            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(json_string)
            
            print(f"Cleaned and stringified {filename}")

clean_and_stringify_json_files(data_folder)

print("All JSON files have been cleaned, stringified, and saved.")