Title: Metacritic Game Scraper

Description: A Python script to scrape game data from Metacritic (https://www.metacritic.com/).

## Disclaimer
This project is for educational purposes only. By using this script, you take full responsibility for any actions you perform using the data scraped. The author is not responsible for any misuse of the script or any violations of Metacritic's terms of service.

Before using this script, please ensure you have permission to scrape the Metacritic website and follow their guidelines and rate limits to avoid causing issues. This script is provided under the MIT License (https://opensource.org/licenses/MIT), which allows for free use, modification, and distribution of the code, but does not hold the author liable for any damages or legal issues arising from its use.

## Overview
This Python script uses the requests and BeautifulSoup libraries to scrape game data from Metacritic's website. The script extracts information such as game title, platform, Metacritic score, user rating, release date, and a summary of the game.

## Dependencies
```
requests
BeautifulSoup4
numpy
pandas
multiprocessing
asyncio
sys
csv
datetime
time
pickle
```

## Code Explanation
The script defines several functions to perform various tasks:

`get_page_soup(url)`: Fetches a webpage and returns its parsed HTML content.
`get_all_pages()`: Fetches all the pages with the list of games by checking the "pagination" element.
`get_rating(page)`: Extracts the Metacritic rating from a given page.
`get_user_rating(page)`: Extracts the user rating from a given page.
`extract_game_data(page)`: Extracts game information from a BeautifulSoup object containing a page's HTML content.
get_current_ts(): Returns a timestamp string to be used in file names.
write_pickle_obj(object_pi, fl_path): Writes an object to a file in pickle format.
read_pickle_obj(fl_path): Reads an object from a file in pickle format.
The script performs the following steps:

Fetches all the pages containing game listings using the get_all_pages() function.
Stores the fetched pages as pickle objects to avoid re-fetching them later.
Reads the stored pages from pickle files and converts them back to BeautifulSoup objects.
Extracts game information from each page using the extract_game_data() function.
Combines the extracted data from all pages into a single list and converts it into a pandas DataFrame.
Writes the DataFrame to a CSV file.
Usage
Install the required dependencies using pip install requests beautifulsoup4 numpy pandas.
Run the script with python metacritic_scraper.py.
The script will create a CSV file containing the game data in the "data" folder with a timestamp in its name.
License
This project is licensed under the MIT License, which allows for free use, modification, and distribution of the code, but does not hold the author liable for any damages or legal issues arising from its use.
