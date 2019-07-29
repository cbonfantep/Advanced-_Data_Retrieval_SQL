import numpy as np
import re

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

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
    return (
        f"Available Routes:<br/>"
        f" /api/v1.0/precipitation<br/>"
        f"  /api/v1.0/stations<br/>"
        f"  /api/v1.0/tobs<br/>"
        f"  /api/v1.0/<\start\><br/>"
        f"  /api/v1.0/<\start\>/<\end\><br/>"
    )

@app.route("/api/v1.0/precipitation")
def prcp():
    """Convert the query results to a Dictionary using date as the
     key and prcp as the value.Return the JSON representation of your dictionary."""
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Return a JSON list of stations from the dataset
    results = session.query(Measurement.date, func.sum(Measurement.prcp)).group_by(Measurement.date).all()
    precipitation = []
    for date, prcp in results:
        precipitation_dic = {}
        precipitation_dic['date'] = date
        precipitation_dic['prcp'] = prcp
        precipitation.append(precipitation_dic)
    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Return a JSON list of stations from the dataset
    results = session.query(Station.station).all()
    # Convert list of tuples into normal list - method to get rid of unnecessary part of the tuple
    all_names = list(np.ravel(results))
    return jsonify(all_names)

@app.route("/api/v1.0/tobs")

# query for the dates and temperature observations from a year from the last data point.
# Return a JSON list of Temperature Observations (tobs) for the previous year.

def temperature():
# Create our session (link) from Python to the DB
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > '2016-08-22').order_by(Measurement.date).all()
    temp = list(np.ravel(results))
    return jsonify(temp)


@app.route("/api/v1.0/<start>")
def start_tobs(start):
# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

    session = Session(engine)
    results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.prcp))\
    .filter(Measurement.date >= start).all()
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.

    temp_start = list(np.ravel(results))

    return jsonify(temp_start)

@app.route("/api/v1.0/<start>/<end>")
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.

def start_end(start, end):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)). \
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    temp_start_end = list(np.ravel(results))

    return jsonify(temp_start_end)

if __name__ == "__main__":
    app.run(debug=True)
