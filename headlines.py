import feedparser
from flask import Flask

app = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'wapo': 'http://feeds.washingtonpost.com/rss/politics?tid=lk_inline_manual_2',
             'xkcd': 'https://www.xkcd.com/rss.xml'
             }

@app.route("/")
@app.route("/<publication>")
def get_news(publication="bbc"):
    try:
        feed = feedparser.parse(RSS_FEEDS[publication])
        first_article = feed['entries'][0]
        return """
<html>
    <head>
        <link rel="icon" href="data:,">
    </head>
    <body>
        <h1> Headlines </h1>
        <b>{0}</b> <br/>
        <i>{1}</i> <br/>
        <p>{2}</p> <br/>
    </body>
</html>""".format(first_article.get("title"), first_article.get("published"), first_article.get("summary"))
    except:
        return "<html><body><p>publication: %s</p></body></html>" % str(publication)
    

if __name__ == '__main__':
    app.run(port=5000, debug=True)
