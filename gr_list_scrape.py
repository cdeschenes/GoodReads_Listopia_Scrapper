import csv
import requests
import re
from bs4 import BeautifulSoup

# base_url = 'https://www.goodreads.com/list/show/1840.Best_Post_Apocalyptic_Fiction?page='
base_url = 'https://www.goodreads.com/list/show/16961.Best_Weird_Fiction_Books?page='
page_number = 1
book_list = []

# Fetch the first page to extract the title for the CSV filename
response = requests.get(base_url + str(page_number))
soup = BeautifulSoup(response.text, 'html.parser')
title = soup.title.string
clean_title = re.sub(r'[\\/*?:"<>|]', '', title.split("|")[0].strip())
csv_filename = clean_title + '.csv'

while True:
    url = base_url + str(page_number)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract book details from the page
    for row in soup.find_all('tr', attrs={'itemtype': 'http://schema.org/Book'}):
        title_tag = row.find('span', itemprop='name')
        author_tag = row.find('span', itemprop='author').find('span', itemprop='name')

        if title_tag and author_tag:
            title = title_tag.text.strip()
            author = author_tag.text.strip()
            book_list.append((title, author))

    # Check for the "next" link to see if there's another page to scrape
    next_link = soup.find('a', class_='next_page', rel='next')
    if next_link:
        page_number += 1
    else:
        # Exit the loop when there's no next page
        break

# Write the extracted data to a CSV file with the custom name
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile, quoting=csv.QUOTE_NONE, escapechar='\\')
    writer.writerow(['Title', 'Author']) # Header
    writer.writerows(book_list)
