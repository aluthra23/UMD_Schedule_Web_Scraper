import pandas as pd
import requests
from bs4 import BeautifulSoup

import helper

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

    # if(len(courses) == 0):
    #     print(f"{course_acronym} HAS 0 undergrad courses")

    for course in courses:
        course_number = course.find('div', class_='course-id').text.strip()

        section_title = course.find('span', class_='course-title').text.strip()

        section_min_credits = course.find('span', class_='course-min-credits')
        if section_min_credits:
            section_min_credits = int(section_min_credits.text.strip())

            section_max_credits = course.find('span', class_='course-max-credits')
            if section_max_credits:
                section_max_credits = int(section_max_credits.text.strip())
            else:
                section_max_credits = section_min_credits

        section_grading = str(course.find('span', class_='grading-method').text).strip()

        ## DO DESCRIPTION AS WELL

        description_fields = {
            "PREREQUISITE":None,
            "COREQUISITE":None,
            "RESTRICTION":None,
            "CREDIT ONLY GRANTED FOR":None,
            "FORMERLY":None,
            "RECOMMENDED":None,
            "CROSS-LISTED WITH": None,
            "DESCRIPTION": None,
        }

        descriptions = course.find('div', class_='approved-course-texts-container')
        if descriptions:
            descriptions = course.find_all('div', class_='approved-course-text')

            for description in descriptions:
                description_fields = helper.extract_course_details(html_content=str(description),
                                                                   existing_dict=description_fields,
                                                                   actual_html=description)

        descriptions = course.find('div', class_='course-texts-container')
        if descriptions:
            description_fields = helper.extract_abnormal_course_details(existing_dict=description_fields,
                                                                  actual_html=descriptions)


        # Normal Classes
        open_sections = course.find_all('div', class_='section delivery-f2f')
        update_classes_data(course_number, open_sections,
                            class_name="section-day-time-group push_two five columns",
                            file_path=file, class_setting="NORMAL",
                            section_title=section_title,
                            section_min_credits=section_min_credits,
                            section_max_credits=section_max_credits,
                            section_grading=section_grading,
                            description_fields=description_fields)

        # Blended Classes
        open_sections = course.find_all('div', class_='section delivery-blended')
        update_classes_data(course_number, open_sections,
                            class_name="section-day-time-group push_one five columns",
                            file_path=file, class_setting="BLENDED",
                            section_title=section_title,
                            section_min_credits=section_min_credits,
                            section_max_credits=section_max_credits,
                            section_grading=section_grading,
                            description_fields=description_fields)

        # Online Classes
        open_sections = course.find_all('div', class_='section delivery-online')
        update_classes_data(course_number, open_sections,
                            class_name="section-day-time-group push_one five columns",
                            file_path=file, class_setting="ONLINE",
                            section_title=section_title,
                            section_min_credits=section_min_credits,
                            section_max_credits=section_max_credits,
                            section_grading=section_grading,
                            description_fields=description_fields)


