import feedparser
from flask import Flask
from flask import render_template
from flask import request
import json
import requests

app = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'wapo': 'http://feeds.washingtonpost.com/rss/politics?tid=lk_inline_manual_2',
             'xkcd': 'https://www.xkcd.com/rss.xml'
             }

@app.route("/")
def get_news():
    try:
        query = request.args.get("publication")
        if not query or query.lower() not in RSS_FEEDS:
            publication = "bbc"
        else:
            publication = query.lower()
        feed = feedparser.parse(RSS_FEEDS[publication])    
    except:
        return "<html><body><p>publication: %s</p></body></html>" % str(publication)

    weather = get_weather("London, UK")
    return render_template("home.html",
                               articles=feed["entries"],
                               weather=weather)
    

def get_weather(query):
    api_url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=679ab64123570193b0ddd09b6bd87085"
    # handles cities with spaces in their name, etc
    query = requests.utils.quote(query)
    # adds the query to the URL
    url = api_url.format(query)
    # get the site
    data_ro = requests.get(url)
    try:
        data_ro.raise_for_status()
    except Exception as exc:
        print("Trouble getting the site" + str(exc))
    parsed = json.loads(data_ro)
    weather = None
    if parsed.get("weather"):
        weather = {"description":
                   parsed["weather"][0]["description"],
                   "temperature":parsed["main"]["temp"],
                   "city":parsed["name"]
                   }
        return weather
    
    
if __name__ == '__main__':
    app.run(port=5000, debug=True)
