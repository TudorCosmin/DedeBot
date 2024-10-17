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

# Set up ChromeDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode for efficiency
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Ensure the 'Data' directory exists
os.makedirs('Data', exist_ok=True)

# Function to scrape the description, price, and technical specifications
def scrape_product_details(product_link, driver):
    product_details = {}
    
    try:
        driver.get(product_link)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.product-info-main')))
        
        # Extract description
        try:
            description_element = driver.find_element(By.CSS_SELECTOR, 'div.product.attribute.description')
            product_description = description_element.text.strip()
        except Exception as e:
            product_description = "Description not found"
            print(f"Error finding description: {e}")
        
        # Extract price
        try:
            price_element = driver.find_element(By.CSS_SELECTOR, '.price-wrapper .price')
            product_price = price_element.text.strip() if price_element else "Price not found"
        except Exception as e:
            product_price = "Price not found"
            print(f"Error finding price: {e}")

        # Scroll to technical specs and extract technical specifications
        try:
            spec_button = driver.find_element(By.CSS_SELECTOR, '#maincontent > div.columns > div > div.product-wrap-details > div.product-wrap-details-info > div.product.info.detailed > div > div:nth-child(1) > button')
            
            # Use JavaScript to ensure the spec button is fully visible
            driver.execute_script("arguments[0].scrollIntoView(true);", spec_button)
            # time.sleep(2)  # Give time for any animations

            # Use JavaScript to click the spec button directly
            driver.execute_script("arguments[0].click();", spec_button)
            # time.sleep(2)  # Allow the specs section to load
            
            # Click "Afiseaza mai multe specificatii" button (using class 'see-more')
            try:
                see_more_button = driver.find_element(By.CSS_SELECTOR, '#additional > button')
                if see_more_button.is_displayed() and see_more_button.is_enabled():
                    driver.execute_script("arguments[0].click();", see_more_button)
                    # time.sleep(2)  # Wait for additional content to load
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

# Function to scrape all product details for each category
def scrape_category_products(category_name, products, driver):
    detailed_products = []

    for product in products:
        product_link = product['link']
        print(f"Scraping product details for: {product['title']}")

        # Scrape detailed info for each product
        details = scrape_product_details(product_link, driver)
        product['description'] = details['description']
        product['price'] = details['price']  # You can choose to keep the old price or overwrite it
        product['technical_specs'] = details['technical_specs']

        detailed_products.append(product)

    # Save the detailed product data to a new JSON file for each category
    category_file_path = os.path.join('Data', f'{category_name}_scraped_data.json')
    with open(category_file_path, 'w', encoding='utf-8') as f:
        json.dump(detailed_products, f, ensure_ascii=False, indent=4)

    print(f"Scraped data for category '{category_name}' saved to '{category_file_path}'")

# Main function to scrape all categories and save the data
def scrape_all_categories(products_data, driver):
    for category_name, products in products_data.items():
        print(f"Scraping category: {category_name}")
        scrape_category_products(category_name, products, driver)

# Load your current JSON file with the basic product data
with open('Data/dedeman_products.json', 'r', encoding='utf-8') as f:
    products_data = json.load(f)


# Scrape details for all categories and save to individual files
scrape_all_categories(products_data, driver)

# Close the browser once scraping is done
driver.quit()

print("Detailed product scraping completed and saved for all categories.")
