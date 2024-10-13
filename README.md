# Fetching Web Data

Python can fetch data from the web. The requests library makes it easier. In
this exercise, you'll practice making web requests using the library, and
handling the data.

## Your Task - Basic Web Scraper

Web scraping is a technique to pull data from a website automatically saving huge amount of time and effort. Web scraping examples could be:

- Generate a list of products
- Price comparison

In this project, you will apply web scraping to different country webpages from **Jumia** shopping platform. Your will be applying the same filter to different countries and generate a table that includes products and prices.

### Jumia Link Structure

In order to build suitable get requests, we need to take a closer look at how a Jumia link is structured. The general structure looks like:

> `<country_base_url>.<country_code>/<product_name>/<brand>/?<filter>`

- country_base_url: Refers to Jumia base url (`https://www.jumia`) + country related domain that could be **com**, **co**, or nothing.
- country_code: Each supported country at Jumia has a code. For instance, **Ghana** has the code of **gh**.
- product_name: Refers to the product we need to search for. In our case, it is **laptops**.
- brand: specifies product brand name if needed.
- filter: specifies needed values that we are filtering upon.

> Note: Most of these values are already given at our starter code.

### Filter

We will apply a **Laptop** product filter as follows:

- Brand: Lenovo & HP
- CPU Speed: 3
- Seller Score: 4-5
- Rating: 4-5

### Procedure

Web scraping procedure can change from site to site. We will use a general procedure to pull laptop product names and prices from **Jumia** after applying the mentioned filter.

General Procedure:

- Webpage Inspection
- Get Request
- Extract Tag Information

## Steps

As far as our procedure is considered, we will start with **webpage inspection** to obtain needed HTML tags, followed by **get request** to fetch webpage data, and finally **extract tag information** to extract information from fetched HTML tags.

### Webpage Inspection

Check the following video that shows how to inspect a Jumia webpage to extract product name.

[Web Inspection Video](https://www.loom.com/embed/ba42ec6a776f49e592ec2ac1240a8c38)

### Get Request

After understanding what tage(s) we are planning to fetch, we can then perform a get request to fetch page data:

> `response = requests.get(needed_webpage_link)`

Needed webpage link here is the URL that you constructed based on what is explained above.

### Extract Tag Data

We will use a library called [beautiful soup](https://pypi.org/project/beautifulsoup4/) to parse HTML data to extract infomration from our tags. Make sure to install it using `pip` and create an object as follows:

> `soup = BeautifulSoup(content, "html.parser")`
>
> `soup.findAll('<your_tag>', attrs={'<attribute_name>':'<value>'})`

`content` is the HTML code that we get in return while `findAll` function returns a list of all selected tags which you can then loop over to extract needed data.

> Note: You will get a list of HTML tags here --> check how to use the method `get_text()` to obtain internal tag data.

## Starter Code

Check the file called `main.py` for a starter code. You will find some import statements, function signatures, triggering command, and constant values you will need to use throughout implementation. Some of the helper functions are already implemented.

You need to implement two functions: `fetch_product_data` and `save_to_file` by using other implemented helper functions.

## Input Validation and Corner Cases

You should take care of the following cases:

- Response Status Code: When triggering a get request, make sure you check what status code you are receiving before you continue to parse received data.
- Empty product dictionary: Not all filters are supposed to generate products from all countries. For instance, You may get data from two countries out of four. Make sure that your code does not crash because of this, and try to print meaningful statements for skipped countries.
- Input filename: You should specify a **CSV** file name as an input. This file will include matched data only. In other words, country webpages who do not have matches should not push anything to the file.

## Testing

There are no tests for this project. You need to check your code agaist Jumia webpage itseld to check if you manage to generate a correct list of products and proces.

## Expected Results

An output example should look like the following:

```
Generated URL for country code [ng] -> https://www.jumia.com.ng/laptops/hp--lenovo/?cpu_speed=3&rating=4-5&seller_score=4-5
Fetched data for Nigeria is {'Hp ENVY X360 15 Intel Core I5(,8GB.512GB SSD)Touchscreen Backlit Keyboard Fingerprint': '₦ 625,500', 'Lenovo Ideapad 5 15ITLO5:Intel Core I5 -1135g7,512GB 8GB TOUCHSCREEN WINDOWS 11 BACKLIT': '₦ 420,000', 'Hp ENVY X360 15 10th Gen Intel Core I5(512GB SSD,8GB)Backlit Keyboard,Touch,FP, Wins 10': '₦ 625,000', 'Hp ENVY X360 15 10th Gen Intel Core I5(256GB SSD,8GB)Backlit Keyboard,Touch,FP, Wins 10': '₦ 609,500'}

Generated URL for country code [tn] -> https://www.jumia.com.tn/laptops/hp--lenovo/?cpu_speed=3&rating=4-5&seller_score=4-5
Failed to find needed data for country code [tn] -> check your specs or generated URL
No available data for Tunisia

Generated URL for country code [ke] -> https://www.jumia.co.ke/laptops/hp--lenovo/?cpu_speed=3&rating=4-5&seller_score=4-5
Fetched data for Kenya is {'HP Refurbished EliteBook 840 G4 Core I5 8GB 256GB SSD 14" Touchscreen 7th Gen Slim Laptop Mouse': 'KSh 31,850'}

Generated URL for country code [ug] -> https://www.jumia.ug/laptops/hp--lenovo/?cpu_speed=3&rating=4-5&seller_score=4-5
Failed to find needed data for country code [ug] -> check your specs or generated URL
No available data for Uganda

Generated URL for country code [sn] -> https://www.jumia.sn/laptops/hp--lenovo/?cpu_speed=3&rating=4-5&seller_score=4-5
Failed to find needed data for country code [sn] -> check your specs or generated URL
No available data for Senegal
```

> Notes:
>
> - Notice that we do not have any returned data for _Uganda_, _Tunisia_ and _Senegal_ using the this example filter.
> - Generated file should include data for _Nigeria_ and _Kenya_ only.
> - Check assets folder for an example output CSV file
