from flask import Flask, render_template,redirect
from scrape_mars import scrape
# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
import pymongo
import json
# Create an instance of our Flask app.
app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
db = client.mars_db
collection = db.mars
# Drops collection if available to remove duplicates
db.mars.drop()


#################################################
# Flask Routes
#################################################

@app.route('/')
def index():
    # Store the entire mars collection in a list
    facts = db.mars.find()

    return render_template('index.html', facts=facts[0])


@app.route("/scrape")
def scrape_data():
    output = scrape()
    # Add scrape data to mongo
    collection.update({},output,upsert=True)
    return redirect("/")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=56575, debug=True)
