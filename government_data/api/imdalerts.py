import requests

from bs4 import BeautifulSoup


def earthquake_status(year):
    r = requests.get('http://www.imd.gov.in/pages/lyear2.php?year=' + str(year))
    soup = BeautifulSoup(r.content, 'html.parser')
    table_rows = soup.find_all('tr')
    title = table_rows[0].text
    headers = [i.text.strip() for i in table_rows[1].find_all('th')]
    final_dict = []
    for data in table_rows[2:]:
        words = data.find_all('td')
        filtered_data = [i.text.strip() for i in words[:-1]]
        filtered_data += ['http://www.imd.gov.in' + words[-1].a['href'][2:]]
        final_dict.append(dict(zip(headers, filtered_data)))
    return final_dict


# TODO: Not high priority: Complete all functions
def weather_status(year):
    # http://www.imd.gov.in/section/nhac/dynamic/allindiasevere.pdf
    pass


def cyclone_status(year):
    # http://www.rsmcnewdelhi.imd.gov.in/images/bulletin/rsmc.pdf
    pass


def monsoon_status(year):
    # http://hydro.imd.gov.in/hydrometweb/(S(txuqot2bqtshih3alobtxa45))/landing.aspx#
    pass
