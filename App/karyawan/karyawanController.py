from flask.helpers import url_for
from werkzeug.utils import redirect
from App import app, response, mysql, curMysql, db
from App.karyawan import modelKaryawan
from App.gaji import gajiController
from flask import request, jsonify, Response, flash, render_template, send_file
from io import BytesIO, TextIOWrapper
import numpy as np, pandas as pd, xlrd, csv, os, datetime, io



# ===================================== GET (SELECT)
# ------------------------ GET Karyawan (Data karyawan)
def tabel_karyawan_get():   # Show all data karyawan without condition
  try:
    cur = mysql.connection.cursor(curMysql)     # akses ke database
    cur.execute('''SELECT a.nik, a.first_name, a.last_name, a.golongan, a.tgl_kerja, b.status as status_aktif, a.tgl_input 
                FROM zzz_dummy_table a , zzz_dummy_sts_aktif b
                WHERE a.status_aktif = b.id_status 
                ORDER BY a.nik''') 
    data = cur.fetchall()               # Fetch data dari query Select
    cur.close()
    return response.success(data, "success")
    # return str(data)
    # return 'tes'
  except Exception as e: 
    print(e)

def tabel_karyawan_nik_get(nik):   # Show all data karyawan with condition NIK
  try:
    cur = mysql.connection.cursor(curMysql)     # akses ke database
    cur.execute('''SELECT nik, first_name, last_name, golongan, tgl_kerja, status_aktif, tgl_input 
                FROM zzz_dummy_table
                WHERE status_aktif = '1'
                  AND nik = %s
                ORDER BY nik''', (nik,)) 
    data = cur.fetchone()               # Fetch data dari query Select
    cur.close()
    return data
    # return str(data)
    # return 'tes'
  except Exception as e:
    print(e)

# ------------------------ GET Detail Karyawan x Gaji
def tabel_kar_gaji_get(nik):
  try:
    cur = mysql.connection.cursor(curMysql)     # akses ke database 
    cur.execute('''SELECT nik, first_name, last_name, golongan, tgl_kerja, status_aktif, tgl_input 
                FROM zzz_dummy_table
                WHERE status_aktif = '1'
                  AND nik = %s
                ORDER BY tgl_input''', (nik,))  # Query tabel karyawan
    dataK = cur.fetchone()               # Fetch data dari query Select
           
    # cur2 = mysql.connection.cursor(curMysql)     # akses ke database
    # cur2.execute('''SELECT tanggal_gajian, nik, salary, gaji_ke 
    #             FROM zzz_dummy_salary
    #             WHERE nik = %s
    #             ORDER BY nik, gaji_ke''', (nik,))  # Query tabel gaji   
    # dataG = cur2.fetchall()               # Fetch data dari query Select
    
    # dataG = gajiController.tabel_gaji_get_nik(nik)
        
    if not dataK:
      return response.badRequest([], 'Data karyawan tidak ada !!')
    
    dataasdasd = gajiController.tabel_gaji_get_nik(nik)   # Tidak perlu di ubah ker format array karena outputan mysqldb default nya adlh array
    data = singleDetailKaryGaji(dataK, dataasdasd)    
    
    # return jsonify(dataK)
    return  response.success(data, "success")
    # return print(json.dumps(dataK))
    # return dataG
  except Exception as e:
    print(e)
    

def singleDetailKaryGaji(v_karyawan,v_gaji):
  data = {
    # 'nik':v_karyawan.nik,
    'nik':v_karyawan.get("nik"),
    'first_name':v_karyawan.get("first_name"),
    'last_name':v_karyawan.get("last_name"),
    'golongan':v_karyawan.get("golongan"),
    'status_aktif':v_karyawan.get("status_aktif"),
    'tanggal_kerja':v_karyawan.get("tgl_kerja"),
    # 'golongan':v_karyawan.golongan,
    # 'tgl_kerja':v_karyawan.tgl_kerja,
    # 'status_aktif':v_karyawan.status_aktif
    'gaji': v_gaji  # nah detail gaji akan ditempatkan disini, jadi nested di jsonnya. Setiap karyawan akan ditampilkan gajinya
  }
  return data
  
