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
mars_scrape = mongo.db.mars_scrape
mars_scrape.drop()

# Render the index.html page with any web scrape listings in our database. 
# If there are no listings, the table will be empty.
@app.route("/")
def index():
    result = mars_scrape.find_one()
    return render_template("index.html", result=result)

@app.route('/scrape')
def scrape():
    mars_scrape_data = scrape_mars.scrape()
    mars_scrape.insert(mars_scrape_data)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)