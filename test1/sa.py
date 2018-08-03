import MySQLdb
db = MySQLdb.connect(host="10.0.4.146",
					user="root",
					passwd="1234",
					db="hajj_info",
					port=1337)
cur = db.cursor()
cur.execute("SELECT * FROM personal_info")