### ==================================================
### Ini untuk format menggunakan SQLAlchemy. 
### Tetapi pakai mysqldb saja karena sudah terbiasa dengan Query. Markicooobbbb!!!
### Kalau menggunakan mysqldb tidak perlu query di bawah ini. langsung def tabel_karyawan_get() 
'''
def formatArray(datas):
  array = []  
  for i in datas:
    array.append(singleObject(i)) # INGAT pelajaran di w3school tentang Lists, Tuples, Sets, DIctionaries ? nah ini method yang ada di Lists
                    # menambahkan di arraynya
                    # membuat Function singleDosen dulu
  return array

def singleObject(data):
  data={
    'nik':data.nik,
    'first_name':data.first_name,
    'last_name':data.last_name      # dan bisa menampilkan kolom lain - tergantung querymu lur
  }
  return data
'''



# ===================================== POST (INSERT)
def saveKaryawan():     # INGAAATT !!! Masih proteksi EXCEPTION jika error, kalau input data double langsung error (bukan show message custom / handlingnya blm ada)
  try:
    nik = request.form.get('nik')         # Ini yang bikin lama, gara2 lupa konsep dictionary. Kebingungan syntax untuk manggil nama kolomnya
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    golongan = request.form.get('golongan')
    tgl_kerja = request.form.get('tgl_kerja')
    status_aktif = request.form.get('status_aktif')
    tgl_input = request.form.get('tgl_input')
    
    dataK = tabel_karyawan_nik_get(nik)
    
    teslen = dataK.get('nik')
    
    cursor = mysql.connection.cursor(curMysql)
    cursor.execute('''INSERT INTO zzz_dummy_table (TGL_INPUT, NIK, FIRST_NAME, LAST_NAME, GOLONGAN, STATUS_AKTIF, TGL_KERJA) VALUES (SYSDATE(), %s, %s, %s, %s, %s, STR_TO_DATE(%s, '%%Y-%%m-%%dT%%H:%%i'))''', (nik, first_name, last_name, golongan, status_aktif,tgl_kerja))
    mysql.connection.commit() # Insert format tanggal menggunakan postman masih blm bisa
    cursor.close()
    # returnnya
    return response.success('', 'Sukses menambahkan data karyawan')
    
    # if teslen is None :   # Cek datanya ada atau tidak
    #   # koneksi ke database
    #   cursor = mysql.connection.cursor(curMysql)
    #   cursor.execute('''INSERT INTO zzz_dummy_table (TGL_INPUT, NIK, FIRST_NAME, LAST_NAME, GOLONGAN, STATUS_AKTIF, TGL_KERJA) VALUES (SYSDATE(), %s, %s, %s, %s, %s, STR_TO_DATE(%s, '%%Y-%%m-%%dT%%H:%%i'))''', (nik, first_name, last_name, golongan, status_aktif,tgl_kerja))
    #   mysql.connection.commit() # Insert format tanggal menggunakan postman masih blm bisa
    #   cursor.close()
    #   # returnnya
    #   return response.success('', 'Sukses menambahkan data karyawan')
    # else:
    # #   return response.badRequest([], "Error / NIK sudah pernah dipakai !!!")    
    #   return  response.badRequest(nik, "Error / NIK sudah pernah dipakai !!!")    
  except Exception as e:
    print(e)
    

