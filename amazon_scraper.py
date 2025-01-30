pip install requests beautifulsoup4 pandas

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

# ✅ List of rotating User-Agents to avoid detection
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.177 Safari/537.36",
]

def fetch_product_details(product_url):
    """Fetches detailed product information from its individual page."""

    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "en-US,en;q=0.9",
    }

    time.sleep(random.uniform(3, 6))  # Random delay to avoid bot detection

    response = requests.get(product_url, headers=headers)
    if response.status_code != 200:
        print(f"❌ Failed to load product page: {product_url}")
        return None

    soup = BeautifulSoup(response.content, "html.parser")

    # ✅ Extract Product Name
    title_element = soup.find("span", {"id": "productTitle"})
    product_name = title_element.get_text(strip=True) if title_element else "N/A"

    # ✅ Extract Price
    price_element = soup.find("span", class_="a-offscreen")
    product_price = price_element.get_text(strip=True) if price_element else "N/A"

    # ✅ Extract Rating
    rating_element = soup.find("span", class_="a-icon-alt")
    product_rating = rating_element.get_text(strip=True).split(" ")[0] if rating_element else "N/A"

    # ✅ Extract Seller Name Correctly
    seller_element = soup.find("a", {"id": "sellerProfileTriggerId"})
    seller_name = seller_element.get_text(strip=True) if seller_element else "N/A"

    return {
        "Product Name": product_name,
        "Price (₹)": product_price,
        "Rating": product_rating,
        "Seller Name": seller_name
    }

def fetch_amazon_products(url, max_pages=3):
    """Scrapes Amazon search pages and visits each product page for details."""

    all_products = []
    page = 1

    while page <= max_pages:
        print(f"📄 Scraping Search Page {page}...")

        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept-Language": "en-US,en;q=0.9",
        }
        time.sleep(random.uniform(3, 10))  # Random delay

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"❌ Failed to retrieve page {page}. Status code: {response.status_code}")
            break

        soup = BeautifulSoup(response.content, "html.parser")

        # ✅ Find all product containers
        products = soup.find_all("div", {"data-component-type": "s-search-result"})

        for product in products:
            try:
                # ✅ Extract Product URL
                link_element = product.find("a", class_="a-link-normal s-no-outline")
                product_url = "https://www.amazon.in" + link_element["href"] if link_element else "N/A"

                # ✅ Go inside the product page and scrape details
                if product_url != "N/A":
                    product_details = fetch_product_details(product_url)
                    if product_details:
                        all_products.append(product_details)

            except Exception as e:
                print(f"⚠️ Error extracting product details: {e}")

        # ✅ Check for the next page button
        next_page = soup.find("a", class_="s-pagination-next")
        if next_page and "href" in next_page.attrs:
            url = "https://www.amazon.in" + next_page["href"]
            page += 1
        else:
            print("✅ No more pages found.")
            break

    return all_products

def save_to_csv(data, filename="amazon_full_product_data.csv"):
    """Saves the scraped product data to a CSV file."""
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"✅ Data saved to {filename}")

if __name__ == "__main__":
    # ✅ Amazon category URL
    category_url = "https://www.amazon.in/s?rh=n%3A6612025031&fs=true&ref=lp_6612025031_sar"

    # ✅ Scrape first 3 pages of products (Modify `max_pages` if needed)
    product_data = fetch_amazon_products(category_url, max_pages=3)
    save_to_csv(product_data)
