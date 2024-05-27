# Web Scraper for UMD Course Data

## Overview
I have developed this UMD Schedule Web Scraper project, which is designed to scrape course information from the University of Maryland's [Course Catalog](https://academiccatalog.umd.edu/undergraduate/approved-courses/) and [Schedule of Classes](https://app.testudo.umd.edu/soc/) websites and then make datasets based on the data scraped. This project is structured into several directories, each containing specific scripts that perform various tasks related to data scraping and validation.

My inspiration for this came from a project idea related to UMD coursework and data analysis. However, I realized that I couldn't find any datasets related to UMD coursework particularly, so I decided to construct the datasets myself by developing webscrapers. 

## Citation Requirement
If you use any of the datasets or scripts from this project, you must cite the original author:
- Author: Arav Luthra

Please include the following citation in your work:

"Arav Luthra. UMD Schedule Web Scraper. https://github.com/aluthra23/UMD_Schedule_Web_Scraper/"

## Datasets

### With the webscrapers that I have built, I have developed the following 3 datasets: 


### `umd_catalog_courses.csv` (Found in course_catalog_scraper folder)
This is a dataset which contains data for each undergraduate course taught at UMD and was scraped from the Course Catalog page, as described above. The dataset looks like the following, with CMSC351 being an example. Any empty data for any of the fields implies that the specific course didn't have any information regarding it. 
  
| COURSE PREFIX | COURSE NUMBER | NAME     | CREDITS | DESCRIPTION                                                                                                          | PREREQUISITE                    | RESTRICTION                                                                                                  | FORMERLY NAMED | RECOMMENDED | CREDIT ONLY GRANTED FOR | REPEATABLE TO | CROSS-LISTED | COREQUISITE |
| ------------- | -------------- | -------- | ------- | -------------------------------------------------------------------------------------------------------------------- | ------------------------------- | ------------------------------------------------------------------------------------------------------------ | -------------- | ----------- | ------------------------ | ------------- | ------------ | ----------- |
| CMSC          | CMSC351        | Algorithms | 3       | A systematic study of the complexity of some elementary algorithms related to sorting, graphs and trees, and combinatorics. Algorithms are analyzed using mathematical techniques to solve recurrences and summations. | Minimum grade of C- in CMSC250 and CMSC216 | Must be in a major within the CMNS-Computer Science department; or must be in Engineering: Computer program; or must be in the Computer Science Minor program; and Permission from the CMSC - Computer Science department |                |             |                          |               |              |             |


### `umd_course_prefixes.csv` (Found in course_prefixes_dataset_creation folder)
This is a dataset which which stores each course prefix and also stores its respective full form. The data was scraped from the Course Catalog page, as described above. The dataset looks like the following with CMSC being an example. 

| COURSE PREFIX | FULL FORM            |
| ------------- | -------------------- |
| CMSC          | Computer Science     |

