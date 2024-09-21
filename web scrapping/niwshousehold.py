import requests
from bs4 import BeautifulSoup
import pandas as pd

# Load the CSV file with the list of topics
topics_df = pd.read_csv("topics_list.csv")

# Initialize a list to store the detailed data
detailed_data = []

# Loop through each topic in the CSV
for _, topic in topics_df.iterrows():
    # Get the detail page URL
    detail_url = topic["Detail URL"]
    
    # Send a GET request to fetch the detail page content
    response = requests.get(detail_url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Extract the topic description
    description_section = soup.find("section", class_="page-section")
    description = description_section.find("p", class_="pre-wrap").get_text(strip=True) if description_section else "Description not available"
    
    # Find the section containing the variable categories by its heading
    categories_section = soup.find_all("section", class_="page-section")
    
    # Loop through sections to find the one with "Variable categories" heading
    variable_categories_section = None
    for section in categories_section:
        heading = section.find("h2")
        if heading and "Variable categories" in heading.get_text(strip=True):
            variable_categories_section = section
            break
    
    # Extract the variable categories table if found
    if variable_categories_section:
        categories_table = variable_categories_section.find("table")
        if categories_table:
            # Extract each row from the table
            for row in categories_table.find("tbody").find_all("tr"):
                columns = row.find_all("td")
                if len(columns) == 2:  # Ensure the row has exactly two columns
                    variable_label = columns[0].get_text(strip=True)  # First column is the variable label
                    variable_code = columns[1].get_text(strip=True)   # Second column is the variable code
                    
                    # Append the detailed data for each category
                    detailed_data.append({
                        "Topic Code": topic["Topic Code"],
                        "Topic Name": topic["Topic Name"],
                        "Topic Description": description,
                        "Variable Code": variable_code,
                        "Variable Name": variable_label
                    })
        else:
            print(f"No table found in the Variable categories section for URL: {detail_url}")
    else:
        print(f"Variable categories section not found for URL: {detail_url}")
        # Append just the description without categories
        detailed_data.append({
            "Topic Code": topic["Topic Code"],
            "Topic Name": topic["Topic Name"],
            "Topic Description": description,
            "Variable Code": None,
            "Variable Name": None
        })

# Convert the detailed data to a DataFrame
detailed_df = pd.DataFrame(detailed_data)

# Save the DataFrame to a CSV file
detailed_df.to_csv("household_detailed_metadata.csv", index=False)

print("Detailed metadata saved to household_detailed_metadata.csv")
