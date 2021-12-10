import datetime
# from MySQLdb import DATETIME
from pandas.io.sql import to_sql
from App import app, mysql, curMysql, response, db  # --- import app(variable) dari file App/_init_.py yang sudah di deklarasi yang akan di gunakan di route --- #
from App.karyawan import karyawanController, modelKaryawan
from App.response import success
from flask import json, render_template, url_for, redirect, request, flash, send_file, jsonify, Response
# from flask_mysqldb import MySQL # library untuk konek ke MySQL
# import MySQLdb.cursors
import numpy as np
import pandas as pd
import xlrd, csv, os
# import xlsxwriter
# import flask_excel as excel
# import pyexcel as p
from io import BytesIO, TextIOWrapper
import io





# mysql = MySQL(app)

# Tes koneksi ke mysql

# @app.route('/tes-tampil-data-karyawan')
# def users():
#     cur = mysql.connection.cursor(curMysql)
#     cur.execute('''SELECT * from zzz_dummy_table''') # Coba exec query 
#     rv = cur.fetchall()
#     return str(rv) # Cetak hasil query ke dalam format string



# ------------------------------------- Tampilan Master (kodingan lawas dengan view css)
  # yang ini digunakan untuk nampilke data ke html / php (View nya lebih mendingan)
@app.route('/tabel-karyawan')         # URL 127.0.0.1:5000/tabel-karyawan untuk menampilkan data karyawan dari database
def tabelKaryawan():                          # function
  cur = mysql.connection.cursor()     # akses ke database
  cur.execute('''SELECT a.nik, a.first_name, a.last_name, a.golongan, b.status as status_aktif, a.tgl_kerja, a.status_aktif
                FROM zzz_dummy_table a , zzz_dummy_sts_aktif b
                WHERE a.status_aktif = b.id_status 
                ORDER BY a.nik''') 
  #cur.execute('SELECT * FROM zzz_dummy_table ORDER BY tgl_input')
  data=cur.fetchall()                 # Fetch data dari query Select
  cur.close()
  return render_template('karyawan/tabel-karyawan.php', dummy = data) # redirect ke tabel-karyawan.php




# ============================================ CRUD
# -------------------------------------------- Insert data karyawan (kodingan lawas dengan view css)
@app.route('/insert', methods=['POST'])
def nginputcoy():
  # submited
  if request.method == 'POST' and 'nik' in request.form and 'first_name' in request.form and 'last_name' in request.form and 'golongan' in request.form and 'tgl_kerja' in request.form: 
    
    # nik = request.post['nik']
    nik = request.form['nik']         # variabel untuk menyimpan value dari form di modal tabel.php
    fn = request.form['first_name']
    ln = request.form['last_name']
    gol = request.form['golongan']
    tgl_kerja = request.form['tgl_kerja']
    sts_aktif = request.form['sts_aktif']

    # Cek di tabel zzz_dummy_table apakah sudah ada record nik yang sudah tersimpan ?
    cursor = mysql.connection.cursor(curMysql)
    cursor.execute('SELECT * FROM zzz_dummy_table WHERE nik = %s', (nik,))
    sudahada = cursor.fetchone() 

    if sudahada:    # jika sudah maka akan muncul notifikasi dan tidak menjalankan query insert
        flash('Nik sudah pernah diinput !!') 
    elif not nik or not fn or not ln or not gol:  # jika form masih ada yang kosong maka kan ada notif dan tidak menjalankan query insert
        flash('Form harus terisi semua !!')       # flash adalah library tambahan untuk menyimpan message tanpa harus membuat variabel baru
    else:
        # NIK belum pernah di input dan form sudah terisi semua. Menjalankan query insert ke database
        cursor.execute('''INSERT INTO zzz_dummy_table (TGL_INPUT, NIK, FIRST_NAME, LAST_NAME, GOLONGAN, STATUS_AKTIF, TGL_KERJA) VALUES (SYSDATE(), %s, %s, %s, %s, %s, STR_TO_DATE(%s, '%%Y-%%m-%%dT%%H:%%i'))''', (nik, fn, ln, gol, sts_aktif,tgl_kerja))
        mysql.connection.commit()                 # commit setelah insert
        flash("Data Inserted Successfully")
  elif request.method == 'POST':          
        # Form is empty... (no POST data)     
        flash('Mohon isi form nya !!')
    # Show registration form with message (if any)
  return redirect(url_for('tabelKaryawan'))               # redirect function tabel






# -------------------------------------------- Delete (kodingan lawas dengan view css)

@app.route('/delete/<string:nik>', methods = ['GET'])
def delete(nik):
    flash("Berhasil delete !")
    cur = mysql.connection.cursor(curMysql)
    cur.execute("DELETE FROM zzz_dummy_table WHERE nik=%s", (nik,))
    mysql.connection.commit()
    return redirect(url_for('tabelKaryawan'))
  




# -------------------------------------------- Update (kodingan lawas dengan view css)

