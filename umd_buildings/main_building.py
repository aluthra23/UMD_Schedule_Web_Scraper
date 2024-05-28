import building_code_scraper
import constants
import csv


with open('umd_schedule_of_classes_courses.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write the header row
    writer.writerow(constants.CSV_SOC_HEADER)

    # Iterate over each course acronym
    for course_acronym in constants.course_acronyms:
        soc_scraper.scrape_course_data(course_acronym, file)

    print("Data collection complete. Data has been saved to umd_schedule_of_classes_courses.csv")


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
