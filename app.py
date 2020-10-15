# Dependencies

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import numpy as np
import pandas as pd

from datetime import datetime

# Import Flask
from flask import Flask, jsonify

import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    
    print("Welcome page request.")
    
    return (
    f"<br/>"
    f"<br/>"
    f"Welcome to Surf's UP, Hawaii's Weather API!!!!<br/>"
    f"Please note that data is available from January 1, 2010 to August 23, 2017.<br/>"
    f"<br/>"
    f"Available Routes:<br/>"
    f"<br/>"
    f"/api/v1.0/precipitation<br/>"
    f"- A list of dates and precipitation observations from the last year.<br/>"
    f"<br/>"
    f"/api/v1.0/stations<br/>"
    f"- A list of stations from the dataset.<br/>"
    f"<br/>"
    f"/api/v1.0/tobs<br/>"    
    f"- A list of Temperature Observations (tobs) for the previous year.<br/>"
    f"<br/>"
    f"/api/v1.0/2015-05-18<br/>"
    f"- A list of Min, Max, and Avg Temperature Observations (tobs) for particulater start date.<br/>"
    f"<br/>"
    f"/api/v1.0/2015-05-18/2015-09-18<br/>"
    f"- A list of Min, Max, and Avg Temperature Observations (tobs) for particulater start and end date.<br/>"
    )


#################################################
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a JSON list of precipitation from the dataset."""
    
    print("Received precipitation api request.")
    
    # Find the last date in the datebase, then calculate 1 year before that.
    date_query = session.query(func.max(func.strftime("%Y-%m-%d", Measurement.date))).all()
    final_date_string = date_query[0][0]
    final_date = dt.datetime.strptime(final_date_string, "%Y-%m-%d")

    start_date = final_date - dt.timedelta(365)
    
    # Get precipiation data for the last year.
    precipitation_results = session.query(func.strftime("%Y-%m-%d", Measurement.date), Measurement.prcp).\
        filter(func.strftime("%Y-%m-%d", Measurement.date) >= start_date).all()
    
    # Close the Query
    session.close() 
    
    precipitation = {}
    for result in precipitation_results:
            precipitation[result[0]] = result[1]
    
    return jsonify(precipitation)


#################################################
@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations from the dataset."""
    
    print("Received stations api request.")
    
    # Get station data.
    stations_results = session.query(Station).all()
    
    # Close the Query
    session.close() 
    
    #Create a list of dictionaries
    stations_list=[]
    for station in stations_results:
        station_dictionary = {}
        station_dictionary["id"]=station.id
        station_dictionary["station"]=station.station
        station_dictionary["name"]=station.name
        station_dictionary["latitude"]=station.latitude
        station_dictionary["longitude"]=station.longitude
        station_dictionary["elevation"]=station.elevation
        stations_list.append(station_dictionary)
    
    return jsonify(stations_list)
     

#################################################
@app.route("/api/v1.0/tobs")
def tobs():
    """Return a JSON list of temperature observation from the dataset."""
    
    print("Received tobs api request.")

    # Find the last date in the datebase, then calculate 1 year before that.
    date_query = session.query(func.max(func.strftime("%Y-%m-%d", Measurement.date))).all()
    final_date_string = date_query[0][0]
    final_date = dt.datetime.strptime(final_date_string, "%Y-%m-%d")

    start_date = final_date - dt.timedelta(365)
    
    # Get temperature data for the last year.
    temperature_results = session.query(Measurement).\
        filter(func.strftime("%Y-%m-%d", Measurement.date) >= start_date).all()

    # Close the Query
    session.close() 
    
    #Create a list of dictionaries
    temperature_list=[]
    for temperature in temperature_results:
        temperature_dictionary = {}
        temperature_dictionary["date"]=temperature.date
        temperature_dictionary["id"]=temperature.id
        temperature_dictionary["station"]=temperature.station
        temperature_dictionary["tobs"]=temperature.tobs
        temperature_list.append(temperature_dictionary)
    
    return jsonify(temperature_list)


#################################################
@app.route("/api/v1.0/<start>")

def start(start):
    """Return a JSON list of Min, Max, and Avg Temperature Observations (tobs) for particulater start date."""
    
    print("Received start api request.")
    
    start_date_result = session.query(Measurement.date, func.max(Measurement.tobs),func.min(Measurement.tobs),func.round(func.avg(Measurement.tobs))).\
        filter(Measurement.date >= start).all()

    # Close the Query
    session.close() 
    
    # Create a list
    start_temperature_list = []
    for tobs in start_date_result:
        start_temperature_dict ={}
        start_temperature_dict["Max Temp"]=float(tobs[1])
        start_temperature_dict["Min Temp"]=float(tobs[2])
        start_temperature_dict["Avg Temp"]=float(tobs[3])
        start_temperature_list.append(start_temperature_dict)
  
    return jsonify(start_temperature_list)


#################################################
@app.route("/api/v1.0/<start>/<end>")

def startend(start, end):
    """Return a JSON list of Min, Max, and Avg Temperature Observations (tobs) for particulater start and end date."""
    
    print("Received start - end api request.")
    
    start_date_2_result = session.query(func.max(Measurement.tobs),func.min(Measurement.tobs),func.round(func.avg(Measurement.tobs))).\
        filter(Measurement.date.between(start,end)).all()

    # Close the Query
    session.close() 
    
    # Create a list
    start_temperature_2_list = []
    for tobs in start_date_2_result:
        start_temperature_2_dict ={}
        start_temperature_2_dict["Max Temp"]=float(tobs[0])
        start_temperature_2_dict["Min Temp"]=float(tobs[1])
        start_temperature_2_dict["Avg Temp"]=float(tobs[2])
        start_temperature_2_list.append(start_temperature_2_dict)
  
    return jsonify(start_temperature_2_list)


#################################################

if __name__ == '__main__':
    app.run(debug=True)
    