import csv
import requests
from bs4 import BeautifulSoup
import random
import time

# List of different user-agent strings
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.64',
    'Mozilla/5.0 (Linux; Android 11; Pixel 4 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36',
]

# url ="https://amzn.in/d/1SL1XUf"
# url ="https://www.bbc.com/news"
url ="https://www.bbc.com/news/articles/cdx921zreweo"

def get_random_user_agent():
    """Select a random user-agent from the list."""
    return random.choice(user_agents)


def scrape_headlines(url):
    """Scrape headlines from the given URL."""
    try:
        headers = {
            'User-Agent': get_random_user_agent()
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            headlines = soup.find_all(['h1', 'h2', 'h3'])
            return [headline.get_text(strip=True) for headline in headlines if headline.get_text(strip=True)]
        else:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")
            return []

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return []


def save_headlines_to_csv(data, filename):
    """Save headlines to a CSV file."""
    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Headline'])
            for row in data:
                writer.writerow([row])
        print(f"Saved {len(data)} unique headlines to '{filename}'")
    except Exception as e:
        print(f"Error saving to CSV: {e}")


def clean_headlines(headlines):
    """Remove duplicate headlines."""
    return list(set(headlines))


if __name__ == "__main__":
    # Scrape headlines from the page
    headlines = scrape_headlines(url)

    if headlines:
        print(f"Scraped {len(headlines)} headlines.")

        # Clean the data by removing duplicates
        cleaned_headlines = clean_headlines(headlines)

        # Save cleaned data to CSV
        save_headlines_to_csv(cleaned_headlines, 'headlines.csv')

        # Throttling: wait for a random amount of time before making another request
        time.sleep(random.uniform(1, 3))  # Random delay between 1 and 3 seconds
    else:
        print("No headlines found.")
