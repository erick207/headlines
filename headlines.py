import feedparser
from flask import Flask
from flask import render_template

app = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'wapo': 'http://feeds.washingtonpost.com/rss/politics?tid=lk_inline_manual_2',
             'xkcd': 'https://www.xkcd.com/rss.xml'
             }

@app.route("/")
def get_news():
    try:
        
        return render_template("home.html", articles=feed['entries'])
    except:
        return "<html><body><p>publication: %s</p></body></html>" % str(publication)
    

if __name__ == '__main__':
    app.run(port=5000, debug=True)
