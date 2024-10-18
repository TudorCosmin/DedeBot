import json
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = Options()
chrome_options.add_argument("--headless")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

os.makedirs('data', exist_ok=True)

def scrape_product_details(product_link, driver):
    """
    Scrapes detailed product information from the product page.

    Parameters
    ----------
        product_link: str
            The URL of the product page.
        driver :webdriver.Chrome
            The Selenium WebDriver instance.

    Returns
    -------
        dict
            a dictionary containing the product description, price, and technical specifications.
    """
    product_details = {}
    
    try:
        driver.get(product_link)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.product-info-main')))
        
        try:
            description_element = driver.find_element(By.CSS_SELECTOR, 'div.product.attribute.description')
            product_description = description_element.text.strip()
        except Exception as e:
            product_description = "Description not found"
            print(f"Error finding description: {e}")
        
        try:
            price_element = driver.find_element(By.CSS_SELECTOR, '.price-wrapper .price')
            product_price = price_element.text.strip() if price_element else "Price not found"
        except Exception as e:
            product_price = "Price not found"
            print(f"Error finding price: {e}")
        
        # Scrape technical specifications
        try:
            spec_button = driver.find_element(By.CSS_SELECTOR, (
            '#maincontent > div.columns > div > div.product-wrap-details > '
            'div.product-wrap-details-info > div.product.info.detailed > '
            'div > div:nth-child(1) > button'
            ))
            driver.execute_script("arguments[0].scrollIntoView(true);", spec_button)
            driver.execute_script("arguments[0].click();", spec_button)
            
            # Click "Afiseaza mai multe specificatii" button
            try:
                see_more_button = driver.find_element(By.CSS_SELECTOR, '#additional > button')
                if see_more_button.is_displayed() and see_more_button.is_enabled():
                    driver.execute_script("arguments[0].click();", see_more_button)
                    print("Clicked 'See more' button.")
            except Exception as e:
                print(f"Error clicking 'See more' button: {e}")

            # Extract technical specifications
            specs_table = driver.find_element(By.CSS_SELECTOR, 'table#product-attribute-specs-table')
            specs_rows = specs_table.find_elements(By.CSS_SELECTOR, 'tr')

            technical_specs = {}
            for row in specs_rows:
                spec_name = row.find_element(By.CSS_SELECTOR, 'th').text.strip()
                spec_value = row.find_element(By.CSS_SELECTOR, 'td').text.strip()
                technical_specs[spec_name] = spec_value

        except Exception as e:
            technical_specs = {}
            print(f"Error finding technical specifications: {e}")
        
        product_details = {
            'description': product_description,
            'price': product_price,
            'technical_specs': technical_specs
        }
    except Exception as e:
        print(f"Error scraping product details: {e}")
    
    return product_details

def scrape_category_products(category_name, products, driver):
    """
    Scrapes detailed information for each product in a given category.

    Parameters
    ----------
        category_name: str
            The name of the product category (e.g., "Saws", "Hammers" etc.)
        products: list
            A list of dictionaries containing basic product information (e.g., title, link).
        driver: webdriver.Chrome
            The Selenium WebDriver instance.

    Returns
    -------
        None
            The scraped details are saved into a JSON file for the category.
    """
    detailed_products = []

    for product in products:
        product_link = product['link']
        print(f"Scraping product details for: {product['title']}")

        details = scrape_product_details(product_link, driver)
        product['description'] = details['description']
        product['price'] = details['price']
        product['technical_specs'] = details['technical_specs']

        detailed_products.append(product)

    category_file_path = os.path.join('data', f'{category_name}_scraped_data.json')
    with open(category_file_path, 'w', encoding='utf-8') as f:
        json.dump(detailed_products, f, ensure_ascii=False, indent=4)

    print(f"Scraped data for category '{category_name}' saved to '{category_file_path}'")

def scrape_all_categories(products_data, driver):
    """
    Scrapes detailed information for all product categories provided in the input data.

    This function iterates through each category in the input product data, scrapes detailed
    information (such as description, price, and technical specifications) for each product, 
    and saves the results into separate JSON files named after each category.

    Parameters
    ----------
        products_data: dict
            A dictionary containing product categories as keys and lists of 
            product data (title, link) as values.
                Example format: 
                    {
                    "Category1": [{"title": "Product1", "link": "URL1"}, ...],
                    "Category2": [{"title": "Product2", "link": "URL2"}, ...]
                    }
        driver: webdriver.Chrome
            The Selenium WebDriver instance used to interact with web pages.

    Returns
    -------
        None
            The function saves the scraped details into JSON files for each category. 
            Each file is stored in the 'data' directory with the name format '{category_name}_scraped_data.json'.

    Workflow
    --------
        1. Iterate through each category in `products_data`.
        2. For each category, pass its list of products and category name to `scrape_category_products`.
        3. The `scrape_category_products` function handles the individual product scraping and file saving.
        4. Print the status of each category scraping process to the console.
    """
    for category_name, products in products_data.items():
        print(f"Scraping category: {category_name}")
        scrape_category_products(category_name, products, driver)

products_json_path = 'scraping/dedeman_products_suruburi.json'
with open(products_json_path, 'r', encoding='utf-8') as f:
    products_data = json.load(f)

scrape_all_categories(products_data, driver)

driver.quit()

print("Detailed product scraping completed and saved for all categories.")
