import random
import time
import csv
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import numpy as np

# Constants
chrome_driver_path = 'path_to_chromedriver'  # Replace with your actual ChromeDriver path
target_url = 'https://www.bbc.com/news'  # Example target: BBC News
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0',
    'Mozilla/5.0 (Windows NT 6.1; Win64; rv:70.0) Gecko/20100101 Firefox/70.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; rv:89.0) Gecko/20100101 Firefox/89.0'
]


# Function to add a random delay between requests (request throttling)
def random_delay(min_delay=2, max_delay=5):
    delay = random.uniform(min_delay, max_delay)
    print(f"Sleeping for {delay:.2f} seconds...")
    time.sleep(delay)


# Function to scrape the page using Selenium and BeautifulSoup
def scrape_page(url):
    # Set up Chrome options for headless browsing
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode (without GUI)

    # Create Service object for Selenium WebDriver
    service = Service(executable_path=chrome_driver_path)

    # Initialize the WebDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Use random User-Agent for each request
    headers = {
        'User-Agent': random.choice(user_agents)
    }

    # Open the target URL
    driver.get(url)

    # Wait for the page to load completely (adjust the selector as needed)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'h3.gs-c-promo-heading__title'))
        )
    except Exception as e:
        print(f"Error waiting for page to load: {e}")
        driver.quit()
        return []

    # Get page source after JavaScript rendering
    page_source = driver.page_source
    driver.quit()

    # Introduce request throttling to avoid detection
    random_delay(min_delay=2, max_delay=5)

    # Use BeautifulSoup to parse the page source
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find the headlines on the page (adjust the CSS selector as needed)
    headlines = soup.find_all('h3', class_='gs-c-promo-heading__title')

    # Extract the text of the headlines
    headlines_text = [headline.get_text() for headline in headlines]

    return headlines_text


# Function to save data to CSV
def save_to_csv(data, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Headline'])  # CSV header
        for row in data:
            writer.writerow([row])


# Data Transformation: Load and Process Data using Pandas
def load_and_process_data(filename):
    # Load CSV into a DataFrame
    df = pd.read_csv(filename)
    print(f"Data loaded from {filename}.")

    # Clean data by removing duplicates and missing values
    df.drop_duplicates(inplace=True)
    df.dropna(inplace=True)

    # Data transformation: Descriptive statistics
    print("Descriptive Statistics:")
    print(df.describe())

    return df


# Identify Patterns and Trends (e.g., Frequency of words in headlines)
def analyze_headlines(df):
    # Count the frequency of words in the headlines
    words = ' '.join(df['Headline']).split()
    word_count = pd.Series(words).value_counts()

    # Display the most common words
    print("\nMost Common Words in Headlines:")
    print(word_count.head(10))


# Perform Time Series Analysis (optional - if there's a time aspect)
def time_series_analysis(df):
    # For the purpose of the example, we'll simulate timestamps (you can adjust this part)
    df['Timestamp'] = pd.date_range(start="2024-01-01", periods=len(df), freq='D')

    # Simulate tracking headlines per day (or you could track any numeric variable)
    daily_counts = df.groupby('Timestamp').size()

    print("\nTime Series Analysis (Headlines Per Day):")
    print(daily_counts)

    # Plotting Time Series Analysis using Matplotlib
    plt.figure(figsize=(10, 6))
    plt.plot(daily_counts.index, daily_counts.values, marker='o', linestyle='-', color='b')
    plt.title('Headlines Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Headlines')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


# Perform Correlation and Clustering Analysis
def advanced_analytics(df):
    # Example: Create a simple numeric representation of the headlines (word length)
    df['Headline_Length'] = df['Headline'].apply(len)

    # Correlation analysis (e.g., between headline length and word frequency, if applicable)
    print("\nCorrelation Analysis:")
    print(df.corr())

    # Clustering analysis: Using KMeans clustering on headline length
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df[['Headline_Length']])

    kmeans = KMeans(n_clusters=3, random_state=42)
    df['Cluster'] = kmeans.fit_predict(df_scaled)

    print("\nClustering Analysis (Headline Length Clusters):")
    print(df[['Headline', 'Cluster']].head(10))

    # Plotting Clustering using Seaborn
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x=df.index, y='Headline_Length', hue='Cluster', palette='Set2', data=df)
    plt.title('Headline Length Clustering')
    plt.xlabel('Index')
    plt.ylabel('Headline Length')
    plt.tight_layout()
    plt.show()


# Data Visualization - Interactive Visualization with Plotly
def plot_interactive(df):
    # Create a simple interactive plot with Plotly for headline lengths
    fig = px.scatter(df, x=df.index, y='Headline_Length', color='Cluster',
                     labels={'Headline_Length': 'Headline Length', 'index': 'Index'},
                     title='Interactive Visualization of Headline Lengths')
    fig.show()


# Main execution
if __name__ == "__main__":
    # Step 1: Scrape the website
    headlines = scrape_page(target_url)

    if headlines:
        print(f"Scraped {len(headlines)} headlines.")

        # Step 2: Data Cleaning and Validation (remove duplicates)
        cleaned_headlines = list(set(headlines))  # Remove duplicate headlines

        # Step 3: Store cleaned data in CSV
        save_to_csv(cleaned_headlines, 'headlines.csv')
        print(f"Saved {len(cleaned_headlines)} unique headlines to 'headlines.csv'")

        # Step 4: Load and Process Data using Pandas
        df = load_and_process_data('headlines.csv')

        # Step 5: Analyze Patterns, Trends, and Outliers
        analyze_headlines(df)

        # Step 6: Perform Time Series Analysis (optional)
        time_series_analysis(df)

        # Step 7: Advanced Analytics (Correlation, Clustering)
        advanced_analytics(df)

        # Step 8: Interactive Data Visualization using Plotly
        plot_interactive(df)

    else:
        print("No data scraped.")
