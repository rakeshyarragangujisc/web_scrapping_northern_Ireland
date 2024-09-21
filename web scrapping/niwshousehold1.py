import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define the base URL for scraping
base_url = "https://build.nisra.gov.uk"

# Define the URL of the page to scrape
main_url = f"{base_url}/en/metadata/dataset?d=HOUSEHOLD"

# Send a GET request to fetch the main page content
response = requests.get(main_url)
soup = BeautifulSoup(response.content, "html.parser")

# Find the table containing the list of variables
table = soup.find("table", class_="meta-table")

# Initialize a list to store the topic code and name
topics_data = []

# Extract each row from the table
for row in table.find("tbody").find_all("tr"):
    # Extract the topic name and mnemonic (code)
    topic_name = row.find("td").get_text(strip=True)
    topic_code = row.find("td").find_next("td").get_text(strip=True)
    
    # Extract the link to the detailed page
    link = row.find("td").find("a")["href"]
    detail_url = f"{base_url}{link}"
    
    # Append the extracted information to the list
    topics_data.append({
        "Topic Code": topic_code,
        "Topic Name": topic_name,
        "Detail URL": detail_url
    })

# Convert the list to a DataFrame
topics_df = pd.DataFrame(topics_data)

# Save the DataFrame to a CSV file
topics_df.to_csv("topics_list.csv", index=False)

print("Topics list saved to topics_list.csv")
