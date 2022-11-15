from bs4 import BeautifulSoup
import requests

# Constant Values
base_url = 'https://www.jumia.com'
filter = {
            'display_size': '15.0--15.6',
            'operating_system': 'Windows+10',
            'price': '125000-285000',
            'hdd_size': '1000',
            'cpu_speed': '3.00--2.20'
            }

def fetch_product_data(country_code, filter, product_name):
    url = f"{base_url}.{country_code}/{product_name}/?{filter}"
    response = requests.get(url)

    if response.status_code == 200 or response.status_code == 201:
        content = response.text
        soup = BeautifulSoup(content, "html.parser")
        for i, name in enumerate(soup.findAll('h3', attrs={'class':'name'})):
            print(f"[Laptop {i}]: {name.get_text()}\n")
        for i, name in enumerate(soup.findAll('div', attrs={'class':'prc'})):
            print(f"[Laptop {i}]: {name.get_text()}\n")
    else:
        print(f'Failed to access webpage with error {response.status_code}')


def make_filter(filter_params):
    return ("&".join(f'{k}={v}' for k,v in filter.items()))

def save_to_file():
    pass

if __name__ == '__main__':
    # fetch_products()
    
    fetch_product_data(country_code='ng', filter=make_filter(filter_params=filter), product_name='laptops')