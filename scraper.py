import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

print(" Starting Web Scraper...")
print("=" * 50)

try:
    # Initialize HTTP request to target e-commerce website
    # Using timeout to prevent hanging indefinitely on connection issues
    print(" Connecting to website...")
    url = "https://webscraper.io/test-sites/e-commerce/allinone"
    response = requests.get(url, timeout=10)

    # Validate server response before proceeding with parsing
    # Non-200 status codes indicate potential server errors or access issues
    print(f" Status Code: {response.status_code}")
    if response.status_code != 200:
        print("Failed to connect to website")
        exit()

    # Parse HTML content using BeautifulSoup for efficient element extraction
    # HTML parser is chosen for its compatibility with standard HTML documents
    print(" Connected successfully! Parsing HTML...")
    soup = BeautifulSoup(response.text, "html.parser")

    # Locate all product containers using specific class identifier
    # This approach isolates product data from other page elements
    products = soup.find_all("div", class_="thumbnail")
    print(f"Found {len(products)} products")

    # Initialize structured storage for extracted product information
    scraped_data = []

    # Iterate through each product container to extract relevant data points
    for product in products:
        # Extract product name with fallback for missing elements
        # Strip whitespace to ensure clean data formatting
        name_element = product.find("a", class_="title")
        name = name_element.text.strip() if name_element else "N/A"

        # Capture pricing information from dedicated pricing element
        price_element = product.find("h4", class_="price")
        price = price_element.text.strip() if price_element else "N/A"

        # Retrieve product description while handling optional field
        description_element = product.find("p", class_="description")
        description = description_element.text.strip() if description_element else "N/A"

        # Calculate star rating by counting filled star elements
        # Provides quantitative rating from visual representation
        rating_element = product.find("div", class_="ratings")
        rating = (
            len(rating_element.find_all("span", class_="glyphicon-star"))
            if rating_element
            else 0
        )

        # Compile extracted data into structured dictionary
        # Maintaining consistent field names for CSV export
        scraped_data.append(
            {
                "Product Name": name,
                "Price": price,
                "Description": description,
                "Rating": rating,
            }
        )

        print(f" Processed: {name}")

    # Generate timestamp for unique filename creation
    # Prevents overwriting previous files and enables version tracking
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"scraped_data_{timestamp}.csv"

    # Export structured data to CSV file with UTF-8 encoding
    # Ensures compatibility with special characters and international text
    with open(filename, "w", newline="", encoding="utf-8") as file:
        fieldnames = ["Product Name", "Price", "Description", "Rating"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write header row to establish column structure
        writer.writeheader()
        for product in scraped_data:
            writer.writerow(product)

    # Provide user feedback on output file and processing summary
    print(f"Data saved to: {filename}")
    print(f"Total records saved: {len(scraped_data)}")

    # Display sample data for immediate verification of content quality
    # Limited to first 3 products for concise output
    print("Sample of collected data:")
    print("-" * 50)
    for i, product in enumerate(scraped_data[:3]):
        print(f"Product {i+1}:")
        print(f"  Name: {product['Product Name']}")
        print(f"  Price: {product['Price']}")
        print(f"  Rating: {product['Rating']}/5 stars")
        print(f"  Description: {product['Description'][:50]}...")  # First 50 chars
        print("-" * 30)

except Exception as e:
    # Comprehensive error handling for network issues, parsing errors, or file access problems
    print(f" Error occurred: {e}")
    print("Please check your internet connection")

print("=" * 50)
print("Scraping completed successfully!")
input("Press Enter to exit...")
