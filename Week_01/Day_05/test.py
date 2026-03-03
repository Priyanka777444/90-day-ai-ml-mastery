import requests
from bs4 import BeautifulSoup

#step1: fetch a webpage
url = "https://books.toscrape.com/"
response = requests.get(url)

print("Status Code:", response.status_code) 
print("First 500 characters:", response.text[:500])

#step 2 parse html
soup = BeautifulSoup(response.text, 'html.parser')

#step 3 find element
#find first h1 tag
h1 = soup.find('h1')
print("H1 tag:", h1)

#find all articles
arti = soup.find_all('article', class_='product_pod')
print(f"Found {len(arti)} products")

#extract data from first product 
f_prod = arti[0]

#find title
title = f_prod.find('h3').find('a')['title']
print("Title:" , title)

#find price
price = f_prod.find('p', class_='price_color').text
print("Price:", price)

# Find rating
rat = f_prod.find('p', class_='star-rating')['class'][1]
print("Rating:", rat)