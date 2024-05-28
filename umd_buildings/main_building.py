import building_code_scraper
import constants
import csv
import pandas as pd

#
# with open('umd_building_codes.csv', mode='w', newline='') as file:
#     writer = csv.writer(file)
#     # Write the header row
#     writer.writerow(constants.CSV_BUILDINGS_HEADER)
#
#     # Iterate over each course acronym
# for course_acronym in constants.course_acronyms:
#     building_code_scraper.scrape_course_data(course_acronym, file)
#
# print("Data collection complete. Data has been saved to umd_schedule_of_classes_courses.csv")
#
df = pd.read_csv('umd_building_codes.csv')

# Sort the DataFrame by the 'Course Prefix' column
df_sorted = df.sort_values(by='BUILDING CODE')

# Write the sorted DataFrame back to the CSV file
df_sorted.to_csv('umd_building_codes.csv', index=False)

print(df)

print("CSV file sorted and saved successfully.")


