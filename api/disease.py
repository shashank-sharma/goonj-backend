# Pdfplumber is used for graphical pdf extraction, like we can use table lines
# to separate table and then get our text in structured format
import pdfplumber
import requests

from bs4 import BeautifulSoup
from pathlib import Path


import os.path


# Table settings for pdf extraction
table_settings = {
    "vertical_strategy": "lines",
    "horizontal_strategy": "lines",
    "intersection_y_tolerance": 505,
    "keep_blank_chars": False,
    "snap_tolerance": 5,
    "edge_min_length": 50
}


def extract_pdf_to_dict(file):
    pdf = pdfplumber.open(file)
    pages = pdf.pages
    final_data = []

    for page in pages:
        table = page.extract_table(table_settings)
        data = list(filter(lambda x: x, [[tup for tup in sub_list if sub_list[0] and sub_list[0].count('/') == 4] for sub_list in table]))
        filtered_data = [[word.replace(' \n', ' ').replace('\n', ' ').replace('  ', ' ')
                          for word in line if word] for line in data]

        for data in filtered_data:
            data = data + ['Not Available'] * 3
            if len(data) >= 7:
                final_data.append({
                    'Unique Id': data[0],
                    'Name of State/UT': data[1],
                    'Name of District': data[2],
                    'Disease': data[3],
                    'No. of Cases': data[4],
                    'No. of Deaths': data[5],
                    'Date of Start of Outbreak': data[6],
                    'Date of Reporting': data[7],
                    'Current Status': data[8],
                    'Comments': data[9]
                })
    return final_data


def get_all_pdf():
    r = requests.get('https://idsp.nic.in/index4.php?lang=1&level=0&linkid=406&lid=3689', verify=False)
    soup = BeautifulSoup(r.content, 'html.parser')
    l = soup.find('div', {'id': 'cmscontent'})
    html_table = l.find_all('tr')

    real_data = {}
    for table_row in html_table[1:]:
        table_data = table_row.find_all('td')
        year = table_data[0].text.strip()
        real_data[year] = []

        links = table_data[1].find_all('a')
        for link in links:
            real_data[year].append(link['href'])

    return real_data


def download_pdf(url, new=False):
    filename = 'static/disease/' + url.split('/')[-1]
    if not os.path.isfile(filename):
        filename_path = Path(filename)
        r = requests.get(url, verify=False)
        filename_path.write_bytes(r.content)
    return filename