def update_classes_data(course_number, open_sections, class_name, file_path, class_setting, section_title, section_min_credits, section_max_credits, section_grading, description_fields):

    data = []
    if open_sections:
        for section in open_sections:
            section_data = {
                "COURSE NUMBER": course_number,
                "COURSE TITLE": section_title,
                "MINIMUM CREDITS": section_min_credits,
                "MAXIMUM CREDITS": section_max_credits,
                "GRADING METHOD": section_grading,
                "SECTION ID": None,
                "INSTRUCTOR": None,
                "TOTAL SEATS": None,
                "OPEN SEATS": None,
                "WAITLIST COUNT": None,
                "LECTURE TIME": None,
                "DISCUSSION TIME": None,
                "LAB TIME": None,
                "UNSPECIFIED TIME MESSAGE": None,
                "HAS LECTURE": 0,
                "HAS DISCUSSION": 0,
                "HAS LAB": 0,
                "IS NORMAL": 0,
                "IS BLENDED (NORMAL AND ONLINE)": 0,
                "IS ONLINE": 0,
                "SPECIAL RESTRICTION": None,
                "PREREQUISITE": description_fields["PREREQUISITE"],
                "COREQUISITE": description_fields["COREQUISITE"],
                "RESTRICTION": description_fields["RESTRICTION"],
                "CREDIT ONLY GRANTED FOR": description_fields["CREDIT ONLY GRANTED FOR"],
                "FORMERLY": description_fields["FORMERLY"],
                "RECOMMENDED": description_fields["RECOMMENDED"],
                "CROSS-LISTED WITH": description_fields["CROSS-LISTED WITH"],
                "DESCRIPTION": description_fields["DESCRIPTION"],
            }

            if class_setting == 'NORMAL':
                section_data["IS NORMAL"] = 1
            elif class_setting == 'ONLINE':
                section_data["IS ONLINE"] = 1
            else:
                section_data["IS NORMAL"] = 1
                section_data["IS ONLINE"] = 1
                section_data["IS BLENDED (NORMAL AND ONLINE)"] = 1

            # print(f"{course_number} ")


            section_id = str(section.find('span', class_='section-id').text).strip()
            section_data["SECTION ID"] = section_id

            section_instructor = str(section.find('span', class_='section-instructor').text).strip()
            section_data["INSTRUCTOR"] = section_instructor

            total_seats = str(section.find('span', class_='total-seats-count').text).strip()
            section_data["TOTAL SEATS"] = total_seats

            open_seats = str(section.find('span', class_='open-seats-count').text).strip()
            section_data["OPEN SEATS"] = open_seats

            waitlist_seats = str(section.find('span', class_='waitlist-count').text).strip()
            section_data["WAITLIST COUNT"] = waitlist_seats

            times = section.find('div', class_="class-days-container")
            times = times.find_all('div', class_='row')

            # Iterating through class-days-container
            for i, time in enumerate(times):
                if time.find('span', class_='section-days'):
                    days = time.find('span', class_='section-days').text.strip()

                    if str(days).upper().find("TBA") != -1:
                        section_data["UNSPECIFIED TIME MESSAGE"] = days
                        continue

                    start_time = time.find('span', class_='class-start-time').text.strip()
                    end_time = time.find('span', class_='class-end-time').text.strip()

                    class_type = time.find('div', class_='two columns')

                    if class_type:
                        class_type = class_type.text.strip().upper()

                        if class_type == "DISCUSSION":
                            section_data["HAS DISCUSSION"] = 1
                            section_data["DISCUSSION TIME"] = f"{days} {start_time}-{end_time}"

                            # if section_data["HAS LAB"]:
                            #     print(f"{course_number} {section_id} has lab and discussion")

                        elif class_type == "LAB":
                            section_data["HAS LAB"] = 1
                            section_data["LAB TIME"] = f"{days} {start_time}-{end_time}"

                            # if section_data["HAS DISCUSSION"]:
                            #     print(f"{course_number} {section_id} has lab and discussion")
                    else:
                        class_type = "LECTURE"
                        section_data["HAS LECTURE"] = 1
                        section_data["LECTURE TIME"] = f"{days} {start_time}-{end_time}"

                else:
                    message = time.find('span', class_='elms-class-message')
                    if message:
                        message = message.text.strip()
                    else:
                        message = time.find('div', class_='push_one eight columns class-message')

                        if message:
                            message = message.text.strip()
                        else:
                            message = time.find('div', class_='push_two eight columns class-message').text.strip()

                    section_data["UNSPECIFIED TIME MESSAGE"] = message

            # Iterating through section-texts-container
            restrictions = section.find('div', class_="section-texts-container")

            if restrictions:
                restrictions = restrictions.find_all('div', class_='section-text')

                full_restriction = ""
                for i, restriction in enumerate(restrictions):
                    # print(restriction)
                    link = helper.extract_link_from_html(str(restriction))

                    new_line = "\n"

                    if i + 1 == len(restrictions):
                        new_line = ""

                    if link:
                        full_restriction += f"{restriction.text}: {link}{new_line}"
                    else:
                        full_restriction += f"{restriction.text}{new_line}"

                section_data["SPECIAL RESTRICTION"] = full_restriction


            data.append(section_data)
    else:
        return

    if data:
        df = pd.DataFrame(data)
        df.to_csv(file_path, mode='a', header=False, index=False)