# ===================================== PUT (Update)
def updateKaryawan(nik):
  try:
    first_name = request.form.get('first_name') # get value dari postman saat PUT berlangsung
    last_name = request.form.get('last_name')
    golongan = request.form.get('golongan')
    tgl_kerja = request.form.get('tgl_kerja')
    status_aktif = request.form.get('status_aktif')
    note = request.form.get('note')
    
    old_dataK = tabel_karyawan_nik_get(nik)
    
    if not old_dataK:
      return response.badRequest([], 'Data karyawan tidak ada !!')
    
    input = [   # kurung siku adalah array object. Menampilkan dalam variabel input
      {
        'a_old_data':'data_lama',
        'nik':nik,
        'first_name':old_dataK.get('first_name'),
        'last_name':old_dataK.get('last_name'),
        'golongan':old_dataK.get('golongan'),
        'tgl_kerja':old_dataK.get('tgl_kerja'),
        'status_aktif':old_dataK.get('status_aktif'),
        'note':old_dataK.get('note')      
      },
      {         # Data ditampung untuk ditampilkan saat respons berhasil
        'new_data':'data_baru',
        'nik':nik,
        'first_name':first_name,
        'last_name':last_name,
        'golongan':golongan,
        'tgl_kerja':tgl_kerja,
        'status_aktif':status_aktif,
        'note':note
      }
    ]
    
    ## Untuk tes aja. Ignore this !!
    # cur = mysql.connection.cursor(curMysql)     # akses ke database
    # cur.execute('''SELECT nik, first_name, last_name, golongan, tgl_kerja, status_aktif, tgl_input 
    #             FROM zzz_dummy_table
    #             WHERE status_aktif = '1'
    #               AND nik = %s
    #             ORDER BY tgl_input''', (nik,))  # Query tabel karyawan
    # dataK = cur.fetchone()               # Fetch data dari query Select
    
    cur = mysql.connection.cursor(curMysql)     # akses ke database
    cur.execute("""
               UPDATE zzz_dummy_table
               SET FIRST_NAME=%s,
                  LAST_NAME=%s,
                  GOLONGAN=%s
               WHERE nik=%s
            """, (first_name, last_name, golongan, nik))
    
    # dataK["first_name"] = first_name
    # dataK["last_name"] = last_name
    # dataK["golongan"] = golongan
    # dataK["tgl_kerja"] = tgl_kerja
    # dataK["status_aktif"] = status_aktif
    # dataK["note"] = note
    
    
    mysql.connection.commit()
    cur.close()
    return response.success(input, 'succes update !!') # Menampilkan data yang di update melalui postman. Kalau ga di update value nya null
  except Exception as e:
    print(e)
    
    
# ===================================== PUT (Delete)
def deleteKaryawan(nik):
  try:
    dataK = tabel_karyawan_nik_get(nik)
    
    if dataK is None:   # Cek datanya ada atau tidak
      return response.badRequest([], "NIK yang dicari tidak ada")
    else:
      cur = mysql.connection.cursor(curMysql)
      cur.execute("DELETE FROM zzz_dummy_table WHERE nik=%s", (nik,))
      mysql.connection.commit()
      cur.close()
      return response.success(nik, "Data berhasil dihapus !!!")
  except Exception as e:
    print(e)




    
    
##      IMPORT DAN EXPORT 
# ===================================== IMPORT (CSV)   
def readFileExt(fileUpload):    # membaca ext
  namaFile, namaExt = os.path.splitext(fileUpload)
  return namaExt

 
def transform(text_file_contents):
    return text_file_contents.replace("=", ",")

def uploadfiles_csv():
    if request.method == 'POST':
        csv_file = request.files['file']    # path yang di upload menggunakan form di HTML
        csv_file_name = request.files['file'].filename   # ambil nama file dan ext yang di upload
        readFileExt(csv_file_name)
        csv_file = TextIOWrapper(csv_file, encoding='utf-8')    # wrapper
        csv_reader = csv.reader(csv_file, delimiter=',')        # jadi kalau csv kan pemisahan kolomnya menggunakan koma (delimiternya). Untuk baca delimiternya itu lho
        next(csv_reader)  # skip baris pertama
        for row in csv_reader:              # looping untuk membaca data dari csv per cell nya
            sysdate = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')     
            v_tgl_kerja = datetime.datetime.strptime(row[4], "%m/%d/%Y %H:%M")
            new_menu = modelKaryawan.zzz_dummy_table(nik=row[0], first_name=row[1], last_name=row[2], golongan=row[3], tgl_kerja=v_tgl_kerja,  status_aktif=row[5], tgl_input=sysdate, note='')
            db.session.add(new_menu)
            db.session.commit()
        flash(csv_file_name + ' berhasil di upload')
        return redirect('/tabel-karyawan')
        # return jsonify(v_tgl_kerja)
    # return render_template('/karyawan/uploadFileKaryawan.html')
  
  

