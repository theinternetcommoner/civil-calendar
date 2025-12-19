from flask import * # import flask packages
import sqlite3 as db # used for the database

admin = Blueprint("admin", __name__, static_folder = "static", template_folder = "templates")

# defining the database connecction function
def db_connect():
	conn = db.connect('./calendar.db')
	conn.row_factory = db.Row
	return conn

# calendar headind routes
@admin.route('/heading', methods = ['GET'])
def admin_heading():
	# using the predefined database function
	query = db_connect()

	# the query used for retreiving data from the database
	sql = "SELECT * FROM tbl_heading"
	rw = query.execute(sql).fetchall()
	# closing the databse connection
	query.close()

	# rendering data in HTML form using the built-in Jinja2 template
	return render_template('heading.html', row = rw)
	# closing the databse connection
	query.close()

# heading select route
@admin.route('/selectheading/<string:id>', methods = ['GET'])
def admin_selectheading(id):
	query = db_connect()

	sql = "SELECT * FROM tbl_heading WHERE heading_id = ?"
	rw = query.execute(sql, (id,)).fetchall()

	# rendering data in HTML form using the built-in Jinja2 template
	return render_template('selectheading.html', row = rw)
	# closing the databse connection
	query.close()

# heading update route
@admin.route('/updateheading', methods = ['POST'])
def admin_updateheading():
	try:
		# storing search values in dictionary format
		data = {
			'heading_id': request.form['id'],
			'judicial_region': request.form['region'],
			'court': request.form['court'],
			'branch': request.form['branch'],
			'station': request.form['station'],
			'judge': request.form['judge'],
			'prosecutor': request.form['opp'],
			'pao': request.form['pao'],
			'interpreter': request.form['interpreter'],
			'stenographer': request.form['steno'],
		}

		# using the predefined database function
		query = db_connect()

		# sql query for updating data
		sql = """
			UPDATE tbl_heading SET judicial_region = :judicial_region,
			court = :court, branch = :branch, station = :station, judge = :judge,
			prosecutor = :prosecutor, pao = :pao, interpreter = :interpreter, 
			stenographer = :stenographer WHERE heading_id = :heading_id
		"""
		query.execute(sql, data)
		query.commit()
		msg = 'Success!'
	except:
		query.rollback()
		msg = 'Failed'
	finally:
		return render_template('result.html', message = msg)
		query.close() 

# ==================================================================================================

# admin route
@admin.route('/', methods = ['GET'])
def admin_index():
	# using the predefined database function
	query = db_connect()

	# the query used for retreiving data from the database
	sql = "SELECT * FROM tbl_calendar  ORDER BY status"
	rw = query.execute(sql).fetchall()
	# closing the databse connection
	query.close()

	# rendering data in HTML form using the built-in Jinja2 template
	return render_template('admin.html', row = rw)
	# closing the databse connection
	query.close()

# new form
@admin.route('/new')
def admin_new():
	return render_template('new.html')

# insert function
@admin.route('/insert', methods = ['POST'])
def admin_insert():
	try:
		# storing search values in dictionary format
		data = {
			'case_no': request.form['case_no'],
			'case_title': request.form['case_title'],
			'case_nature': request.form['case_nature'],
			'pet_atty': request.form['pet_atty'],
			'res_atty': request.form['res_atty'],
			'hearing_time': request.form['hearing_time'],
			'hearing_sched': request.form['hearing_sched'],
			'updates': request.form['update'],
			'status': request.form['status'],
		}

		# using the predefined database function
		query = db_connect()

		# sql query for inserting data using named parameters
		cols = ', '.join(data.keys())
		vals = ':' + ', :'.join(data.keys())
		sql = f"INSERT INTO tbl_calendar({cols}) VALUES({vals})"
		query.execute(sql, data)
		query.commit()
		msg = 'Success!'
	except:
		query.rollback()
		msg = 'Failed'
	finally:
		return render_template('result.html', message = msg)
		query.close()

# select route
@admin.route('/selectid/<string:id>', methods = ['GET'])
def admin_select(id):
	query = db_connect()

	sql = "SELECT * FROM tbl_calendar WHERE id = ?"
	rw = query.execute(sql, (id,)).fetchall()

	# rendering data in HTML form using the built-in Jinja2 template
	return render_template('select.html', row = rw)
	# closing the databse connection
	query.close()

# update route
@admin.route('/update', methods = ['POST'])
def admin_update():
	try:
		# storing search values in dictionary format
		data = {
			'id': request.form['id'],
			'case_no': request.form['case_no'],
			'case_title': request.form['case_title'],
			'case_nature': request.form['case_nature'],
			'pet_atty': request.form['pet_atty'],
			'res_atty': request.form['res_atty'],
			'hearing_time': request.form['hearing_time'],
			'hearing_sched': request.form['hearing_sched'],
			'updates': request.form['update'],
			'status': request.form['status'],
		}

		# using the predefined database function
		query = db_connect()

		# sql query for updating data
		sql = """
			UPDATE tbl_calendar SET case_no = :case_no,
			case_title = :case_title, case_nature = :case_nature,
			pet_atty = :pet_atty, res_atty = :res_atty,
			hearing_time = :hearing_time, hearing_sched = :hearing_sched,
			updates = :updates, status = :status WHERE id = :id
		"""
		query.execute(sql, data)
		query.commit()
		msg = 'Success!'
	except:
		query.rollback()
		msg = 'Failed'
	finally:
		return render_template('result.html', message = msg)
		query.close()

# route for searching
@admin.route('/search', methods = ['POST'])
def admin_search():
	# using the predefined database function
	query = db_connect()

	# fetching data from HTML input
	searchval = "%"+request.form['search']+"%"

	# storing search values in dictionary format
	data = {
		'case_no': searchval,
		'case_title': searchval,
		'case_nature': searchval,
		'pet_atty': searchval,
		'res_atty': searchval,
		'hearing_time': searchval,
		'hearing_sched': searchval,
	}

	# the query used for retreiving data from the database
	sql = """
		SELECT * FROM tbl_calendar WHERE 
		case_no LIKE :case_no OR 
		case_title LIKE :case_title OR 
		case_nature LIKE :case_nature OR 
		pet_atty LIKE :pet_atty OR 
		res_atty LIKE :res_atty OR 
		hearing_time LIKE :hearing_time OR 
		hearing_sched LIKE :hearing_sched
	"""
	rw = query.execute(sql, data).fetchall()

	# rendering data in HTML form using the built-in Jinja2 template
	return render_template('admin.html', row = rw)
	# closing the databse connection
	query.close()