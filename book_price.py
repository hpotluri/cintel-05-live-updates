import requests
from dotenv import load_dotenv
import os

GOOGLE_BOOK_API = "GOOGLE_BOOK_API"

def get_API_key(keyName):
    # Keep secrets in a .env file - load it, read the values.
    # Load environment variables from .env file
    load_dotenv()
    key = os.getenv(keyName)
    return key

def get_book_price(isbn):
    url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}&key={get_API_key(GOOGLE_BOOK_API)}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        if 'items' in data and len(data['items']) > 0:
            book_info = data['items'][0]
            
            if 'saleInfo' in book_info and 'listPrice' in book_info['saleInfo']:
                price_info = book_info['saleInfo']['listPrice']
                if 'amount' in price_info and 'currencyCode' in price_info:
                    return f"{price_info['amount']} {price_info['currencyCode']}"
    
    return "Price information not found"

# Example ISBN for a book
isbn = "9781423140344"

book_price = get_book_price(isbn)
if book_price != "Price information not found":
    print(f"Book Price: {book_price}")
else:
    print("Book price information not available.")
