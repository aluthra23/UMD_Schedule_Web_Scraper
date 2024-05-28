import pandas as pd
import requests
from bs4 import BeautifulSoup
import csv
import helper  # Ensure you have a helper.py file or remove this if not used

# Term ID for the Fall 2024 term
term_id = "202408"

# Base URL for the UMD schedule of classes search
base_url = "https://app.testudo.umd.edu/soc/search"

def scrape_course_data(course_acronym, file):
    url = f"{base_url}?courseId={course_acronym}&sectionId=&termId={term_id}&_openSectionsOnly=on&creditCompare=%3E%3D&credits=0.0&courseLevelFilter=UGRAD&instructor=&_facetoface=on&_blended=on&_online=on&courseStartCompare=&courseStartHour=&courseStartMin=&courseStartAM=&courseEndHour=&courseEndMin=&courseEndAM=&teachingCenter=ALL&_classDay1=on&_classDay2=on&_classDay3=on&_classDay4=on&_classDay5=on"

    # Fetch the web page
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch data for {course_acronym}")
        return

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    courses = soup.find_all('div', class_='course')

    for course in courses:
        course_number = course.find('div', class_='course-id').text.strip()
        section_title = course.find('span', class_='course-title').text.strip()

        # Normal Classes
        open_sections = course.find_all('div', class_='section delivery-f2f')
        update_classes_data(course_number, open_sections,
                            class_name="section-day-time-group push_two five columns",
                            file_path=file, class_setting="NORMAL")

        # Blended Classes
        open_sections = course.find_all('div', class_='section delivery-blended')
        update_classes_data(course_number, open_sections,
                            class_name="section-day-time-group push_one five columns",
                            file_path=file, class_setting="BLENDED")

        # Online Classes
        open_sections = course.find_all('div', class_='section delivery-online')
        update_classes_data(course_number, open_sections,
                            class_name="section-day-time-group push_one five columns",
                            file_path=file, class_setting="ONLINE")


def update_classes_data(course_number, open_sections, class_name, file_path, class_setting):
    data = set()

    if open_sections:
        for section in open_sections:
            section_data = {
                "BUILDING CODE": None,
                "FULL-FORM": None
            }

            section_id = str(section.find('span', class_='section-id').text).strip()

            times = section.find('div', class_="class-days-container")
            times = times.find_all('div', class_='row')

            # Iterating through class-days-container
            for time in times:
                room = time.find('span', class_='class-building')
                if room:
                    building_code = room.find('span', class_='building-code')
                    if building_code:
                        building_code = building_code.text.strip()
                        section_data["BUILDING CODE"] = building_code
                        data.add(building_code)

    else:
        return

    if data:
        df = pd.read_csv("umd_building_codes.csv")
        building_codes = set(df["BUILDING CODE"])
        building_codes.update(data)
        updated_df = pd.DataFrame({"BUILDING CODE": list(building_codes)})
        updated_df.to_csv("umd_building_codes.csv", index=False)