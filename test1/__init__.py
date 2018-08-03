from flask import Flask,render_template,request,jsonify,redirect,url_for
import pyqrcode
import pyqrcode
import sqlite3
import hashlib
import os
from flask_restful import Resource, Api
import MySQLdb
from sqlalchemy import create_engine
from json import dumps
from flask_httpauth import HTTPBasicAuth
#from flask.ext.jsonpify import jsonify
import MySQLdb
import _mysql
db = MySQLdb.connect(host="10.0.4.146",
                    user="root",
                    passwd="1234",
                    db="hajj_info",
                    port=1337)

class userprofile(Resource):
    def get(self):
        cur = db.cursor()
        query=cur.execute("select * from personal_info")
        data =  cur.fetchall()
        return {'User': [i for i in data]}


PEOPLE_FOLDER = os.path.join('static', 'data_images')
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER
api=Api(app)
@app.route('/')
def homepage():
    return render_template("index.html")

@app.route('/users/<string:num>',methods=['GET'])
def get(num):
    a=num
    print(a)

    cur = db.cursor()
    data = cur.fetchone()
    a=jsonify(data)
    #data=list(data)
    #return a
    db.close()
    return {'User': [i for i in data]}

    #return jsonify(data)

@app.route('/login', methods=['GET', 'POST'])
def login():
     error = None
     if request.method == 'POST':
         if request.form['id'] != 'admin' or request.form['pass'] != 'admin':
             error = 'Invalid Credentials. Please try again.'
         else:
             return redirect(url_for('qr'))
     else:

         return render_template('login.html', error=error)


@app.route('/qr.html', methods=['GET', 'POST'])
def qr():
    if request.method == 'POST':
          nm = request.form['Full_name']
          nat = request.form['Nationality']
          age = request.form['Age']
          phone_number = request.form['Phone_number']
          passport = request.form['passport_number']
          #print(nm,nat,age,phone_number,passport)
          cur = db.cursor()
          print('check')
          cur.execute("SELECT passport_number FROM personal_info WHERE passport_number=?",(passport,))
          data=cur.fetchall()
          print(data,'herer is data')
          print('att pass')
          if len(data)!= 0:
              ms = 'value exist'
              return render_template("qr.html")
              flash('exist')

          else:
              cur = db.cursor()
              print('in else boii')
              cur.execute('INSERT INTO personal_info(Full_name,Nationality,Age,Phone_Number,passport_number) VALUES(?,?,?,?,?)', (nm,nat,age,phone_number,passport))
              cur.commit()
              print('done')
              msg = "Record successfully added"
              cur.execute("SELECT ID FROM personal_info WHERE  Full_name=? AND  Passport_number=?",(nm, passport))
              l=cur.fetchall()
              row = [item[0] for item in l]
              row=row[0]
            #hashlib
              a=bytes(row,'utf-8')
              has = hashlib.sha256(a)
              print(has.hexdigest())
              has=has.hexdigest()
              #cur.execute('INSERT INTO personal_info(Full_name
          #generating images
              save_path='static/data_images'
              compl = os.path.join(save_path,has)
              l = has
              #nm +' '+city+' '+
              q = pyqrcode.create(l)
              q.png(compl +'.png',scale=6)
              full_filename = os.path.join(app.config['UPLOAD_FOLDER'],has+'.png')
              return render_template("qr.html",image_name=full_filename)
              cur.close()
        #except:
         # print('in except')
          #cur=db.cursor()
          #msg = "error in insert operation"
         # cur.close()
         # return render_template("qr.html")

    else:
        return render_template("qr.html")



api.add_resource(userprofile, '/users')



if __name__ == "__main__":
    app.run(host='10.0.4.148',debug=True)
