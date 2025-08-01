import requests
from bs4 import BeautifulSoup
import tweepy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import re
import os
import dotenv
KEY = dotenv.get_key(".env", "X_BEARER_TOKEN")

# Set up X API credentials
X_BEARER_TOKEN = os.getenv("X_BEARER_TOKEN", KEY)

# Set up Google Sheets credentials
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
CREDS = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", SCOPE)
SHEET = gspread.authorize(CREDS).open("LeapScholar_Brand_Monitor").sheet1

# Initialize VADER sentiment analyzer
SENTIMENT_ANALYZER = SentimentIntensityAnalyzer()

# Fetch mentions from Google Search
def fetch_google_mentions():
    url = "https://www.google.com/search?q=LeapScholar+reviews"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        mentions = []
        for item in soup.select("div.g div.tF2Cxc"):
            text = item.select_one("span.aCOpRe").text if item.select_one("span.aCOpRe") else ""
            if text and len(text) > 10:
                mentions.append({"text": text, "date": datetime.now().strftime("%Y-%m-%d"), "platform": "Google"})
        return mentions[:3]
    except Exception as e:
        print(f"Google fetch error: {e}")
        return []

# Fetch mentions from X using API
def fetch_x_mentions():
    client = tweepy.Client(bearer_token=X_BEARER_TOKEN)
    try:
        query = "LeapScholar -is:retweet lang:en"
        tweets = client.search_recent_tweets(query=query, max_results=10)
        mentions = []
        if tweets.data:
            for tweet in tweets.data:
                mentions.append({"text": tweet.text, "date": datetime.now().strftime("%Y-%m-%d"), "platform": "X"})
        return mentions
    except Exception as e:
        print(f"X fetch error: {e}")
        return []

# Analyze sentiment with VADER
def analyze_sentiment(text):
    scores = SENTIMENT_ANALYZER.polarity_scores(text)
    compound = scores["compound"]
    if compound >= 0.05:
        return "Happy"
    elif compound <= -0.05:
        return "Sad"
    else:
        return "Neutral"

# Extract key topics
def extract_topics(text):
    words = re.findall(r'\b\w+\b', text.lower())
    important_words = ["visa", "loan", "counseling", "service", "support", "admission", "scholarship"]
    topics = [word for word in words if word in important_words]
    return topics if topics else ["general"]

# Store data in Google Sheet
def update_google_sheet(mentions):
    if not SHEET.get_all_values():
        SHEET.append_row(["Date", "PlatformName", "Comments", "Sentiments", "Key_info"])
    for mention in mentions:
        topics = ", ".join(extract_topics(mention["text"]))
        SHEET.append_row([mention["date"], mention["platform"], mention["text"], analyze_sentiment(mention["text"]), topics])

# Main function
def main():
    google_mentions = fetch_google_mentions()
    x_mentions = fetch_x_mentions()
    all_mentions = google_mentions + x_mentions
    if all_mentions:
        update_google_sheet(all_mentions)
        print("Data saved to Google Sheet!")
    else:
        print("No mentions found.")

if __name__ == "__main__":
    main()




# import requests
# from bs4 import BeautifulSoup
# import tweepy
# from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
# from datetime import datetime
# import re
# import os

# # Set up X API credentials
# X_BEARER_TOKEN = os.getenv("X_BEARER_TOKEN", "your-bearer-token-here")

# # Set up Google Sheets credentials
# SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
# CREDS = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", SCOPE)
# SHEET = gspread.authorize(CREDS).open("LeapScholar_Brand_Monitor").sheet1

# # Initialize VADER sentiment analyzer
# SENTIMENT_ANALYZER = SentimentIntensityAnalyzer()

# # Fetch mentions from Google Search
# def fetch_google_mentions():
#     url = "https://www.google.com/search?q=LeapScholar+reviews"
#     headers = {"User-Agent": "Mozilla/5.0"}
#     try:
#         response = requests.get(url, headers=headers)
#         soup = BeautifulSoup(response.text, "html.parser")
#         mentions = []
#         for item in soup.select("div.g div.tF2Cxc"):
#             text = item.select_one("span.aCOpRe").text if item.select_one("span.aCOpRe") else ""
#             if text and len(text) > 10:
#                 mentions.append({"text": text, "date": datetime.now().strftime("%Y-%m-%d"), "platform": "Google"})
#         return mentions[:3]
#     except Exception as e:
#         print(f"Google fetch error: {e}")
#         return []

# # Fallback: Use fake X data since API might fail
# def fetch_x_mentions():
#     return [
#         {"text": "LeapScholar helped me with visa! So happy!", "date": "2025-08-01", "platform": "X"},
#         {"text": "Loan process at LeapScholar was slow.", "date": "2025-08-01", "platform": "X"},
#         {"text": "Great counseling from LeapScholar!", "date": "2025-08-01", "platform": "X"}
#     ]

# # Analyze sentiment with VADER
# def analyze_sentiment(text):
#     scores = SENTIMENT_ANALYZER.polarity_scores(text)
#     compound = scores["compound"]
#     if compound >= 0.05:
#         return "Happy"
#     elif compound <= -0.05:
#         return "Sad"
#     else:
#         return "Neutral"

# # Extract key topics
# def extract_topics(text):
#     words = re.findall(r'\b\w+\b', text.lower())
#     important_words = ["visa", "loan", "counseling", "service", "support", "admission", "scholarship"]
#     topics = [word for word in words if word in important_words]
#     return topics if topics else ["general"]

# # Store data in Google Sheet
# def update_google_sheet(mentions):
#     if not SHEET.get_all_values():
#         SHEET.append_row(["Date", "PlatformName", "Comments", "Sentiments", "Key_info"])
#     for mention in mentions:
#         topics = ", ".join(extract_topics(mention["text"]))
#         SHEET.append_row([mention["date"], mention["platform"], mention["text"], analyze_sentiment(mention["text"]), topics])

# # Main function
# def main():
#     google_mentions = fetch_google_mentions()
#     x_mentions = fetch_x_mentions()
#     all_mentions = google_mentions + x_mentions
#     if all_mentions:
#         update_google_sheet(all_mentions)
#         print("Data saved to Google Sheet!")
#     else:
#         print("No mentions found.")

# if __name__ == "__main__":
#     main()
