import os
import io
import feedparser
from datetime import datetime
import requests
import psycopg2
import time

# RSS Feed and Required fields
FEED_URL = os.getenv("rss_feed_url")
TITLE = os.getenv("title")
SUMMARY = os.getenv("summary")
A_LINK = os.getenv("article_link")
TAGS = os.getenv("tags")
I_LINK = os.getenv("image_url")
D_TIME = os.getenv("pub_timestamp")

# DataBase Details
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Polling frequency
POLLING_INTERVAL = int(os.getenv("POLLING_INTERVAL", "600"))  

def connect():  
    try:
        connection = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        print("Connected to the database.")
        return connection
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

def getNews_From_Feeds():
    try:
        print("Fetching feed from URL:", FEED_URL)
        feed = feedparser.parse(FEED_URL)
        
        if not feed.entries:
            print("No entries found in the RSS feed.")
            return
        
        print(f"Found {len(feed.entries)} entries in the feed.")
        
        connection = connect()
        if not connection:
            print("Could not establish a database connection. Exiting.")
            return
        
        cursor = connection.cursor()
        print("Database cursor created.")
        count = 0
        for article in feed.entries:
            #print("Processing article:", article)
            
            title = article.get(TITLE)
            summary = article.get(SUMMARY)
            link = article.get(A_LINK)
            tags = article.get(TAGS)[0]['term'] if article.get(TAGS) else "No tags"
            image_link = article.get(I_LINK)[0]['url'] if article.get(I_LINK) else None
            d_time = article.get(D_TIME)
            d_time = datetime.strptime(d_time, "%a, %d %b %Y %H:%M:%S %z")
            d_time = d_time.replace(tzinfo=None)  
            
            cursor.execute("SELECT 1 FROM news_articles WHERE weblink = %s", (link,))
            if cursor.fetchone():
                print(f"Duplicate article found: Skipping, {title}.")
                continue
            else:
                image_data = None
                if image_link:  
                    try:
                        image_response = requests.get(image_link)
                        if image_response.status_code == 200:
                            image_data = io.BytesIO(image_response.content).getvalue()
                        else:
                            print(f"Failed to fetch image for {title}. Status code: {image_response.status_code}")
                    except requests.RequestException as e:
                        print(f"Error fetching image for {title}: {e}")
                    
                insert_query = """
                INSERT INTO news_articles (title, pub_timestamp, weblink, image, tags, summary)
                VALUES (%s, %s, %s, %s, %s, %s);
                """
                cursor.execute(insert_query, (title, d_time, link, image_data, [tags], summary))
                print(f"Inserted article: {title}")
                count += 1
        
        connection.commit()  
        print(f"{count} articles inserted into the news_articles table.", flush=True)
        
        cursor.close()
        connection.close()
        print("Database connection closed.")
        
    except Exception as e:
        print(f"Error fetching the feed: {e}")

if __name__ == "__main__":
    while True:
        print(f"Fetching data from {FEED_URL}...")
        getNews_From_Feeds()
        print(f"Sleeping for {POLLING_INTERVAL} seconds...", flush=True)
        time.sleep(POLLING_INTERVAL)
