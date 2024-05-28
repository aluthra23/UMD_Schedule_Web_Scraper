# import pandas as pd
# import requests
# from bs4 import BeautifulSoup
# import csv
# import helper  # Ensure you have a helper.py file or remove this if not used
#
# # Base URL for the UMD schedule of classes search
# base_url = "https://www.google.com/maps/search"
#
# def scrape_building_data(course_acronym, file):
#     url = f"{base_url}/{course_acronym} UMD Building"
#
#     # Fetch the web page
#     response = requests.get(url)
#     if response.status_code != 200:
#         print(f"Failed to fetch data for {course_acronym}")
#         return
#
#     # Parse the HTML content
#     soup = BeautifulSoup(response.text, 'html.parser')
#     building_name = soup.find('span', class_='a5H0ec').text.strip()
#
#
#
#
# def update_classes_data(course_number, open_sections, class_name, file_path, class_setting):
#     data = set()
#
#     if open_sections:
#         for section in open_sections:
#             section_data = {
#                 "BUILDING CODE": None,
#                 "FULL-FORM": None
#             }
#
#             section_id = str(section.find('span', class_='section-id').text).strip()
#
#             times = section.find('div', class_="class-days-container")
#             times = times.find_all('div', class_='row')
#
#             # Iterating through class-days-container
#             for time in times:
#                 room = time.find('span', class_='class-building')
#                 if room:
#                     building_code = room.find('span', class_='building-code')
#                     if building_code:
#                         building_code = building_code.text.strip()
#                         section_data["BUILDING CODE"] = building_code
#                         data.add(building_code)
#
#     else:
#         return
#
#     if data:
#         df = pd.read_csv("umd_building_codes.csv")
#         building_codes = set(df["BUILDING CODE"])
#         building_codes.update(data)
#         updated_df = pd.DataFrame({"BUILDING CODE": list(building_codes)})
#         updated_df.to_csv("umd_building_codes.csv", index=False)