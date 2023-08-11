

import asyncio
from asyncio.windows_events import NULL
from datetime import datetime
from pathlib import Path
import os
from random import randint
from random import choices
import random
import string

# External Packages
import pandas as pd
from collections import deque
from dotenv import load_dotenv

# Local Imports
from fetch import fetch_from_url
from util_logger import setup_logger
from book_price import get_book_price
# Set up a file logger
logger, log_filename = setup_logger(__file__)

NY_TIMES_BOOK_API_KEY = "NY_TIMES_BOOK_API_KEY"

def get_API_key(keyName):
    # Keep secrets in a .env file - load it, read the values.
    # Load environment variables from .env file
    load_dotenv()
    key = os.getenv(keyName)
    return key
async def update_csv_book():
    """Update the CSV file with the latest location information."""
    logger.info("Calling update_csv_book")
    try:
        #book_api = f"https://api.nytimes.com/svc/books/v3/lists/full-overview?api-key={get_API_key(NY_TIMES_BOOK_API_KEY)}" #Gets the current best sellers
        book_api = f"https://api.nytimes.com/svc/books/v3/lists/full-overview?published_date=2013-05-22&api-key={get_API_key(NY_TIMES_BOOK_API_KEY)}" #Gets the best sellers that week 
        result = await fetch_from_url(book_api, "json")
        update_interval = 60  # Update every 1 minute (60 seconds)
        total_runtime = 15 * 60  # Total runtime maximum of 15 minutes
        num_updates = 100  # Keep the most recent 10 readings
        logger.info(f"update_interval: {update_interval}")
        logger.info(f"total_runtime: {total_runtime}")
        logger.info(f"num_updates: {num_updates}")

        # Use a deque to store just the last, most recent 10 readings in order
        records_deque = deque(maxlen=num_updates)

        file_path = Path(__file__).parent.joinpath("data").joinpath("book.csv")

        # Check if the file exists, if not, create it with only the column headings
        if not os.path.exists(file_path):
                df_empty = pd.DataFrame(
                columns=["Title", "Author", "Price", "Rank", "Time", "Publication Date", "ISBN"] 
                )
                df_empty.to_csv(file_path, index=False)    

        logger.info(f"Initialized csv file at {file_path}")

        for _ in range(num_updates):  # To get num_updates readings
            for book in range(len(result.data["results"]["lists"][0]["books"])):
                title = result.data["results"]["lists"][0]["books"][book]["title"]
               
                author = result.data["results"]["lists"][0]["books"][book]["author"]
             
                rank = result.data["results"]["lists"][0]["books"][book]["rank"]
                
                isbn = result.data["results"]["lists"][0]["books"][book]["primary_isbn10"]
             
                if isbn == "" or isbn == "None":
                    isbn = result.data["results"]["lists"][0]["books"][book]["primary_isbn13"]
                
                price = get_book_price(isbn)
          
                pubDate = result.data["results"]["lists"][0]["books"][book]["created_date"][0:10]
                
                time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Current time
                new_record = {
                    "Title": title,
                    "Author": author,
                    "Price": price,
                    "Rank": rank,
                    "Time": time_now,
                    "Publication Date": pubDate,
                    "ISBN": isbn
                }
                records_deque.append(new_record)
            # Use the deque to make a DataFrame
            df = pd.DataFrame(records_deque)

            # Save the DataFrame to the CSV file, deleting its contents before writing
            df.to_csv(file_path, index=False, mode="w")
            logger.info(f"Saving books to {file_path}")

            # Wait for update_interval seconds before the next reading
            await asyncio.sleep(update_interval)

    except Exception as e:
        logger.error(f"ERROR in update_csv_book: {e}")



async def update_csv_bookNoAPI():
    """Update the CSV file with the latest location information."""
    logger.info("Calling update_csv_book")
    try:
        update_interval = 60  # Update every 1 minute (60 seconds)
        total_runtime = 15 * 60  # Total runtime maximum of 15 minutes
        num_updates = 100  # Keep the most recent 10 readings
        logger.info(f"update_interval: {update_interval}")
        logger.info(f"total_runtime: {total_runtime}")
        logger.info(f"num_updates: {num_updates}")

        # Use a deque to store just the last, most recent 10 readings in order
        records_deque = deque(maxlen=num_updates)

        file_path = Path(__file__).parent.joinpath("data").joinpath("book.csv")

        # Check if the file exists, if not, create it with only the column headings
        if not os.path.exists(file_path):
                df_empty = pd.DataFrame(
                columns=["Title", "Author", "Price", "Rank", "Time", "Publication Date", "ISBN"] 
                )
                df_empty.to_csv(file_path, index=False)    

        logger.info(f"Initialized csv file at {file_path}")

        for _ in range(num_updates):  # To get num_updates readings
            for book in range(10):
                title = ''.join(random.choices(string.ascii_letters, k=9))
                author = ''.join(random.choices(string.ascii_letters, k=9))
                rank = ''.join(random.choices(string.digits, k=1)) 
                isbn = ''.join(random.choices(string.digits, k=10))
                price = ''.join(random.choices(string.digits, k=2))
                pubDate = ''.join(random.choices(string.ascii_letters, k=9))
                time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Current time
                new_record = {
                    "Title": title,
                    "Author": author,
                    "Price": price,
                    "Rank": rank,
                    "Time": time_now,
                    "Publication Date": pubDate,
                    "ISBN": isbn
                }
                records_deque.append(new_record)
            # Use the deque to make a DataFrame
            df = pd.DataFrame(records_deque)

            # Save the DataFrame to the CSV file, deleting its contents before writing
            df.to_csv(file_path, index=False, mode="w")
            logger.info(f"Saving books to {file_path}")

            # Wait for update_interval seconds before the next reading
            await asyncio.sleep(update_interval)

    except Exception as e:
        logger.error(f"ERROR in update_csv_book: {e}")