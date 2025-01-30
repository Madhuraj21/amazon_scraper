# amazon_scraper
📦 Amazon Product Scraper
This Python script scrapes Product Name, Price, Rating, and Seller Name from Amazon by visiting each product page.

📝 Features
✔ Extracts product details from Amazon
✔ Goes inside each product page for accuracy
✔ Handles missing values gracefully
✔ Rotates User-Agents to avoid detection
✔ Saves data to CSV for easy access

🚀 Installation
1️⃣ Clone the Repository
git clone https://github.com/YOUR_GITHUB_USERNAME/amazon-scraper.git
cd amazon-scraper

2️⃣ Install Dependencies
pip install requests beautifulsoup4 pandas

🛠 Usage
Run the scraper:
python amazon_scraper.py

This will scrape products from Amazon's category page, visit each product page, and save the data to amazon_full_product_data.csv.

