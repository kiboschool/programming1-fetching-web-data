from bs4 import BeautifulSoup
import requests
import csv, os, sys

# Constant Values - No need to change
base_url = 'https://www.jumia'
needed_product = 'laptops'
specs = {
        'brand': ['hp', 'lenovo'],
        'cpu_speed': '3',
        'seller_score': '4-5',
        'rating': '4-5'
        }

# Used to run over all supported countries in our scraper
registered_country_codes = {'Nigeria': 'ng',
                            'Tunisia': 'tn',
                            'Kenya': 'ke',
                            'Uganda': 'ug', 
                            'Senegal': 'sn'}

# Use this in building your URL
com_domain_country_codes = ['ng', 'tn']
co_domain_country_codes = ['ke']
no_domain_country_codes = ['ug', 'sn']
        

def fetch_product_data(country_code, filter, product_name, brand): # TODO: Implement fetch_product_data function
    """
    Access Jumia webpage constructed link and returns a dictionary where key is product name and value is product price
    Procedure:
    1) Construct proper URL based on functions inputs -> check your generated URL using a browser
    2) Perform a GET request and check status code for the response -> Handle failing coded witha a suitable statment
    3) Use Beautiful Soup to fetch list of products and a list of prices
    4) Create a dictionary with suitable <Product, Price> pairs.

    :param country_code: Country code according to Jumia website
    :param filter: a dictionary for all needed parameters in get request for Jumia
    :param product_name: product that we need to search for using Jumia (laptops in our case)
    :param brand: list of brans that need to filter for -- format needs to be suitable for jumia link
    :return: dictionary of <'product': 'price'> pairs in case of available products. None in case of no available products.

    """
    product_info = {}
    
    if country_code in com_domain_country_codes:
        country_base_url = f"{base_url}.com"
    elif country_code in co_domain_country_codes:
        country_base_url = f"{base_url}.co"
    elif country_code in no_domain_country_codes:
        country_base_url = f"{base_url}"
    else:
        print(f"Country code {country_code} is not supported!")
        return None

    if brand:
        url = f"{country_base_url}.{country_code}/{product_name}/{brand}/?{filter}"
    else:
        url = f"{country_base_url}.{country_code}/{product_name}/?{filter}"
    
    print(f'Generated URL for country code [{country_code}] -> {url}')
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
            print(f'Failed to find needed data for country code [{country_code}] -> check your specs or generated URL')
            return None
    else:
        print(f'Failed to access webpage with error code: {response.status_code}')
        return None
    
    return product_info


def build_specs(): # Implemented - No need to change
    """
    Access global predefined specifications and returns needed request parameters with suitable format.
    """
    filter = {k: specs[k] for k in specs.keys() - {'brand'}}
    return ("&".join(f'{k}={v}' for k,v in filter.items()))

def build_brands(): # Implemented - No need to change
    """
    Access global predefined brand list and returns needed brands with suitable format.
    """
    if specs.get('brand'):
        return ("--".join(i for i in specs.get('brand')))
    else:
        return None

def save_to_file(country, data): # TODO: Implement save to file 
    """
    Opens a csv file and saves each country's data.
    :param country: Country Name
    :param country: Product data dictionary for the specified country
    """
    with open(file='fetched_products.csv', mode='a', newline='', encoding='UTF-8') as result_file:
        writer = csv.writer(result_file)
        writer.writerow([country])
        for product, price in data.items():
            writer.writerow([product, price])

def run_scraper(filename): # Implemented - No need to change
    """
    Triggers the whole procedure of scraping.
    Procedure:
    1) Loop over supported countries
    2) Try fetching data for each country webpage
    3) Check returned data and save it to file if relevant

    :param filename: File name specified by user -> input argument
    """
    if os.path.exists(filename):
        os.remove(filename)
    for country, country_code in registered_country_codes.items():
        data = fetch_product_data(country_code=country_code, 
                            filter=build_specs(), 
                            product_name=needed_product, 
                            brand=build_brands())

        if data:
            print(f'Fetched data for {country} is {data}\n')
            save_to_file(country=country, data=data)
        else:
            print(f'No available data for {country}\n')

if __name__ == '__main__':
    if len(sys.argv) == 2:
        run_scraper(sys.argv[1])
    else:
        print("Usage: python3 main.py 'your file name'")