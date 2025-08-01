from flask import Flask, render_template
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from collections import Counter
from datetime import datetime


app = Flask(__name__)

# Set up Google Sheets
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
CREDS = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", SCOPE)
SHEET = gspread.authorize(CREDS).open("LeapScholar_Brand_Monitor").sheet1

@app.route("/")
def index():
    # Get data from Google Sheet
    data = SHEET.get_all_records()
    print("Raw data from sheet:", data)  # Debug print
    if not data:
        print("No data found in sheet!")
        return render_template("index.html", sentiments={}, topics={}, mentions=[], dates={})
    
    # Count sentiments for pie chart
    sentiments = Counter(row["Sentiments"] for row in data)
    sentiment_data = {
        "labels": list(sentiments.keys()),
        "values": list(sentiments.values())
    }
    print("Sentiment data:", sentiment_data)  # Debug print
    
    # Count topics for bar chart
    topics = Counter()
    for row in data:
        if row["Key_info"]:
            for topic in row["Key_info"].split(", "):
                topics[topic] += 1
    topic_data = {
        "labels": list(topics.keys()),
        "values": list(topics.values())
    }
    print("Topic data:", topic_data)  # Debug print
    
    # Prepare data for line chart (mentions by date)
    dates = {}
    for row in data:
        date = row["Date"]
        dates[date] = dates.get(date, 0) + 1
    date_data = {
        "labels": sorted(dates.keys()),
        "values": [dates[date] for date in sorted(dates.keys())]
    }
    print("Date data:", date_data)  # Debug print
    
    # Get recent mentions for table
    mentions = data[-5:]  # Last 5 rows
    print("Mentions:", mentions)  # Debug print
    
    return render_template("index.html", sentiments=sentiment_data, topics=topic_data, mentions=mentions, dates=date_data)

@app.route('/update')
def update_data():
    # Simulate data update (replace with actual logic)
    import brand_monitor
    brand_monitor.main()  # Assumes brand_monitor.py has a main() function
    return "Data updated!", 200

if __name__ == "__main__":
    app.run(debug=True)