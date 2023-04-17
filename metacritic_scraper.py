# Import libraries
import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from multiprocessing import Pool
import asyncio
import sys
import csv
from datetime import datetime
import time
import pickle 

# Set scraper header
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

# Set session
session = requests.Session()

def get_page_soup(url):
    """
    Fetch a webpage and return its parsed HTML content.
    """
    response = session.get(url, headers=headers)
    response.raise_for_status()  # Check if the request was successful.
    soup = BeautifulSoup(response.text, "html.parser")
    return soup

def get_all_pages():
    """
    Get all the pages with the list of games by checking the "pagination" element.
    """
    base_url = "https://www.metacritic.com/browse/games/score/metascore/all/all/filtered?sort=desc&page="
    pages = []
    current_page = 0

    while True:
        try:
            page_url = base_url + str(current_page)
            soup = get_page_soup(page_url)
            pagination = soup.find("ul", class_="pages")
            if not pagination:
                break
            pages.append(soup)
            current_page += 1
        except Exception as e:
            print (f"{e}")
            time.sleep(5)
    return pages

def get_rating(page):
    try:
        rating = (page
                    .find("div", class_="metascore_w large game positive")
                    .get_text(strip=True))
    except:
        try:
            rating = (page
                        .find("div", class_="metascore_w large game mixed")
                        .get_text(strip=True))
        except:
            rating = (page
                        .find("div", class_="metascore_w large game negative")
                        .get_text(strip=True))
    return rating

def get_user_rating(page):
    try:
        rating_u = (page
                    .find("div", class_="metascore_w user large game positive")
                    .get_text(strip=True))
    except:
        try:
            rating_u = (page
                        .find("div", class_="metascore_w user large game mixed")
                        .get_text(strip=True))
        except:
            try:
                rating_u = (page
                        .find("div", class_="metascore_w user large game negative")
                        .get_text(strip=True))
            except:
                rating_u = np.NaN
    return rating_u

def extract_game_data(page):
    """
    Extract game information from a BeautifulSoup object containing a page's HTML content.
    """
    game_data = []
    for page in page.find_all("table"):
        for page in page.find_all("tr"):
            try:
                number = page.find("span", class_="title numbered").get_text(strip=True)
                name = page.find("a", class_="title").get_text(strip=True)
                platform = page.find("span", class_="data").get_text(strip=True)
                rating = get_rating(page)
                rating_u = get_user_rating(page)
                release_date = page.find_all("span")[4].get_text(strip=True)
                summary = page.find("div", class_="summary").get_text(strip=True)
                game_data.append([number, name, platform, rating, rating_u, release_date, summary])
                #print (f'{number}|{name}|{platform}|{rating}|{rating_u}|{release_date}|{summary}')
            except:
                pass
    return game_data

def get_current_ts():
    return datetime.now().strftime('%Y_%m_%d_%H_%M_%S')

def write_pickle_obj(object_pi, fl_path):
    """
    Writes an object to a file in pickle format.

    Parameters:
    object_pi (object): the object to be written to the file
    fl_path (str): the path to the file where the object will be written

    Returns:
    None
    """    
    # open the file in write binary mode
    with open(fl_path, 'wb') as file_pi:
        # write the object to the file in pickle format
        pickle.dump(object_pi, file_pi)

def read_pickle_obj(fl_path):
    """
    Reads an object from a file in pickle format.

    Parameters:
    fl_path (str): the path to the file where the object is stored

    Returns:
    object: the object read from the file
    """
    # open the file in read binary mode
    with open(fl_path, 'rb') as filehandler:
        # read the object from the file in pickle format
        object_pi = pickle.load(filehandler)
    # return the object
    return object_pi


# Scrape all pages
pages = get_all_pages()
# Save pages read as pickle object
write_pickle_obj([str(x) for x in pages],"data\\pages.obj")  

pages = [BeautifulSoup(x,"html.parser") for x in  read_pickle_obj(f"data\\pages.obj")]

#Scrape all game data from Metacritic and return the data as a list of dictionaries.
all_game_data = []

for page in pages:
    game_data = extract_game_data(page)
    all_game_data.append(game_data)

all_game_data = sum(all_game_data, [])

# Get game data in a dataframe
all_game_dataframe = pd.DataFrame(all_game_data, columns=["index", "name", "platform", "metacritic", "user_rating", "release_date", "summary"])

# Write to csv
all_game_dataframe.to_csv(f"data\\{get_current_ts()}_metacritic.csv",quoting=csv.QUOTE_ALL,index=False)

