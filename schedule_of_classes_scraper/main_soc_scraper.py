import soc_scraper
import constants
import csv
import time
from course_prefixes_dataset_creation.main_course_prefixes_scraper import update_umd_courses
import pandas as pd

with open('umd_schedule_of_classes_courses.csv', mode='w', newline='') as file:
    start_time = time.time()
    writer = csv.writer(file)
    # Write the header row
    writer.writerow(constants.CSV_SOC_HEADER)

    update_umd_courses(file_path='../course_prefixes_dataset_creation/umd_course_prefixes.csv')
    df = pd.read_csv("../course_prefixes_dataset_creation/umd_course_prefixes.csv")

    # Iterate over each course acronym
    for course_acronym in df["COURSE PREFIX"]:
        soc_scraper.scrape_course_data(course_acronym, file)

    print("Data collection complete. Data has been saved to umd_schedule_of_classes_courses.csv")
    print("--- %s seconds ---" % (time.time() - start_time))
