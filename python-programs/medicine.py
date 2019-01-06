"""
Used to get data for medicine_data.json

Not meant to be used in Django project but as a backup
Example:
    "M": {
        "MELANOCYL TAB 40":
            {
                "power": "",
                "category": "Ethical Drugs",
                "manufacturer": "FRANCO-INDIA PHARMA.P.LTD-001",
                "price": "382.6",
                "product_type": "TABLETS",
                "product": "TABLETS",
                "quantity": "40"
            }
        }
"""

from bs4 import BeautifulSoup
import requests
import json


def get_info_from_web(url):
    r = requests.get(url)
    try:
        soup = BeautifulSoup(r.content, 'html.parser')
        manufacturer = soup.find('span', {'id': 'ctl00_MainContent_lblManufacturer'}).get_text()
        product_type = soup.find('span', {'id': 'ctl00_MainContent_lblProductType'}).get_text()
        category = soup.find('span', {'id': 'ctl00_MainContent_lblCategoryName'}).get_text()
        power = soup.find('span', {'id': 'ctl00_MainContent_LabelPower'}).get_text()
        quantity = soup.find('span', {'id': 'ctl00_MainContent_lblQuntity'}).get_text()
        product = soup.find('span', {'id': 'ctl00_MainContent_lblProduct'}).get_text()
        price = soup.find('span', {'id': 'ctl00_MainContent_lblOurMRP'}).get_text()
    except:
        print('Error with: ' + url)
        return {'error': ''}

    return {'manufacturer': manufacturer,
            'product_type': product_type,
            'category': category,
            'power': power,
            'quantity': quantity,
            'product': product,
            'price': price}


def get_medicine_from_web(url):
    real_data = {}
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    l = soup.find_all('div', {'class': 'animationDiv'})
    for div in l:
        med_name = div.getText().strip().replace('  ', ' ')
        link = div.find('a')['href'].replace('%', '').replace('+', '').replace(':', '').replace('&', '').replace('*', '')
        temp_data = get_info_from_web('http://www.arogyaretail.com/' + link)
        real_data[med_name] = temp_data
    return real_data


print('Starting ...')
total_medicine = 0
main_data = {}
for ordinate in range(65, 91):
    print('Scraping - ' + chr(ordinate) + ' Count | ' + str(total_medicine))
    tem_data = get_medicine_from_web('http://www.arogyaretail.com/items.aspx?Search=' + chr(ordinate))
    total_medicine += len(tem_data)
    main_data[chr(ordinate)] = tem_data

print('\n\nTotal: ' + str(total_medicine))
with open('medicine_data.json', 'w') as fp:
    json.dump(main_data, fp)
