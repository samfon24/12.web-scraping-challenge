from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import time
# import scrape file
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# identify the collection and drop any existing data for this demonstration
listings = mongo.db.listings
listings.drop()

# Render the index.html page with any web scrape listings in our database. 
# If there are no listings, the table will be empty.
@app.route("/")
def index():
    listing_results = listings.find()
    return render_template("index.html", listing_results=listing_results)

@app.route('/scrape')
def scrape():
    listings_data = scrape_mars.scrape()
    time.sleep(30)
    listings.insert_many(listings_data)

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)