# ===================================== IMPORT (Excel)   
def uploadfiles_excel():
  if request.method == 'POST':
    excel_file = request.files['file']
    excel_file_name = request.files['file'].filename
    # csv_file = os.path.abspath(os.path.dirname(__file__))
    book = xlrd.open_workbook(file_contents=excel_file.read())
    # book = xlrd.open_workbook(r'C:\xampp\htdocs\python\coba_read_write_excel\testing.xls')
    # print("The number of worksheets is {0}".format(book.nsheets))
    # print("Worksheet name(s): {0}".format(book.sheet_names()))
    sh = book.sheet_by_index(0)
    # print("{0} {1} {2}".format(sh.name, sh.nrows, sh.ncols))
    print("Cell row1 , col 1 == {0}".format(sh.cell_value(rowx=1, colx=1)))
    for row in range(1, sh.nrows):
      # tes = sh.cell_value(rowx=row, colx=0)
      sysdate = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
      seconds = (sh.cell_value(rowx=row, colx=4) - 25569) * 86400.0
      v_tgl_kerja = datetime.datetime.utcfromtimestamp(seconds).strftime('%Y-%m-%dT%H:%M:%S')
      # datetime.datetime(2018, 1, 11, 0, 0)
      new_menu = modelKaryawan.zzz_dummy_table(nik=sh.cell_value(rowx=row, colx=0), first_name=sh.cell_value(rowx=row, colx=1), last_name=sh.cell_value(rowx=row, colx=2), golongan=sh.cell_value(rowx=row, colx=3), tgl_kerja=v_tgl_kerja,  status_aktif=sh.cell_value(rowx=row, colx=5), tgl_input=sysdate, note='')
      db.session.add(new_menu)
      db.session.commit()
    # return jsonify(v_tgl_kerja)
    flash(excel_file_name + ' berhasil di upload')
    return redirect('/tabel-karyawan')
  # return render_template('/karyawan/uploadFileKaryawan_excel.html')
  
  
  
# ===================================== EXPORT (csv)  
def downloadfile_csv():
		cur = mysql.connection.cursor(curMysql)
		
		cur.execute('''SELECT a.nik, a.first_name, a.last_name, a.golongan, DATE_FORMAT(a.tgl_kerja, '%m-%d-%Y %H:%i:%s') as tgl_kerja, 
                b.status as status_aktif, 
                DATE_FORMAT(a.tgl_input, '%m-%d-%Y %H:%i:%s') as tgl_input
                FROM zzz_dummy_table a , zzz_dummy_sts_aktif b
                WHERE a.status_aktif = b.id_status 
                ORDER BY a.nik''') 
		result = cur.fetchall()

		output = io.StringIO()
		writer = csv.writer(output)
		
		line = ['nik, First Name, Last Name, Golongan, Tgl Kerja, Status Aktif, Tgl Input']
		writer.writerow(line)

		for row in result:
			line = [str(row['nik']) + ',' + row['first_name'] + ',' + row['last_name'] + ',' + row['golongan'] + ',' + row['tgl_kerja'] + ',' + row['status_aktif'] + ',' + row['tgl_input'] ]
			writer.writerow(line)

		output.seek(0)
		
		return Response(output, mimetype="text/csv", headers={"Content-Disposition":"attachment;filename=employee_report.csv"})


# ====================================== EXPORT (Excel)
def downloadfile_excel():
  # return redirect(url_for('tabelGaji'))

    ## create a random Pandas dataframe
    # df_1 = pd.DataFrame(np.random.randint(0,10,size=(10, 4)), columns=list('ABCD'))
    cur = mysql.connect
    df_1 = pd.read_sql_query('''SELECT a.nik, a.first_name, a.last_name, a.golongan, a.tgl_kerja, b.status as status_aktif, a.tgl_input 
                FROM zzz_dummy_table a , zzz_dummy_sts_aktif b
                WHERE a.status_aktif = b.id_status 
                ORDER BY a.nik''', cur)   # sementara tanpa filter dulu, jadi export whole data from some table 

    #create an output stream
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')

    #taken from the original question
    df_1.to_excel(writer, startrow = 0, merge_cells = False, sheet_name = "Sheet_1")
    workbook = writer.book
    worksheet = writer.sheets["Sheet_1"]    # penamaan sheet
    format = workbook.add_format()          #
    format.set_bg_color('#eeeeee')          # set default color
    worksheet.set_column(1,9,28)            # set column size

    #the writer has done its job
    writer.close()

    #go back to the beginning of the stream
    output.seek(0)

    #finally return the file
    return send_file(output, attachment_filename="testing.xlsx", as_attachment=True)
  
  
  
  
  
  
  ### IMPORT DAN EXPORT UNTUK REPORT
  # ===================================== EXPORT (csv report)  
