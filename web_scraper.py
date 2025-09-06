import csv
from datetime import datetime
import glob


def generate_html_report():
    """Finds the latest CSV file and generates an HTML report from it."""
    print(" Searching for latest scraped data file...")

    # Find all CSV files starting with 'scraped_data_'
    csv_files = glob.glob("scraped_data_*.csv")

    if not csv_files:
        print(" No scraped data files found. Please run web_scraper.py first.")
        return

    # Get the most recently created file
    latest_file = max(csv_files, key=os.path.getctime)
    print(f" Found file: {latest_file}")

    # Read data from the CSV file
    data = []
    with open(latest_file, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)

    # Generate HTML filename based on CSV timestamp
    timestamp = latest_file.replace("scraped_data_", "").replace(".csv", "")
    html_filename = f"report_{timestamp}.html"

    # Create the HTML report
    with open(html_filename, "w", encoding="utf-8") as html_file:
        html_file.write(
            f"""<!DOCTYPE html>
<html>
<head>
    <title>Web Scraping Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #2c3e50; text-align: center; margin-bottom: 20px; }}
        .info {{ background: #e8f4fc; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th {{ background-color: #34495e; color: white; padding: 15px; text-align: left; }}
        td {{ padding: 12px; border-bottom: 1px solid #ddd; }}
        tr:hover {{ background-color: #f8f9fa; }}
        .rating {{ color: #ffd700; font-weight: bold; }}
        .product-name {{ font-weight: bold; color: #2c3e50; }}
        .price {{ color: #27ae60; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Web Scraping Report</h1>
        
        <div class="info">
            <strong>Generated on:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}<br>
            <strong>Total products scraped:</strong> {len(data)}<br>
            <strong>Source File:</strong> {latest_file}
        </div>
        
        <table>
            <tr>
                <th>Product Name</th>
                <th>Price</th>
                <th>Rating</th>
                <th>Description</th>
            </tr>"""
        )

        for product in data:
            rating = int(product["Rating"])
            stars = "★" * rating + "☆" * (5 - rating)
            html_file.write(
                f"""
            <tr>
                <td class="product-name">{product['Product Name']}</td>
                <td class="price">{product['Price']}</td>
                <td><span class="rating">{stars}</span> ({rating}/5)</td>
                <td>{product['Description']}</td>
            </tr>"""
            )

        html_file.write(
            """
        </table>
    </div>
</body>
</html>"""
        )

    print(f" HTML report generated: {html_filename}")
    print(" Open this file in your web browser to view the results!")


if __name__ == "__main__":
    import os

    generate_html_report()
    input("Press Enter to exit...")
