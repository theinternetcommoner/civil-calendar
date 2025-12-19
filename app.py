# Civil Case Calendar Generator App
# This program was built for me (yes, me!) to address my problem
# in generating hhearing calendar shcedules, but feel 
# free to use and modify my code

# it was designed and built to only have the packages 
# it needs to work that's why SQL Alchemy was not used 

from flask import * # import flask packages
import os # used for generating secret key
import sqlite3 as db # used for the database
from datetime import datetime # used for date convertion
from waitress import serve # WSGI for deployment/production
import logging # import logging package
from flask_bootstrap import Bootstrap5
from admin.admin import admin # import admin file blueprint

app = Flask(__name__)

bootstrap = Bootstrap5(app)

app.secret_key = os.urandom(64) # generate secret key

app.register_blueprint(admin, url_prefix = "/admin")

logging.basicConfig(level = logging.INFO) # enable logging

# defining the database connecction function
def db_connect():
	conn = db.connect('calendar.db')
	conn.row_factory = db.Row
	return conn

# The home page route
@app.route('/', methods = ['GET'])
def home():
	return render_template('index.html')

# route that generates the hearing calendar
@app.route('/generate', methods = ['POST'])
def generate():
	# using the predefined database function
	query = db_connect()

	# fetching data from HTML inputs
	short_date = str(request.form['hearing_date'])
	time = request.form['time']
	hearing_date = request.form['hearing_date']

	# converting shrort date to words (e.g. 2025-09-01 to September 1, 2025)
	date_object = datetime.strptime(short_date, "%Y-%m-%d")
	calendar_date = date_object.strftime("%B %d, %Y")

	# the query used for retreiving data from the database
	sql = "SELECT * FROM tbl_calendar WHERE hearing_sched LIKE ? AND hearing_time = ? ORDER BY status"
	rw = query.execute(sql, ['%'+hearing_date+'%', time]).fetchall()

	sql1 = "SELECT * FROM tbl_heading"
	rw1 = query.execute(sql1).fetchall()

	if rw:
		msg = ''
	else:
		msg = 'NO HEARING'

	# rendering data in HTML form using the built-in Jinja2 template
	return render_template('calendar.html', row = rw, hrow = rw1, calendar_date = calendar_date.upper(), time = time.upper(), message = msg)
	# closing the databse connection
	query.close()

# Running the app (using the default or production WSGI)

dev_mode = False # used for wsgi switching between default and deployment

if __name__ == '__main__':
	if dev_mode == True:
		# default wsgi
		app.run(host = '0.0.0.0', port = 5050, debug = True)
	else:
		# waitress (deployment)
		print('Service Started Successfully')
		serve(app, host = '0.0.0.0', port = 5050, threads = 4)