def downloadfile_csv_report():
  cur = mysql.connection.cursor(curMysql)
  
  cur.execute('''SELECT a.NIK,
              CONCAT(a.FIRST_NAME , a.LAST_NAME) AS NAMA,
              a.GOLONGAN,
              DATE_FORMAT(B.TANGGAL_GAJIAN ,'%m-%d-%Y %H:%i:%s') AS TANGGAL_GAJIAN,
              b.TANGGAL_GAJIAN,
              b.GAJI_KE,
              b.SALARY,
              DATE_FORMAT(A.TGL_KERJA ,'%m-%d-%Y %H:%i:%s') AS TGL_MASUK_KERJA,
              c.status AS STATUS_KARYAWAN
          FROM zzz_dummy_table a, zzz_dummy_salary b, zzz_dummy_sts_aktif c
          WHERE a.NIK = b.NIK
            AND a.status_aktif = c.id_status
          ORDER BY A.NIK, B.GAJI_KE;''')
  result = cur.fetchall()

  output = io.StringIO()
  writer = csv.writer(output)
  
  line = ['NIK, Nama, Golongan, Tanggal Gajian, Gaji ke-, Salary, Tanggal Masuk Kerja, Status Karyawan']
  # line = ['NIK, Nama, Golongan, Tanggal Gajian, Gaji ke -, Salary, ']
  writer.writerow(line)

  for row in result:
    # line = [str(row['NIK']) + ',' + row['NAMA'] + ',' + row['GOLONGAN'] + ',' + row['TANGGAL_GAJIAN'] + ',' + row['GAJI_KE'] + ',' + row['SALARY'] + ',' + row['TGL_MASUK_KERJA'] + ',' + row['STATUS_KARYAWAN']]
    line = [str(row['NIK']) + ',' + str(row['NAMA']) + ',' + row['GOLONGAN'] + ',' + row['TANGGAL_GAJIAN'] + ',' + str(row['GAJI_KE']) + ',' + str(row['SALARY']) + ',' + row['TGL_MASUK_KERJA'] + ',' + row['STATUS_KARYAWAN'] ]
    writer.writerow(line)

  output.seek(0)
  
  return Response(output, mimetype="text/csv", headers={"Content-Disposition":"attachment;filename=employee_salary_report.csv"})
  
  
  
  # ===================================== EXPORT (Excel report)  
  def downloadfile_excel():
  # return redirect(url_for('tabelGaji'))

    ## create a random Pandas dataframe
    # df_1 = pd.DataFrame(np.random.randint(0,10,size=(10, 4)), columns=list('ABCD'))
    cur = mysql.connect
    df_1 = pd.read_sql_query('''SELECT a.NIK,
              CONCAT(a.FIRST_NAME , a.LAST_NAME) AS NAMA,
              a.GOLONGAN,
              DATE_FORMAT(B.TANGGAL_GAJIAN ,'%m-%d-%Y %H:%i:%s') AS TANGGAL_GAJIAN,
              b.TANGGAL_GAJIAN,
              b.GAJI_KE,
              b.SALARY,
              DATE_FORMAT(A.TGL_KERJA ,'%m-%d-%Y %H:%i:%s') AS TGL_MASUK_KERJA,
              c.status AS STATUS_KARYAWAN
          FROM zzz_dummy_table a, zzz_dummy_salary b, zzz_dummy_sts_aktif c
          WHERE a.NIK = b.NIK
            AND a.status_aktif = c.id_status
          ORDER BY A.NIK, B.GAJI_KE;''', cur)   # sementara tanpa filter dulu, jadi export whole data from some table 

    #create an output stream
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')

    #taken from the original question
    df_1.to_excel(writer, startrow = 0, merge_cells = False, sheet_name = "Sheet_1")
    workbook = writer.book
    worksheet = writer.sheets["Sheet_1"]    # penamaan sheet
    format = workbook.add_format()          #
    format.set_bg_color('#eeeeee')          # set default color
    worksheet.set_column(1,9,28)            # set column size

    #the writer has done its job
    writer.close()

    #go back to the beginning of the stream
    output.seek(0)

    #finally return the file
    return send_file(output, attachment_filename="employee_salary_report.xlsx", as_attachment=True)
  
  



    

# 1. Lama dalam searching yang dikatakan konsultan tentang tidak menggunakan mvc.
# 2. Menggunakan template baru agar lebih rapi dan mudah mudah dalam maintaining.
# 3. Masih bingung tentang tidak menggunakan php, tapi menggunakan pythonnya. 
# 4. Dijelaskan fia tentang apa yang akan kami buat, jadi memahami dulu dan mencari konsep yang sesuai.

# 1. Sebenarnya sudah selesai modul 1 , 2 , 3 dari minggu lalu. tapi ada revisi dari meeting terakhir
# 2. 