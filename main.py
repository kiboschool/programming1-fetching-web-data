from bs4 import BeautifulSoup
import requests

# Constant Values
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
           'Accept-Language': 'en-US, en;q=0.5'
}

amzn_webpage_link = 'https://tinyurl.com/2mn2tb4c'
flipkart_webpage_link = 'https://tinyurl.com/2atd9rr4'

def amzn_product_list(amzn_webpage_link: str):
    response = requests.get(amzn_webpage_link, headers=headers)

    if response.status_code == 200 or response.status_code == 201:
        content = response.text
        soup = BeautifulSoup(content, "html.parser")
        for i, name in enumerate(soup.findAll('span', attrs={'class':'a-size-medium a-color-base a-text-normal'})):
            print(f"[Laptop {i}]: {name.get_text()}\n")
    else:
        print(f'Failed to access webpage with error {response.status_code}')


def flipkart_product_list(flipkart_webpage_link):
    response = requests.get(flipkart_webpage_link, headers=headers)

    if response.status_code == 200 or response.status_code == 201:
        content = response.text
        soup = BeautifulSoup(content, "html.parser")
        for i, name in enumerate(soup.findAll('div', attrs={'class':'_4rR01T'})):
            print(f"[Laptop {i}]: {name.get_text()}\n")
    else:
        print(f'Failed to access webpage with error {response.status_code}')


def fetch_products():
    print('Amazon Laptop Filter:\n')
    amzn_product_list(amzn_webpage_link=amzn_webpage_link)
    print('Flipkart Laptop Filter:\n')
    flipkart_product_list(flipkart_webpage_link=flipkart_webpage_link)

if __name__ == '__main__':
    fetch_products()