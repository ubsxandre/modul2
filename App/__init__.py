from flask import Flask, redirect
from flask_mysqldb import MySQL # library untuk konek ke MySQL
from flask_sqlalchemy import SQLAlchemy
from App import config
# from flask import redirect
import MySQLdb.cursors
import pymysql
# import json



app = Flask(__name__) # --- app(variabel) yang sudah di deklarasi yang digunkan di route dan akan dijalankan di run.py --- #
mysql = MySQL(app)
curMysql = MySQLdb.cursors.DictCursor
db = SQLAlchemy(app)
app.config.from_object(config.Config)  # 

# from App.karyawan import karyawanController # bisa di model kyk gini, atau di import di karyawan/routes.py -- from App import karyawanController
from App.karyawan import routes # --- import dari setiap route folder yang nantinya akan di jalankan ke run.py --- #
from App.gaji import routes
from App import first_routes

