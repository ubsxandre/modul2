from App import app  # --- import app(variable) dari file App/_init_.py yang sudah di deklarasi yang akan di gunakan di route --- #
from App import mysql, curMysql
from App.gaji import gajiController
from flask import render_template, url_for, redirect, request, flash
# from flask_mysqldb import MySQL # library untuk konek ke MySQL
# import MySQLdb.cursors

# mysql = MySQL(app)

# Tes koneksi ke mysql

# @app.route('/tes-tampil-data-karyawan')
# def users():
#     cur = mysql.connection.cursor(curMysql)
#     cur.execute('''SELECT * from zzz_dummy_table''') # Coba exec query 
#     rv = cur.fetchall()
#     return str(rv) # Cetak hasil query ke dalam format string


# ------------------------------------- Tampilan Master

@app.route('/tabel-gaji')         # URL 127.0.0.1:5000/tabel-karyawan untuk menampilkan data karyawan dari database
def tabelGaji():                          # function
  cur = mysql.connection.cursor()     # akses ke database
  cur.execute('SELECT tanggal_gajian, nik, salary, gaji_ke FROM zzz_dummy_salary ORDER BY nik, gaji_ke') 
  #cur.execute('SELECT * FROM zzz_dummy_table ORDER BY tgl_input')
  data=cur.fetchall()                 # Fetch data dari query Select
  cur.close()
  return render_template('gaji/tabel-gaji.php', dummy = data) # redirect ke tabel.php


@app.route('/tabel-gaji-json', methods=['GET'])   # INGAATT!! GET itu untuk menampilkan data
def gajis():
  return gajiController.tabel_gaji_get()



# ============================================ CRUD
# -------------------------------------------- Insert data karyawan
@app.route('/insert-gaji', methods=['GET', 'POST'])
def semoga_naik_gaji():
  # submited
  if request.method == 'POST' and 'tgl_gajian' in request.form and 'nik' in request.form and 'gaji' in request.form: 
    nik = request.form['nik']           # membuat variabel untuk menyimpan value dari form_nginput
    tg = request.form['tgl_gajian']
    gj = request.form['gaji']

    # Cek di tabel zzz_dummy_salary apakah sudah ada record nik yang sudah tersimpan ?
    cursor = mysql.connection.cursor(curMysql)
    cursor.execute('SELECT * FROM zzz_dummy_salary WHERE nik = %s AND tanggal_gajian= %s', (nik, tg))
    sudahada = cursor.fetchone() 

    if sudahada:
        flash('Data sudah ada !!') 
    elif not nik or not tg or not gj:
        flash('Masih ada form yang belum terisi !!') 
    else:
        cursor.execute('INSERT INTO zzz_dummy_salary (GAJI_KE, NIK, TANGGAL_GAJIAN, SALARY) VALUES (f_gaji_ke(%s), %s, %s, %s)', (nik, nik, tg, gj,))
        mysql.connection.commit()
        flash("Data Inserted Successfully")
  elif request.method == 'POST':
        flash('Mohon diisi formnya !!')
  return redirect(url_for('tabelGaji'))        




# -------------------------------------------- Delete

@app.route('/delete-gaji/<string:nik>,<string:gaji_ke>', methods = ['POST','GET'])
def delete_gaji(nik, gaji_ke):
    flash("Berhasil delete !")
    cur = mysql.connection.cursor(curMysql)
    cur.execute("DELETE FROM zzz_dummy_salary WHERE nik=%s AND gaji_ke=%s", (nik, gaji_ke))
    mysql.connection.commit()
    return redirect(url_for('tabelGaji'))

  

# -------------------------------------------- Update 

@app.route('/update-gaji', methods=['GET', 'POST'])
def semoga_lebih_baik():

    if request.method == 'POST':
        nik = request.form['nik']
        tg = request.form['tanggal_gajian']
        gk = request.form['gaji_ke']
        p_gk = request.form['p_gaji_ke']
        gj = request.form['gaji']
        
        cur = mysql.connection.cursor()
        # cur.execute('SELECT * FROM zzz_dummy_salary WHERE nik = %s AND gaji_ke= %s', (nik, gk))
        # sudahada = cur.fetchone() 

        # if sudahada:
        #   flash('Data sudah ada, Gagal Update !!') 
        # elif not nik or not tg or not gj:
        #   flash('Isinen kabeh !!') 
        # else:

        cur.execute("""
              UPDATE zzz_dummy_salary
              SET tanggal_gajian=%s,
                salary=%s
              WHERE nik=%s
              AND gaji_ke = %s
          """, (tg, gj, nik, p_gk))
        flash("Data Gaji Updated Successfully")
        mysql.connection.commit()
      
    # elif request.method == 'POST':
    #   flash('Isinen kabeh !!')
    # Show registration form with message (if any)
        return redirect(url_for('tabelGaji'))

