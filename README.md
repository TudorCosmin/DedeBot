# DedeBot
RebelDot AI hackaton


## scraping_page Function

### Overview

This script is designed to scrape detailed product information (such as descriptions, prices, and technical specifications) from e-commerce websites, using Selenium WebDriver. The data is scraped for each product in a given category and saved into structured JSON files for further use or analysis.

### Features

- **Scrape product details:** For each product, it retrieves the description, price, and technical specifications (if available).
- **Multiple categories support:** The script can handle multiple categories, saving the scraped data into separate JSON files for each category.
- **Headless browsing:** It uses a headless Chrome browser to perform web scraping without opening a visible browser window.
- **Error handling:** Includes basic error handling to ensure that missing or unavailable product details do not cause the scraping process to fail.

### Requirements

To run the script, you need to have the following installed:
- Python 3.x
- Selenium
- ChromeDriver (automatically managed by `webdriver_manager`)
- Chrome Browser (in headless mode)

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/your-repository.git
    cd your-repository
    ```

2. Install the required Python dependencies:
    ```bash
    pip3 install -r requirements.txt
    ```

    This will install:
    - Selenium
    - `webdriver_manager` (for automatically managing the ChromeDriver)

3. Ensure you have a `data` folder with a `dedeman_products.json` file, containing basic product information in the following format:

    ```json
    {
        "Category1": [
            {"title": "Product1", "link": "URL1", "image": "imageURL1"},
            {"title": "Product2", "link": "URL2", "image": "imageURL2"}
        ],
        "Category2": [
            {"title": "Product3", "link": "URL3", "image": "imageURL3"}
        ]
    }
    ```

## Usage

Run the script by executing the following command:

```bash
python3 scraping_page.py
```

## clean_and_stringify_json_files Function

### Overview

This function cleans and formats JSON files in a specified folder by removing products that do not contain valid technical specifications. The cleaned data is then re-saved into the same JSON file with proper indentation.

### Parameters

- `data_folder` (str): Path to the folder containing the JSON files to clean.

### How it Works

1. Iterates through all `.json` files in the provided folder.
2. Loads each file and filters out products that lack the `technical_specs` field or where the field is empty.
3. Saves the cleaned data back into the file, formatted with an indentation of 4 spaces.

### Example Usage

```bash
python3 clean_and_stringify_json_files('data')
```
