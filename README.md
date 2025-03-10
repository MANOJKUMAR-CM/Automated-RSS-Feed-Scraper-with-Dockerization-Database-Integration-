# 📰 Automated RSS Feed Scraper with Dockerization & Database Integration 🚀

## **Overview**  
This project sets up an **RSS Feed Scraper** that automatically fetches and processes news articles from RSS feeds, storing them in a **containerized PostgreSQL database**. The application is designed to handle dynamic RSS streams efficiently, avoid unnecessary duplicates, and ensure persistence.  

---

## 📌 Features
- **Automated RSS Scraping**: Fetches articles from RSS feeds at regular intervals.
- **Dockerized Database**: Containerized database setup with automatic table creation.
- **Configurable Feeds**: Supports multiple news sources like The Hindu, TOI, NDTV, etc.
- **Duplicate Handling**: Avoids redundant data while tracking changes in the feed.
- **Persistent Storage**: Saves articles with essential metadata in a structured format.
- **Logging & Debugging**: Generates logs for monitoring and debugging.

---

## 📂 Data Structure

Each article is stored as a tuple with the following fields:

1. **Title** *(Required)*
2. **Publication Timestamp** *(Stored as `datetime`)*
3. **Weblink** *(Required)*
4. **Article Image** *(Downloaded if available)*
5. **Tags** *(One or more tags)*
6. **Summary** *(Optional)*

---

## 📁 Project Structure  

```bash
📁 RSS Feed Scraper  
│── 📜 docker-compose.yml      # Defines multi-container setup  
│── 📜 Dockerfile              # Builds the RSS scraper image  
│── 📜 scraper.py              # Python script for fetching and storing RSS feeds  
│── 📜 requirements.txt        # Dependencies for the Python scraper  
│── 📜 init.sh                 # Database initialization and schema setup  
│── 📜 README.md               # Project documentation (this file)  
```

## 🏗️ Setup & Execution

### 1️⃣ **Start Docker Desktop**
Ensure Docker is running before executing the commands.

### 2️⃣ **Build & Run Services**
- Run the following command to build and start the containers:
``` sh
docker-compose up --build -d
```
### 3️⃣ **Verify Running Containers**
- Check if the containers are running successfully
``` sh
docker ps
```
- Example output:
``` sh
CONTAINER ID   IMAGE                     STATUS                    PORTS                    NAMES
a7870a1100e4   assignment4-rss_scraper   Up 8 seconds                                       rss_scraper
cfebee72340d   postgres:latest           Up 14 seconds (healthy)   0.0.0.0:5432->5432/tcp   news_rssFeed_db
```
### 4️⃣ **Check Logs**
- Monitor logs for debugging and information:
``` sh
docker logs news_rssFeed_db
docker logs rss_scraper
```
### 🛠️ To Stop the Services
- Stop all containers:
``` sh
docker-compose down
```

---

## 📧 Contact  

If you have questions, suggestions, or just want to connect, feel free to reach out!  

- **Name**: Manoj Kumar.CM  
- **Email**: [manoj.kumar@dsai.iitm.ac.in]  
- **GitHub Profile**: [Manoj Kumar C M](https://github.com/MANOJKUMAR-CM)  

Happy coding! 🚀

