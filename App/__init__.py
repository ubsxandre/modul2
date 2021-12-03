from flask import Flask
from flask_mysqldb import MySQL # library untuk konek ke MySQL
from flask import redirect
import MySQLdb.cursors
# import json

app = Flask(__name__) # --- app(variabel) yang sudah di deklarasi yang digunkan di route dan akan dijalankan di run.py --- #
mysql = MySQL(app)
curMysql = MySQLdb.cursors.DictCursor


# from App.karyawan import karyawanController # bisa di model kyk gini, atau di import di karyawan/routes.py -- from App import karyawanController
from App.karyawan import routes # --- import dari setiap route folder yang nantinya akan di jalankan ke run.py --- #
from App.gaji import routes
from App import first_routes

