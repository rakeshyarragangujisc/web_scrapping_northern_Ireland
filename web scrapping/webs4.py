import pandas as pd

# Read the CSV files into DataFrames
df_household = pd.read_csv('household_detailed_metadata.csv')
df_people = pd.read_csv('people_detailed_metadata.csv')

# Define the relevant columns
geo_column_household = 'Variable Code'  # Assuming this is the correct column name for household
geo_column_people = 'Variable Code'     # Assuming this is the correct column name for people

# Function to check if Variable Code starts with 'N' or '95'
def is_geography_related(code):
    code_str = str(code)
    return (code_str.startswith('N') and any(char.isalpha() for char in code_str)) or code_str.startswith('95')

# Household data separation based on geography-related codes
geo_household = df_household[df_household[geo_column_household].apply(is_geography_related)]
non_geo_household = df_household[~df_household[geo_column_household].apply(is_geography_related)]

# People data separation based on geography-related codes
geo_people = df_people[df_people[geo_column_people].apply(is_geography_related)]
non_geo_people = df_people[~df_people[geo_column_people].apply(is_geography_related)]

# Save the DataFrames into an Excel file with different sheets
output_path = 'processed_data1.xlsx'

with pd.ExcelWriter(output_path) as writer:
    # non-geographical data to their respective sheets
    non_geo_household.to_excel(writer, sheet_name='Household', index=False)
    non_geo_people.to_excel(writer, sheet_name='People', index=False)
    
    # geographical data to separate sheets
    geo_household.to_excel(writer, sheet_name='Household_Geography', index=False)
    geo_people.to_excel(writer, sheet_name='People_Geography', index=False)

print(f"Data processed and saved to {output_path}.")
