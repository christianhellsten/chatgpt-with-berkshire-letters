"""
Downloads Berkshire letters to disk.
"""
import os
import time
import requests
import logging
from bs4 import BeautifulSoup
from urllib.parse import urlparse

logging.basicConfig(level=logging.INFO)

URL = "https://www.berkshirehathaway.com/letters"
PROXY = None # "http://142.132.225.143:8080"

def download_files(base_url, save_dir='letters', file_types=['.pdf', '.html'], timeout=(5, 10), proxy=None):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    }
    proxies = {
        'http': proxy,
        'https': proxy
    } if proxy else None

    url = f"{base_url}/letters.html"
    try:
        response = requests.get(url, headers=headers, timeout=timeout, proxies=proxies)
        if response.status_code != 200:
            raise Exception(f"Expected HTTP 200 not {response.status_code}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Request error: {e}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find('table', class_='MsoNormalTable')
    if not table:
        logging.warning("Table not found.")
        return

    for link in table.find_all('a'):
        href = link.get('href')
        if not href:
            continue

        file_ext = os.path.splitext(href)[1]
        if file_ext in file_types:
            file_url = f"{base_url}/{href}"
            file_name = os.path.basename(href)
            file_path = os.path.join(save_dir, file_name)
            if os.path.exists(file_path):
                logging.info(f"Already downloaded. Skipping: {file_url}")
                continue

            time.sleep(1)
            try:
                file_response = requests.get(file_url, headers=headers, timeout=timeout)
            except requests.exceptions.RequestException as e:
                logging.error(f"Request error: {e}")
                continue

            if not os.path.exists(save_dir):
                os.makedirs(save_dir)

            with open(file_path, 'wb') as f:
                f.write(file_response.content)

            logging.info(f"Downloaded: {file_name}")

if __name__ == "__main__":
    download_files(URL, save_dir='letters', proxy=PROXY)
