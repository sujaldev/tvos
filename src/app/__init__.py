from flask import Flask
from flask import request
from flask import render_template
from urllib.parse import quote_plus
from streaming_api import API

app = Flask(__name__)
app.jinja_env.filters['quote_plus'] = lambda url: quote_plus(url)
api = API()


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/results")
def results():
    query = request.values["q"]
    results = api.search(query)
    return render_template("results.html", results=results)


@app.route("/final")
def final():
    query = request.values["q"]
    return render_template("video.html", result={
        "link": api.get_media_source(query)
    })


if __name__ == "__main__":
    app.run(debug=True)
