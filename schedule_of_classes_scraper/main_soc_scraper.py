import soc_scraper
import constants
import csv


with open('class_sections.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write the header row
    writer.writerow(constants.CSV_SOC_HEADER)

    # Iterate over each course acronym
    for course_acronym in constants.course_acronyms:
        soc_scraper.scrape_course_data(course_acronym, file)

    print("Data collection complete. Data has been saved to open_sections.csv")
