import requests
from bs4 import BeautifulSoup
import csv
import pandas

# URL of the University of Maryland's approved courses page
url = 'https://academiccatalog.umd.edu/undergraduate/approved-courses/'

# Send a GET request to the page
response = requests.get(url)
response.raise_for_status()  # Check that the request was successful

# Parse the HTML content of the page
soup = BeautifulSoup(response.content, 'html.parser')

# Dictionary to hold course prefixes and their full forms
course_dict = {}

# Find all course prefixes and their descriptions
course_letters = soup.find('ul', class_='letternav clearfix')
course_letters = course_letters.find_all('li')
course_letters = [letter.text for letter in course_letters]

all_course_prefixes = soup.find('div', class_='az_sitemap')
all_course_prefixes = all_course_prefixes.find_all('li')
all_course_prefixes = [course.text for course in all_course_prefixes]

course_prefixes = [entry for entry in all_course_prefixes if entry not in course_letters]

def separate_course_prefix(full_course_prefix: str):
    words = full_course_prefix.split(' - ')
    return words[0], words[1]


with open('umd_course_prefixes.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Course Prefix', 'Full Form'])

    for entry in course_prefixes:
        course_prefix, full_form = separate_course_prefix(entry)
        writer.writerow([course_prefix, full_form])

print('Data successfully written to umd_course_prefixes.csv')


# URL of the University of Maryland's approved courses page
url = 'https://app.testudo.umd.edu/soc/'

# Send a GET request to the page
response = requests.get(url)
response.raise_for_status()  # Check that the request was successful

# Parse the HTML content of the page
soup = BeautifulSoup(response.content, 'html.parser')

# Dictionary to hold course prefixes and their full forms
course_dict = {}

# Find all course prefixes and their descriptions
course_prefixes = soup.find_all('div', class_='course-prefix row')

with open('umd_course_prefixes.csv', 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    df = pandas.read_csv('umd_course_prefixes.csv')
    existing_course_prefixes = set(df["Course Prefix"])

    for entry in course_prefixes:
        course_prefix = entry.find('span', class_='prefix-abbrev push_one two columns').text.strip()

        if course_prefix not in existing_course_prefixes:
            full_form = entry.find('span', class_='prefix-name nine columns').text.strip()
            writer.writerow([course_prefix, full_form])

print('Data successfully appended to schedule_course_prefixes.csv')

