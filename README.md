# DedeBot


## Overview of the Project

This project implements a chatbot for Dedeman.ro, a leading construction materials and home improvement site in Romania. The chatbot is designed to assist users by providing human-like responses to free-form text queries, recommending relevant products based on user input and the chat history. Acting as a virtual product advisor, the chatbot offers personalized suggestions tailored to user preferences, project requirements, and specific needs.

In addition to product recommendations, the chatbot can also answer a comprehensive list of Frequently Asked Questions (FAQs), covering a wide range of topics related to products and services. Its goal is to create a friendly, interactive customer experience, combining useful product insights with natural, conversational responses.

The chatbot is focused on delivering helpful product recommendations, ensuring it remains responsive to the user's needs while avoiding questions unrelated to products, such as delivery schedules or store hours.

## Getting Started to run the chatbot

Install Python 3.9.

Create a virtual environment in the root folder:

```
python -m venv .venv
```
If Python 3 is not default on the system, the command may be `python3`.

Activate the virtual environment and install the dependencies:
```
source .venv/bin/activate
pip install -r requirements.txt
```

## Running the Chatbot

To start the chatbot, use the following command in the root directory:

```
chainlit run app.py
```


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




## scrape_links Function

### Overview

This script automates the process of scraping product details from the Dedeman website across multiple product categories using Selenium WebDriver. It captures product titles, links, images, and prices, and saves the data in a structured JSON file.

### Features

- **Scrape product details:** Retrieves essential information such as product title, price, image URL, and product link.
- **Scroll to load more content:** Automatically scrolls the webpage to load additional content and capture all available products.
- **Cookie handling:** Automatically accepts cookies if a popup is present.
- **Multiple categories support:** Can scrape multiple categories and multiple pages within each category.
- **Error handling:** Graceful handling of missing or incomplete product information without breaking the scraping process.

### Requirements

To run the script, you need the following:

- Python 3.x
- Selenium (for web automation)
- ChromeDriver (Ensure the path is correctly set for your operating system)
- Chrome Browser (in regular or headless mode)

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/your-repository.git
    cd your-repository
    ```

2. Install the required Python dependencies:

    ```bash
    pip install -r requirements.txt
    ```

    This will install:
    - Selenium
    - `webdriver_manager` (for automatically managing the ChromeDriver)

3. Ensure you have the **ChromeDriver** executable installed and set the correct path in the script.

### Usage

Run the script using:

```bash
python scrape_links.py
```

The script will scrape product details from multiple categories and save the results into a JSON file (`dedeman_products.json`).

### JSON Output Format

The output file (`dedeman_products.json`) will store product information in the following format:

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

### Error Handling
* If any errors occur during scraping, the script will log the error and continue scraping the remaining products or categories.
* A screenshot of any page where errors occur will be saved for debugging (`error_screenshot.png`).
