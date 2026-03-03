"""
Build by Priyanka
web_scrapper
"""

import requests
from bs4 import BeautifulSoup
import csv
from datetime import time , datetime

scrap = [] #for scrabed data

def scrap_book():
    """Scrab the data from books.toscrab.com"""
    print("Scrabing Books")

    url = "http://books.toscrape.com/"

    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        #find all books container
        books = soup.find_all('article', class_ = 'product_pod') 

        print(f"Found {len(books)} books")

        for book in books:
            #extract title
            title = book.find('h3').find('a')['title']

            #extract price
            price = book.find('p', class_='price_color').text

            #extract rating
            rating = book.find('p', class_ = 'star-rating')['class'][1]

            #store
            book_data = {
                'title': title,
                'pricing' : price,
                'rating' : rating,
                'scrabbed_at': str(datetime.now())
            }

            scrap.append(book_data)
            print(f"✓ {title} - {price}")

            print(f"\nScraped {len(books)} books successfully!")
    except requests.exceptions.RequestException as e:
        print(f"Error {e}")

def scrap_quotes():
    """Scrab the data from qoutes.toscrab.com"""
    print("Scrabing Quotes")

    url = "http://quotes.toscrape.com/"

    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        #find all quotes container
        quotes = soup.find_all('div', class_ = 'quote') 

        print(f"Found {len(quotes)} books")

        for quote in quotes:
            #extract quote
            text = quote.find('span', class_ = 'text').text

            #extract author name
            author = quote.find('small', class_='author').text

            #extract tags
            tags = quote.find_all('a', class_ = 'tag')
            t = ', '.join([tag.get_text() for tag in tags])

            #store
            q_data = {
                'quote': text,
                'author' : author,
                'tags' : t,
                'scrabbed_at' :str(datetime.now())
            }

            scrap.append(q_data)
            print(f"✓ {author} - {text[:50]}")

            print(f"\nScraped {len(quotes)} Quotes successfully!")
    except requests.exceptions.RequestException as e:
        print(f"Error {e}")

def view():
    """View scrabbed data"""

    if len(scrap) == 0:
        print("No data to show!")
        return
    
    for i, item in enumerate(scrap, 1):
        print(f"\n{i}.")
        
        # Check what type of item it is
        if 'title' in item:  # It's a book
            print(f"  Type: Book")
            print(f"  Title: {item['title'][:50]}")
            print(f"  Price: {item['pricing']}")
            print(f"  Rating: {item['rating']}")
        
        elif 'quote' in item:  # It's a quote
            print(f"  Type: Quote")
            print(f"  Text: {item['quote'][:70]}...")
            print(f"  Author: {item['author']}")
            print(f"  Tags: {item['tags']}")
    
    print("-" * 80)


def save_csv():
    """Save the data to csv"""
    global scrap

    if len(scrap) ==0:
        print("Their is no data available here")
        return
     
    #Separate books and quotes
    books = [item for item in scrap if 'title' in item]
    quotes = [item for item in scrap if 'quote' in item]

    #books
    if books:
        filen = f"books_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"
        with open(filen , 'w', newline='', encoding='utf-8') as f:
            write = csv.DictWriter(f, fieldnames=['title', 'pricing', 'rating', 'scrabbed_at'])
            write.writeheader()
            write.writerows(books)

        print("All books are saved in the file")

    #save quotes
    if quotes:
        filen = f"quotes_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"
        with open(filen, 'w', newline='', encoding='utf-8') as f:
            write = csv.DictWriter(f, fieldnames=['quote', 'author', 'tags', 'scrabbed_at'])
            write.writeheader()
            write.writerows(quotes)
        print("All quotes are saved in the file")

    print(f"\nTotal items saved: {len(scrap)}") 


def main():
    print("Welcome to Web Scraper by Priyanka!")
    
    while True:
        print("\n1. Scrape Books")
        print("2. Scrape Quotes")
        print("3. View Scraped Data")
        print("4. Save to CSV")
        print("5. Exit")
        
        choice = input("\nEnter choice (1-5): ")
        
        if choice == "1":
            scrap_book()
        elif choice == "2":
            scrap_quotes()
        elif choice == "3":
            view()
        elif choice == "4":
            save_csv()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice!")

main()