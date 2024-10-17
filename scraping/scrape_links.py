from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import json
import time

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-extensions")

# Set up the WebDriver (adjust path to the chromedriver executable)
service = Service(executable_path='C:\\Users\\Voic\\Downloads\\chromedriver-win64\\chromedriver.exe')
driver = webdriver.Chrome(service=service, options=chrome_options)

# Function to accept cookies manually if needed
def accept_cookies():
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler')))
        cookie_button = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
        cookie_button.click()
        time.sleep(2)  # Allow time for the cookies banner to be dismissed
        print("Cookies accepted.")
    except Exception as e:
        print(f"Cookies popup not found or already accepted: {e}")

# Function to scroll the page to load more content
def scroll_to_load():
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)  # Wait for new content to load
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break  # Exit if no more content is loaded
        last_height = new_height
    print("Page fully scrolled.")

# Function to scrape product details from a single category page
def scrape_category_page(category_url):
    driver.get(category_url)
    time.sleep(2)  # Give the page time to load
    accept_cookies()  # Handle cookies popup

    # Scroll to the bottom of the page to load all products
    scroll_to_load()

    # Wait for product elements to load
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.product-image-wrap')))
        product_divs = driver.find_elements(By.CSS_SELECTOR, 'div.product-item-info')
        
        print(f"Found {len(product_divs)} product divs")

        products = []
        for product_div in product_divs:
            try:
                # Extract product link
                product_link = product_div.find_element(By.CSS_SELECTOR, 'a.product-item-photo').get_attribute('href')
                
                # Extract product title from the 'alt' attribute of the image
                product_title = product_div.find_element(By.CSS_SELECTOR, 'img.product-image-photo').get_attribute('alt')
                
                # Extract product image URL
                product_image_url = product_div.find_element(By.CSS_SELECTOR, 'img.product-image-photo').get_attribute('src')

                # Extract price
                try:
                    price_element = product_div.find_element(By.CSS_SELECTOR, '.price-wrapper .price')
                    product_price = price_element.text.strip() if price_element else "Price not found"
                except Exception as e:
                    product_price = "Price not found"
                    print(f"Error finding price for product: {product_title}. Error: {e}")
                
                products.append({
                    'title': product_title,
                    'link': product_link,
                    'image': product_image_url,
                    'price': product_price
                })

                print(f"Scraped: {product_title}, {product_link}, {product_image_url}, {product_price}")
            except Exception as e:
                print(f"Error scraping product: {e}")
                continue
    except Exception as e:
        print(f"Error navigating category: {e}")
        driver.save_screenshot("error_screenshot.png")
        return []

    return products

# Function to scrape multiple pages for the same category
def scrape_category_pages(category_name, category_urls):
    all_products = []
    
    for page_url in category_urls:
        print(f"Scraping page: {page_url}")
        products = scrape_category_page(page_url)
        all_products.extend(products)  # Append products from each page to the same list
    
    return all_products

# Define the categories to scrape, including specific URLs for each page
categories = {
    'Electric Screwdrivers': [
        'https://www.dedeman.ro/ro/masini-de-gaurit-si-insurubat/c/251?page=1',
        'https://www.dedeman.ro/ro/masini-de-gaurit-si-insurubat/c/251?page=2',
        'https://www.dedeman.ro/ro/masini-de-gaurit-si-insurubat/c/251?page=3',
    ],
    'Wood Screws': [
        'https://www.dedeman.ro/ro/suruburi-pentru-lemn-cu-cap-inecat/c/3152?page=1',
        'https://www.dedeman.ro/ro/suruburi-pentru-lemn-cu-cap-inecat/c/3152?page=2',
        'https://www.dedeman.ro/ro/suruburi-pentru-lemn-cu-cap-inecat/c/3152?page=3',
    ],
    'Hex Nuts': [
        'https://www.dedeman.ro/ro/piulite-hexagonale/c/3173?page=1',
    ],
    'Interior Paints': [
        'https://www.dedeman.ro/ro/vopsele-lavabile-pentru-interior/c/3908?page=1',
        'https://www.dedeman.ro/ro/vopsele-lavabile-pentru-interior/c/3908?page=2',
        'https://www.dedeman.ro/ro/vopsele-lavabile-pentru-interior/c/3908?page=3',
    ],
    'Wood Products': [
        'https://www.dedeman.ro/ro/produse-din-lemn/c/59?page=1',
        'https://www.dedeman.ro/ro/produse-din-lemn/c/59?page=2',
        'https://www.dedeman.ro/ro/produse-din-lemn/c/59?page=3',
        'https://www.dedeman.ro/ro/produse-din-lemn/c/59?page=4',
        'https://www.dedeman.ro/ro/produse-din-lemn/c/59?page=5',
    ],
    'Wood Drill Bits': [
        'https://www.dedeman.ro/ro/burghie-lemn/c/3562?page=1',
    ],
    'Special Adhesives': [
        'https://www.dedeman.ro/ro/adezivi-de-montaj-speciali/c/3374?page=1',
        'https://www.dedeman.ro/ro/adezivi-de-montaj-speciali/c/3374?page=2',
        'https://www.dedeman.ro/ro/adezivi-de-montaj-speciali/c/3374?page=3',
    ],
    'Saws': [
        'https://www.dedeman.ro/ro/fierastraie/c/252?page=1',
        'https://www.dedeman.ro/ro/fierastraie/c/252?page=2',
    ],
    'Rulers': [
        'https://www.dedeman.ro/ro/rigle/c/934?page=1',
        'https://www.dedeman.ro/ro/rigle/c/934?page=2',
    ],
    'Electric Sanders': [
        'https://www.dedeman.ro/ro/slefuitoare-electrice/c/254?page=1',
    ],
    'Sanding Sheets': [
        'https://www.dedeman.ro/ro/foi-abrazive-pentru-slefuire-manuala/c/3573?page=1',
    ],
    'Hammers': [
        'https://www.dedeman.ro/ro/ciocane/c/298?page=1',
        'https://www.dedeman.ro/ro/ciocane/c/298?page=2',
        'https://www.dedeman.ro/ro/ciocane/c/298?page=3',
    ],
    'Brushes': [
        'https://www.dedeman.ro/ro/pensule/c/943?page=1',
    ]
}

# Function to scrape all categories and their pages
def scrape_categories(categories):
    all_products = {}

    for category_name, category_urls in categories.items():
        print(f"Scraping category: {category_name}")
        products = scrape_category_pages(category_name, category_urls)  # Scrape all pages for the category
        all_products[category_name] = products  # Store all products under the same category name

    return all_products

# Scrape the categories and get the products
all_products = scrape_categories(categories)

# Close the driver
driver.quit()

# Save the products in a JSON file
with open('dedeman_products.json', 'w', encoding='utf-8') as f:
    json.dump(all_products, f, ensure_ascii=False, indent=4)

print("Scraping completed and saved to dedeman_products.json")
