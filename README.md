# Web Scraper for UMD Course Data

## Overview
The UMD Schedule Web Scraper project is designed to scrape course information from the University of Maryland's [Course Catalog](https://academiccatalog.umd.edu/undergraduate/approved-courses/) and [Schedule of Classes](https://app.testudo.umd.edu/soc/) websites. This project is structured into several directories, each containing specific scripts that perform various tasks related to data scraping and validation.

In addition, it addresses the challenge of the unavailability of datasets regarding UMD courses. The lack of existing datasets prompted the need to create one, leading to the development of custom web scrapers. These scrapers are designed to form the datasets required for various projects and analyses.

## Citation Requirement
If you use any of the datasets or scripts from this project, you must cite the original author:
- Author: Arav Luthra

Please include the following citation in your work:

"Arav Luthra. UMD Schedule Web Scraper. https://github.com/aluthra23/UMD_Schedule_Web_Scraper/"


## Directory Structure

### Root Directory
- `constants.py`: Contains three arrays:
  - `Course Acronyms`: An array of course prefixes.
  - `Course Catalog CSV Header`: An array defining the CSV header for the course catalog scraper.
  - `Schedule of Classes CSV Header`: An array defining the CSV header for the schedule of classes scraper.
- `helper.py`: Contains helper methods for scraping in each directory.

- `check_websites_for_course_updates`
  - `course_catalog.py`: Contains methods to scrape and validate that the current course acronyms array in `constants.py` includes all course prefixes displayed on the course catalog website. Also includes the `ensure_no_extra_elements` method to ensure there are no extra elements in the course acronyms array.
  - `schedule_of_classes.py`: Contains methods to scrape and validate that the current course acronyms array in `constants.py` includes all course prefixes displayed on the schedule of classes website. Also includes the `ensure_no_extra_elements` method.
  - `main_check_both_websites.py`: Main script to run both `course_catalog.py` and `schedule_of_classes.py` to check and validate the course acronyms array against both websites.

- `course_catalog_scraper`
  - `main_catalog_scraper.py`: Calls the `scrape_course_data` method in `scraper.py` for each course prefix. This method scrapes the webpage for all courses under a specific course prefix and stores the information in a CSV file named `umd_catalog_courses.csv`.
  - `scraper.py`: Contains the `scrape_course_data` method which scrapes the following information for each course:

| COURSE PREFIX | COURSE NUMBER | NAME | CREDITS | DESCRIPTION | PREREQUISITE | RESTRICTION | FORMERLY NAMED | RECOMMENDED | CREDIT ONLY GRANTED FOR | REPEATABLE TO | CROSS-LISTED | COREQUISITE |
| ------------- | -------------- | ---- | ------- | ----------- | ------------ | ----------- | -------------- | ----------- | ------------------------ | ------------- | ------------ | ----------- |

  The scraped data is stored in `umd_catalog_courses.csv`.

- `course_prefixes_dataset_creation`
  - `main_prefix_scraper.py`: Visits the course catalog and schedule of classes webpages to scrape the course prefixes and their full forms. The data is stored in a CSV file named `umd_course_prefixes.csv`.

- `schedule_of_classes_scraper`
  - `main_soc_scraper.py`: Calls the `scrape_course_data` method in `soc_scraper.py` for each course acronym. This method scrapes the schedule of classes webpage and stores the following information for each class under each course prefix:

| COURSE NUMBER | COURSE TITLE | MINIMUM CREDITS | MAXIMUM CREDITS | GRADING METHOD | SECTION ID | INSTRUCTOR | TOTAL SEATS | OPEN SEATS | WAITLIST COUNT | LECTURE TIME | DISCUSSION TIME | LAB TIME | UNSPECIFIED TIME MESSAGE | HAS LECTURE | HAS DISCUSSION | HAS LAB | IS NORMAL | IS BLENDED (NORMAL AND ONLINE) | IS ONLINE | SPECIAL RESTRICTION | PREREQUISITE | COREQUISITE | RESTRICTION | CREDIT ONLY GRANTED FOR | FORMERLY | RECOMMENDED | CROSS-LISTED WITH | DESCRIPTION |
| ------------- | ------------- | --------------- | --------------- | -------------- | ---------- | ---------- | ----------- | ---------- | --------------- | ------------ | --------------- | -------- | ------------------------- | ----------- | -------------- | ------- | --------- | ---------------------------- | ---------- | ------------------ | ------------ | ----------- | ----------- | ------------------------ | -------- | ----------- | ----------------- | ----------- |

  The scraped data is stored in `class_sections.csv`.

## Setup Instructions
1. Clone the repository:
    ```sh
    git clone https://github.com/aluthra23/UMD_Schedule_Web_Scraper.git
    cd UMD_Schedule_Web_Scraper
    ```

2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

3. Run the scrapers:
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
