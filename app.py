from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://yuhsul1:456papa@ds145981.mlab.com:45981/heroku_rcdbkjkn"
mongo = PyMongo(app)

@app.route("/scrape")
def scraper():
    mars = mongo.db.mars 
    mars_data = scrape_mars.scrape()
    mars.update(
        {}, 
        mars_data,
        upsert=True)
    return redirect("/", code=302)

@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars = mars)

if __name__ == "__main__":
    app.run(debug=True)