@app.route('/update',methods=['POST','GET'])
def update():

    if request.method == 'POST':
        nik = request.form['nik']
        fn = request.form['first_name']
        ln = request.form['last_name']
        gol = request.form['golongan']
        tgl_kerja = request.form['tgl_kerja']
        sts_aktif = request.form['sts_aktif']
        
        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE zzz_dummy_table
               SET FIRST_NAME=%s,
                  LAST_NAME=%s,
                  GOLONGAN=%s,
                  STATUS_AKTIF=%s
               WHERE nik=%s
            """, (fn, ln, gol, sts_aktif, nik))
        flash("Data Karyawan Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('tabelKaryawan'))
      
# <div class="form-group" >
#                           <h6 for="nik" >Tanggal Mulai Kerja</h6>
#                           <i class="fas fa-laugh"></i>
#                           </label>
#                           <input type="datetime-local" value="{{row.4.strftime('%Y-%m-%d %H:%M:%S')}}" name="tgl_kerja" id="tgl_kerja" required>
#                         </div>




# ============================================ Report / Combine data
# --------------------------------------------

@app.route('/report-gaji-karyawan')
def report_gaji_karyawan():             # function untuk menampilkan data hasil combine dari tabel karyawan dan tabel gaji
  cur = mysql.connection.cursor()
  cur.execute('''SELECT a.NIK,
                CONCAT(a.FIRST_NAME , a.LAST_NAME) AS NAMA,
                a.GOLONGAN,
                b.TANGGAL_GAJIAN,
                b.GAJI_KE,
                b.SALARY,
                DATE_FORMAT(A.TGL_KERJA ,'%Y-%m-%d') AS TGL_MASUK_KERJA,
                c.status AS STATUS_KARYAWAN
            FROM zzz_dummy_table a, zzz_dummy_salary b, zzz_dummy_sts_aktif c
            WHERE a.NIK = b.NIK
              AND a.status_aktif = c.id_status
            ORDER BY A.NIK, B.GAJI_KE;''')
  #cur.execute('SELECT * FROM zzz_dummy_table ORDER BY tgl_input')
  data=cur.fetchall()
  cur.close()
  return render_template('karyawan/report_karyawan.php', dummy = data)










# =============================================== Kodingan baru dengan konsep baru
# -------------------------- Read Data
# yang ini nampilke data tok dalam bentuk json di web browser / bisa lewat postman
@app.route('/tabel-karyawan-json', methods=['GET'])   # INGAATT!! GET itu untuk menampilkan data 
def karyawans():    
  return karyawanController.tabel_karyawan_get()

### Sebenarnya bisa GET dan POST dijadikan satu route dan diberi kondisi if else. tapi mari coba dipisah !!! 
### Modelnya seperti ini 
# @app.route('/tabel-karyawan-json', methods=['GET', 'POST'])  
# def karyawans():  
#   if request.method == 'GET':
#     return karyawanController.tabel_karyawan_get()
#   else:
#     return karyawanController.saveKaryawan() 



### -------------------------- INSERT  menggunakan POST
@app.route('/tabel-karyawan-json', methods=['POST'])   # GET dan POST dipisah
def karyawansInsert():    
  return karyawanController.saveKaryawan()


# -------------------------- Simple combine data from table x table (karyawan x gaji) == GET
# Update data == PUT
# Delete data == DELETE ** Tergantung request an
# yang ini nampilke data tok dalam bentuk json di web browser / bisa lewat postman
@app.route('/tabel-karyawan-json/<nik>', methods=['GET', 'PUT', 'DELETE'])   # DI function ini bukan hanya GET saja, nanti ditambahi PUT
def karsGaji(nik):
  if request.method == 'GET':
    return karyawanController.tabel_kar_gaji_get(nik)
  elif request.method == 'PUT':     # Nah ini elsenya adalah PUT untuk update data
    return karyawanController.updateKaryawan(nik)
  else:
    return karyawanController.deleteKaryawan(nik)
  
  
  
### Ignore this. Just for exercise !!!
# @app.route('/uploadfiles_csv', methods=['POST', 'GET'])   # Reading data from CSV and print into cmd
# # Get the uploaded files
# def uploadfiles_csv():
#     if request.method == 'POST':
#         csv_file = request.files['file']
#         csv_file = TextIOWrapper(csv_file, encoding='utf-8')
#         csv_reader = pd.read_csv(csv_file)
#         for row in csv_reader:
#             sysdate = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
#             # v_tgl_kerja = datetime.datetime.strptime(row[4], "%m/%d/%Y %H:%M")
#             # tetete = [
#             #   sysdate
#             # ]
#         # return redirect('/tabel-karyawan')
#         return jsonify(print(csv_reader))
#     return render_template('/karyawan/uploadFileKaryawan.html')
  
  
  
  
### Reading data from Excel and csv
## --------------------------- Import from csv
@app.route('/uploadfiles_csv', methods=['POST', 'GET'])   # Reading data from CSV and save to mysql using sqlalchemy
# Get the uploaded files
def import_csv():
  if request.method == 'POST':
    return karyawanController.uploadfiles_csv()
  return render_template('/karyawan/uploadFileKaryawan.html')

## --------------------------- Import from Excel
@app.route('/uploadfiles_excel', methods=['POST', 'GET'])   # Reading data from CSV and save to mysql using sqlalchemy
# Get the uploaded files
def import_excel():
  if request.method == 'POST':
    return karyawanController.uploadfiles_excel()
  return render_template('/karyawan/uploadFileKaryawan_excel.html')

## --------------------------- Export to csv
@app.route('/downloadfiles_csv')
def export_csv():
  return karyawanController.downloadfile_csv()
  
  
## --------------------------- Ecport to excel
@app.route('/downloadfiles_excel')
def export_exc():
  return karyawanController.downloadfile_excel()