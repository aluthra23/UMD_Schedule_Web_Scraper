import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the webpage containing the building codes and full names
url = "https://www.arcgis.com/home/item.html?id=3e678424faaa4fcd8fd9af75885d4472"

# Send a GET request to the webpage
response = requests.get(url)

# Parse the HTML content of the webpage
soup = BeautifulSoup(response.content, 'html.parser')

# Find the table or relevant section containing the building information
# Adjust the selector based on the actual structure of the webpage
table = soup.find('table')

# Initialize lists to store the building codes and names
codes = []
full_names = []

# Loop through the table rows and extract the building codes and full names
for row in table.find_all('tr')[1:]:  # Skip the header row
    cols = row.find_all('td')
    if len(cols) >= 2:
        code = cols[0].text.strip()
        full_name = cols[1].text.strip()
        codes.append(code)
        full_names.append(full_name)

# Create a pandas DataFrame to store the data
df = pd.DataFrame({
    'Building Code': codes,
    'Full Name': full_names
})

# Save the DataFrame to a CSV file
df.to_csv('umd_building_codes.csv', index=False)

print("Dataset created and saved as 'umd_building_codes.csv'")