### `umd_schedule_of_classes_courses.csv` (Found in schedule_of_classes_scraper folder)
This is a dataset which contains data for each undergraduate course that will be taught in the Fall 2024 Semester and was scraped from the Schedule of Classes page, as described above. The scraper can be easily adjusted for other semesters as well. Some courses are repeated because they may have more than 1 section and teacher teaching the course. The dataset looks like the following, with CMSC351 being an example (There's 4 sections teaching 351 in the Fall 2024 Semester). Any empty data for any of the fields implies that the specific course didn't have any information regarding it. 

| COURSE NUMBER | COURSE TITLE | MINIMUM CREDITS | MAXIMUM CREDITS | GRADING METHOD | SECTION ID | INSTRUCTOR      | TOTAL SEATS | OPEN SEATS | WAITLIST COUNT | LECTURE TIME       | DISCUSSION TIME | LAB TIME | UNSPECIFIED TIME MESSAGE | HAS LECTURE | HAS DISCUSSION | HAS LAB | IS NORMAL | IS BLENDED (NORMAL AND ONLINE) | IS ONLINE | SPECIAL RESTRICTION | PREREQUISITE                        | COREQUISITE | RESTRICTION | CREDIT ONLY GRANTED FOR | FORMERLY | RECOMMENDED | CROSS-LISTED WITH | DESCRIPTION                                                                                                                                                                                                                                             |
| ------------- | ------------ | --------------- | --------------- | -------------- | ---------- | --------------- | ----------- | ---------- | --------------- | ------------------- | ---------------- | -------- | ------------------------- | ----------- | -------------- | ------- | --------- | ---------------------------- | ---------- | ------------------ | ----------------------------------- | ----------- | ----------- | ------------------------ | -------- | ----------- | ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| CMSC351       | Algorithms   | 3               | 3               | Reg            | 101        | Justin Wyss-Gallifent | 290         | 0          | 0               | MWF 8:00am-8:50am   |                |          |                           | 1           | 0              | 0       | 1         | 0                            | 0          |                    | Minimum grade of C- in CMSC250 and CMSC216 |             |             |                         | A systematic study of the complexity of some elementary algorithms related to sorting, graphs and trees, and combinatorics. Algorithms are analyzed using mathematical techniques to solve recurrences and summations. |
| CMSC351       | Algorithms   | 3               | 3               | Reg            | 201        | Clyde Kruskal   | 95          | 0          | 0               | MWF 11:00am-11:50am |                |          |                           | 1           | 0              | 0       | 1         | 0                            | 0          |                    | Minimum grade of C- in CMSC250 and CMSC216 |             |             |                         | A systematic study of the complexity of some elementary algorithms related to sorting, graphs and trees, and combinatorics. Algorithms are analyzed using mathematical techniques to solve recurrences and summations. |
| CMSC351       | Algorithms   | 3               | 3               | Reg            | 301        | Clyde Kruskal   | 200         | 103        | 0               | MWF 4:00pm-4:50pm   |                |          |                           | 1           | 0              | 0       | 1         | 0                            | 0          |                    | Minimum grade of C- in CMSC250 and CMSC216 |             |             |                         | A systematic study of the complexity of some elementary algorithms related to sorting, graphs and trees, and combinatorics. Algorithms are analyzed using mathematical techniques to solve recurrences and summations. |
| CMSC351       | Algorithms   | 3               | 3               | Reg            | 401        | Herve Franceschi| 135         | 0          | 0               | MWF 1:00pm-1:50pm   |                |          |                           | 1           | 0              | 0       | 1         | 0                            | 0          |                    | Minimum grade of C- in CMSC250 and CMSC216 |             |             |                         | A systematic study of the complexity of some elementary algorithms related to sorting, graphs and trees, and combinatorics. Algorithms are analyzed using mathematical techniques to solve recurrences and summations. |


## Directory Structure

### Root Directory
- `constants.py`: Contains three arrays:
  - `Course Acronyms`: An array of course prefixes.
  - `Course Catalog CSV Header`: An array defining the CSV header for the course catalog scraper.
  - `Schedule of Classes CSV Header`: An array defining the CSV header for the schedule of classes scraper.
- `helper.py`: Contains helper methods for scraping in each directory.

### `check_websites_for_course_updates` Directory
- `course_catalog.py`: Contains methods to scrape and validate that the current course acronyms array in `constants.py` includes all course prefixes displayed on the course catalog website. Also includes the `ensure_no_extra_elements` method to ensure there are no extra elements in the course acronyms array.
- `schedule_of_classes.py`: Contains methods to scrape and validate that the current course acronyms array in `constants.py` includes all course prefixes displayed on the schedule of classes website. Also includes the `ensure_no_extra_elements` method.
- `main_check_both_websites.py`: Main script to run both `course_catalog.py` and `schedule_of_classes.py` to check and validate the course acronyms array against both websites.

### `course_catalog_scraper` Directory
- `main_catalog_scraper.py`: Calls the `scrape_course_data` method in `scraper.py` for each course prefix. This method scrapes the webpage for all courses under a specific course prefix and stores the information in a CSV file named `umd_catalog_courses.csv`.
- `scraper.py`: Contains the `scrape_course_data` method which scrapes the following information for each course:

| COURSE PREFIX | COURSE NUMBER | NAME     | CREDITS | DESCRIPTION                                                                                                          | PREREQUISITE                    | RESTRICTION                                                                                                  | FORMERLY NAMED | RECOMMENDED | CREDIT ONLY GRANTED FOR | REPEATABLE TO | CROSS-LISTED | COREQUISITE |
| ------------- | -------------- | -------- | ------- | -------------------------------------------------------------------------------------------------------------------- | ------------------------------- | ------------------------------------------------------------------------------------------------------------ | -------------- | ----------- | ------------------------ | ------------- | ------------ | ----------- |
 
  The scraped data is stored in `umd_catalog_courses.csv`, as seen above. 

### `course_prefixes_dataset_creation` Directory
- `main_prefix_scraper.py`: Visits the course catalog and schedule of classes webpages to scrape the course prefixes and their full forms. The data is stored in a CSV file named `umd_course_prefixes.csv`.

  The `umd_course_prefixes.csv` contains the following data:

| COURSE PREFIX | FULL FORM            |
| ------------- | -------------------- |

### `schedule_of_classes_scraper` Directory
- `main_soc_scraper.py`: Calls the `scrape_course_data` method in `soc_scraper.py` for each course acronym. This method scrapes the schedule of classes webpage and stores the following information for each class under each course prefix:

| COURSE NUMBER | COURSE TITLE | MINIMUM CREDITS | MAXIMUM CREDITS | GRADING METHOD | SECTION ID | INSTRUCTOR | TOTAL SEATS | OPEN SEATS | WAITLIST COUNT | LECTURE TIME | DISCUSSION TIME | LAB TIME | UNSPECIFIED TIME MESSAGE | HAS LECTURE | HAS DISCUSSION | HAS LAB | IS NORMAL | IS BLENDED (NORMAL AND ONLINE) | IS ONLINE | SPECIAL RESTRICTION | PREREQUISITE | COREQUISITE | RESTRICTION | CREDIT ONLY GRANTED FOR | FORMERLY | RECOMMENDED                                                                                                                                                                                                            | CROSS-LISTED WITH                                                                                                                                                                                                      | DESCRIPTION                                                                                                                                                                                                            |
| ------------- | ------------ | --------------- | --------------- | -------------- | ---------- | ---------- | ------------ | ---------- | --------------- | ------------- | ---------------- | -------- | ------------------------- | ----------- | -------------- | ------- | --------- | ---------------------------- | ---------- | ------------------ | ------------ | ----------- | ----------- | ------------------------ | -------- |------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

  The scraped data is stored in `umd_schedule_of_classes_courses.csv` which can be found in this directory as well.

## Setup Instructions
1. Clone the repository:
    ```sh
    git clone https://github.com/aluthra23/UMD_Schedule_Web_Scraper.git
    cd UMD_Schedule_Web_Scraper
    ```

2. Install the required packages (Make sure you have pip downloaded):
    ```sh
    pip install -r requirements.txt
    ```

3. Run the scrapers: (use python or python3)
    - To check and update course acronyms:
      ```sh
      python check_websites_for_course_updates/main_check_both_websites.py
      ```
    - To scrape course catalog data:
      ```sh
      python course_catalog_scraper/main_catalog_scraper.py
      ```
    - To scrape course prefixes:
      ```sh
      python course_prefixes_dataset_creation/main_prefix_scraper.py
      ```
    - To scrape schedule of classes data:
      ```sh
      python schedule_of_classes_scraper/main_soc_scraper.py
      ```

## Requirements
The project dependencies are listed in `requirements.txt`:

```txt
beautifulsoup4==4.12.3
certifi==2024.2.2
charset-normalizer==3.3.2
idna==3.7
numpy==1.26.4
pandas==2.2.2
python-dateutil==2.9.0.post0
pytz==2024.1
requests==2.32.2
six==1.16.0
soupsieve==2.5
tzdata==2024.1
urllib3==2.2.1
```

## License
This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.
