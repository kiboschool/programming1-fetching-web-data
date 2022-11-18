from bs4 import BeautifulSoup
import requests
import csv, os

# Constant Values
base_url = 'https://www.jumia'

specs = {
        'brand': ['hp', 'lenovo'],
        'cpu_speed': '3',
        'seller_score': '4-5',
        'rating': '4-5'
        }

registered_country_codes = {'Nigeria': 'ng',
                            'Tunisia': 'tn',
                            'Kenya': 'ke',
                            'Uganda': 'ug'}

# registered_country_codes = {'Kenya': 'ke'}

com_domain_country_codes = ['ng', 'tn']
co_domain_country_codes = ['ke']
no_com_domain_country_codes = ['ug']
                

needed_product = 'laptops'

def fetch_product_data(country_code, filter, product_name, brand):
    product_info = {}
    
    if country_code in com_domain_country_codes:
        country_base_url = f"{base_url}.com"
    elif country_code in co_domain_country_codes:
        country_base_url = f"{base_url}.co"
    elif country_code in no_com_domain_country_codes:
        country_base_url = f"{base_url}"
    else:
        print(f"Country code {country_code} is not supported!")
        return None

    if brand:
        url = f"{country_base_url}.{country_code}/{product_name}/{brand}/?{filter}"
    else:
        url = f"{country_base_url}.{country_code}/{product_name}/?{filter}"
    
    print(f'Generated URL -> {url}\n')
    response = requests.get(url)

    if response.status_code == 200 or response.status_code == 201:
        content = response.text
        soup = BeautifulSoup(content, "html.parser")

        product_lst = soup.findAll('h3', attrs={'class':'name'})
        price_lst = soup.findAll('div', attrs={'class':'prc'})

        if product_lst and price_lst:
            for product_idx in range(0, len(product_lst)):
                if price_lst[product_idx]:
                    product_info[product_lst[product_idx].get_text()] = price_lst[product_idx].get_text()
                else:
                    product_info[product_lst[product_idx].get_text()] = 'NA'
        else:
            print(f'Failed to find needed data -> check your specs or generated URL')
            return None
    else:
        print(f'Failed to access webpage with error code: {response.status_code}')
        return None
    
    return product_info


def build_specs():
    filter = {k: specs[k] for k in specs.keys() - {'brand'}}
    return ("&".join(f'{k}={v}' for k,v in filter.items()))

def build_brands():
    if specs.get('brand'):
        return ("--".join(i for i in specs.get('brand')))
    else:
        return None

def save_to_file(country, data):
    with open(file='fetched_products.csv', mode='a', newline='', encoding='UTF-8') as result_file:
        writer = csv.writer(result_file)
        writer.writerow([country])
        for product, price in data.items():
            writer.writerow([product, price])

def run_scraper():
    if os.path.exists('fetched_products.csv'):
        os.remove('fetched_products.csv')
    for country, country_code in registered_country_codes.items():
        data = fetch_product_data(country_code=country_code, 
                            filter=build_specs(), 
                            product_name=needed_product, 
                            brand=build_brands())

        if data:
            print(f'Fetched data for {country} is {data}\n')
            save_to_file(country=country, data=data)
        else:
            print(f'No available data for {country}')

if __name__ == '__main__':
    run_scraper()