import os
import json

data_folder = 'Data'
# Function to check if technical_specs is empty, remove products if it is, and stringify the data
def clean_and_stringify_json_files(data_folder):
    # List all JSON files in the 'Data' folder
    for filename in os.listdir(data_folder):
        if filename.endswith('.json'):
            file_path = os.path.join(data_folder, filename)

            # Open and load the JSON file
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

            # Filter out products where technical_specs is empty
            cleaned_data = []
            for product in data:
                if 'technical_specs' in product and product['technical_specs'] != {}:
                    cleaned_data.append(product)

            # Convert cleaned data back to a JSON-formatted string
            json_string = json.dumps(cleaned_data, ensure_ascii=False, indent=4)

            # Save the cleaned and stringified data back to the file
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(json_string)
            
            print(f"Cleaned and stringified {filename}")

# Run the function to clean and stringify JSON files
clean_and_stringify_json_files(data_folder)

print("All JSON files have been cleaned, stringified, and saved.")