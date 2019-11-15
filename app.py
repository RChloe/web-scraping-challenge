from flask import Flask, render_template,jsonify

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

# Creates a collection in the database and inserts two documents
# db.team.insert_many(
#     [
#         {
#             'player': 'Jessica',
#             'position': 'Point Guard'
#         },
#         {
#             'player': 'Mark',
#             'position': 'Center'
#         }
#     ]
# )
mars_data = {
  "featured_image_url": "https://www.jpl.nasa.gov/spaceimages/images/mediumsize/PIA16883_ip.jpg", 
  "hemisphere_image_urls": [
    {
      "img_url": "http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg", 
      "title": "Cerberus Hemisphere Enhanced"
    }, 
    {
      "img_url": "http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg", 
      "title": "Schiaparelli Hemisphere Enhanced"
    }, 
    {
      "img_url": "http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg", 
      "title": "Syrtis Major Hemisphere Enhanced"
    }, 
    {
      "img_url": "http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg", 
      "title": "Valles Marineris Hemisphere Enhanced"
    }
  ], 
  "html_table": "<table border=\"1\" class=\"dataframe\">\n  <thead>\n    <tr style=\"text-align: right;\">\n      <th></th>\n      <th>0</th>\n      <th>1</th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <th>0</th>\n      <td>Equatorial Diameter:</td>\n      <td>6,792 km</td>\n    </tr>\n    <tr>\n      <th>1</th>\n      <td>Polar Diameter:</td>\n      <td>6,752 km</td>\n    </tr>\n    <tr>\n      <th>2</th>\n      <td>Mass:</td>\n      <td>6.39 \u00d7 10^23 kg (0.11 Earths)</td>\n    </tr>\n    <tr>\n      <th>3</th>\n      <td>Moons:</td>\n      <td>2 (Phobos &amp; Deimos)</td>\n    </tr>\n    <tr>\n      <th>4</th>\n      <td>Orbit Distance:</td>\n      <td>227,943,824 km (1.38 AU)</td>\n    </tr>\n    <tr>\n      <th>5</th>\n      <td>Orbit Period:</td>\n      <td>687 days (1.9 years)</td>\n    </tr>\n    <tr>\n      <th>6</th>\n      <td>Surface Temperature:</td>\n      <td>-87 to -5 \u00b0C</td>\n    </tr>\n    <tr>\n      <th>7</th>\n      <td>First Record:</td>\n      <td>2nd millennium BC</td>\n    </tr>\n    <tr>\n      <th>8</th>\n      <td>Recorded By:</td>\n      <td>Egyptian astronomers</td>\n    </tr>\n  </tbody>\n</table>", 
  "mars_weather": "InSight sol 342 (2019-11-13) low -99.9\u00baC (-147.8\u00baF) high -23.3\u00baC (-9.9\u00baF)\nwinds from the SW at 5.2 m/s (11.7 mph) gusting to 20.5 m/s (46.0 mph)\npressure at 6.90 hPapic.twitter.com/NO4iCrXgrl", 
  "news_p": "A new paper identifies a ring of minerals at the rover's landing site that are ideal for fossilizing microbial life.", 
  "news_title": "NASA's Mars 2020 Will Hunt for Microscopic Fossils"
}

# Set route
@app.route('/')
def index():
    # Store the entire team collection in a list
    #facts = db.mars.find()

    #for fact in facts:
    #   return(fact)
    return('Hello World')
    # Return the template with the teams list passed in
    #return render_template('index.html', teams=teams)



#################################################
# Flask Routes
#################################################

@app.route("/scrape")
def welcome():
    from scrape_mars import scrape
    #output = scrape()
    output = scrape()
    #collection.insert(output)
    collection.update({},output,upsert=True)
    return (output)

# @app.route("/api/v1.0/precipitation")
# def precip():
#     measurements.dropna(inplace=True)
#     measurements_df = pd.DataFrame(measurements,columns=['date','prcp'])
#     measurements_dict=measurements_df.set_index('date').T.to_dict('list')

#     return (
#         jsonify(measurements_dict)
#     )

# @app.route("/api/v1.0/stations")
# def station():
#     stations_df = pd.DataFrame(stations,columns=['station'])
#     stations_dict = stations_df.to_dict('list')

#     return (
#         jsonify(stations_dict)
#     )

# @app.route("/api/v1.0/tobs")
# def tobs():
#     # Calculate the date 1 year ago from the last data point in the database
#     last_date = session.query(func.max(Measurement.date))
#     last_date_list=[date[0] for date in last_date]
#     last_date_date=dt.datetime.strptime(last_date_list[0],'%Y-%m-%d')
#     twelve_months_ago=last_date_date-dt.timedelta(days=365)
#     twelve_months_ago_string=twelve_months_ago.strftime('%Y-%m-%d')

#     # Perform a query to retrieve the data and tobs scores
#     tobs_scores = session.query(Measurement.tobs,Measurement.date).filter(Measurement.date>twelve_months_ago_string)
#     tobs_last_12 = pd.DataFrame(tobs_scores)

#     tobs_df = pd.DataFrame(tobs_last_12,columns=['date','tobs'])
#     tobs_dict=tobs_df.set_index('date').T.to_dict('list')

#     return (
#         jsonify(tobs_dict)
#     )

# @app.route("/api/v1.0/<start_date>")
# # This function called `calc_temps` will accept start date and end date in the format '%Y-%m-%d' 
# # and return the minimum, average, and maximum temperatures for that range of dates
# def calc_temps(start_date, end_date=None):
#     """TMIN, TAVG, and TMAX for a list of dates.
    
#     Args:
#         start_date (string): A date string in the format %Y-%m-%d
#         end_date (string): A date string in the format %Y-%m-%d
        
#     Returns:
#         TMIN, TAVE, and TMAX
#     """
#     last_date = session.query(func.max(Measurement.date))
#     if end_date is None:
#         end_date = last_date
#     return jsonify(session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
#         filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all())

# @app.route("/api/v1.0/<start_date>/<end_date>")
# # This function called `calc_temps2` will accept start date and end date in the format '%Y-%m-%d' 
# # and return the minimum, average, and maximum temperatures for that range of dates
# def calc_temps2(start_date, end_date=None):
#     """TMIN, TAVG, and TMAX for a list of dates.
    
#     Args:
#         start_date (string): A date string in the format %Y-%m-%d
#         end_date (string): A date string in the format %Y-%m-%d
        
#     Returns:
#         TMIN, TAVE, and TMAX
#     """
#     last_date = session.query(func.max(Measurement.date))
#     if end_date is None:
#         end_date = last_date
#     return jsonify(session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
#         filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all())


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=56575, debug=True)
