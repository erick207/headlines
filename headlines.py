import feedparser
from flask import Flask
from flask import render_template
from flask import request
import json
import requests

app = Flask(__name__)

# URL globals used to obtain services, the {} in WEATHER_URL is formatted with user input(GET)
WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&APPID=679ab64123570193b0ddd09b6bd87085"
CURRENCY_URL = "https://openexchangerates.org//api/latest.json?app_id=98bc030a611147269cc6e7893ff0a119"

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'wapo': 'http://feeds.washingtonpost.com/rss/politics?tid=lk_inline_manual_2',
             'xkcd': 'https://www.xkcd.com/rss.xml'
             }

DEFAULTS = {'publication':'bbc',
            'city':'London, UK',
            'currency_from':'USD',
            'currency_to':'ARS'}

@app.route("/")
def home():
    # get customized headlines, based on user input or default
    publication = request.args.get('publication')
    if not publication:
        publication = DEFAULTS['publication']
    articles = get_news(publication)
    # get customized weather based on user input or default
    city = request.args.get('city')
    if not city:
        city = DEFAULTS['city']
    weather = get_weather(city)
    # get customized currency based on user input or default
    currency_from = request.args.get("currency_from")
    if not currency_from:
        currency_from = DEFAULTS['currency_from']
    currency_to = request.args.get('currency_to')
    if not currency_to:
        currency_to = DEFAULTS['currency_to']
    rate = get_rate(currency_from, currency_to)
    
    return render_template("home.html",
                           articles=articles,
                           weather=weather,
                           currency_from=currency_from,
                           currency_to=currency_to,
                           rate=rate)

def get_news(query):
    try:
        if not query or query.lower() not in RSS_FEEDS:
            publication = DEFAULTS['publication']
        else:
            publication = query.lower()
        feed = feedparser.parse(RSS_FEEDS[publication])    
    except:
        return "<html><body><p>publication %s unreachable</p></body></html>" % str(publication)
    return feed['entries']
    

def get_weather(query):
    # api_url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=679ab64123570193b0ddd09b6bd87085"
    # handles cities with spaces in their name, etc
    query = requests.utils.quote(query)
    # adds the query to the URL
    url = WEATHER_URL.format(query)
    # get the site
    data_ro = requests.get(url)
    try:
        data_ro.raise_for_status()
    except Exception as exc:
        print("Trouble getting the weather site: " + str(exc))
    parsed = data_ro.json()
    weather = None
    if parsed.get("weather"):
        weather = {"description":parsed["weather"][0]["description"],
                   "temperature":parsed["main"]["temp"],
                   "city":parsed["name"],
                   "country":parsed["sys"]["country"]
                   }
        return weather
    
def get_rate(frm, to):
    all_currency_ro = requests.get(CURRENCY_URL)
    try:
        all_currency_ro.raise_for_status()
    except Exception as exc:
        print("trouble getting the currency site: " + str(exc))
    parsed = all_currency_ro.json().get("rates")
    frm_rate = parsed.get(frm.upper())
    to_rate = parsed.get(to.upper())
    return to_rate/frm_rate
    

if __name__ == '__main__':
    app.run(port=5000, debug=True)
