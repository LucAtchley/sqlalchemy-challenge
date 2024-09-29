# Import the dependencies.
from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine('sqlite:///hawaii.sqlite')
# Declare a Base using `automap_base()`
Base = automap_base()
# Use the Base class to reflect the database tables
Base.prepare(engine, reflect=True)

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

#################################################
# Flask Setup
#################################################
app = Flask(__name__)




#################################################
# Flask Routes
#################################################
@app.route('/')
def home():
    return jsonify({
        'routes': [
            '/api/v1.0/precipitation',
            '/api/v1.0/stations',
            '/api/v1.0/tobs',
            '/api/v1.0/<start>',
            '/api/v1.0/<start>/<end>'
        ]
    })

@app.route('/api/v1.0/precipitation')
def precipitation():
    recent_date = session.query(func.max(Measurement.date)).scalar()

    if isinstance(recent_date, str):
        recent_date = datetime.strptime(recent_date, '%Y-%m-%d')
    
    one_year = recent_date - timedelta(days=365)
    prec_data = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= one_year).\
    filter(Measurement.date <= recent_date).all()

    return jsonify(prec_data)


@app.route('/api/v1.0/stations')
def stations():
    stations = session.query(Station).all()
    stations_list = [Station.station for station in stations]
    return jsonify(stations_list)

@app.route('/api/v1.0/tobs')
def tobs():
    most_active_station = 'USC00519281'
    results = session.query(func.min(Measurement.tobs),
                        func.max(Measurement.tobs),
                        func.avg(Measurement.tobs)
                       ).filter(Measurement.station == most_active_station).all()
    lowest_temp, highest_temp, average_temp = results[0]
    return jsonify(results)

@app.route('/api/v1.0/<start>')
def start(start):
    
    return jsonify()

@app.route('/api/v1.0/<start>/<end>')
def start_end(start, end):
    
    return jsonify()

if __name__ == '__main__':
    app.run(debug=True)

session.close()