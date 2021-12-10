from App import app, response, mysql, curMysql, db
from App.gaji import modelGaji
from flask import request, jsonify, send_file, Response, redirect
from io import BytesIO, TextIOWrapper
import datetime, io, numpy as np, pandas as pd, xlrd, csv, os, datetime

def tabel_gaji_get_nik(nik):  # Simpan dulu
  try:
    cur = mysql.connection.cursor(curMysql)     # akses ke database
    cur.execute('SELECT tanggal_gajian, nik, salary, gaji_ke FROM zzz_dummy_salary WHERE nik = %s ORDER BY nik, gaji_ke', (nik,)) 
    data = cur.fetchall()               # Fetch data dari query Select
    cur.close()
    # return response.success(data, "success")
    # return str(data)
    # return 'tes'
    return data
  except Exception as e:
    print(e)

def tabel_gaji_get():
  try:
    cur = mysql.connection.cursor(curMysql)     # akses ke database
    cur.execute('SELECT tanggal_gajian, nik, salary, gaji_ke FROM zzz_dummy_salary ORDER BY nik, gaji_ke') 
    data = cur.fetchall()               # Fetch data dari query Select
    cur.close()
    return response.success(data, "success")
    # return str(data)
    # return 'tes'
  except Exception as e:
    print(e)
  

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
    'tanggal_gajian':data.tanggal_gajian,
    'salary':data.salary,
    'gaji_ke':data.gaji_ke      # dan bisa menampilkan kolom lain - tergantung querymu lur
  }
  return data





##      IMPORT DAN EXPORT 
# ===================================== IMPORT (CSV)    
def transform(text_file_contents):
    return text_file_contents.replace("=", ",")

def uploadfilesGaji_csv():
    if request.method == 'POST':
        csv_file = request.files['file']    # nama file yang di upload menggunakan form di HTML
        csv_file = TextIOWrapper(csv_file, encoding='utf-8')    # wrapper
        csv_reader = csv.reader(csv_file, delimiter=',', )        # jadi kalau csv kan pemisahan kolomnya menggunakan koma (delimiternya). Untuk baca delimiternya itu lho
        for row in csv_reader:              # looping untuk membaca data dari csv per cell nya
            # sysdate = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')    
            # v_tgl_gajian = row[1]
            v_tgl_gajian = datetime.datetime.strptime(row[1], "%m/%d/%Y %H:%M")
            new_menu = modelGaji.zzz_dummy_salary(nik=row[0], tanggal_gajian=v_tgl_gajian, gaji_ke=row[2], salary=row[3])
            db.session.add(new_menu)
            db.session.commit()
        return redirect('/tabel-gaji')
        # return jsonify(v_tgl_gajian)
    # return render_template('/karyawan/uploadFileKaryawan.html')
  
  

# ===================================== IMPORT (Excel)   
def uploadfilesGaji_excel():
  if request.method == 'POST':
    excel_file = request.files['file']
    # csv_file = os.path.abspath(os.path.dirname(__file__))
    book = xlrd.open_workbook(file_contents=excel_file.read())
    # book = xlrd.open_workbook(r'C:\xampp\htdocs\python\coba_read_write_excel\testing.xls')
    # print("The number of worksheets is {0}".format(book.nsheets))
    # print("Worksheet name(s): {0}".format(book.sheet_names()))
    sh = book.sheet_by_index(0)
    # print("{0} {1} {2}".format(sh.name, sh.nrows, sh.ncols))
    print("Cell row1 , col 1 == {0}".format(sh.cell_value(rowx=1, colx=1)))
    for row in range(sh.nrows):
      # tes = sh.cell_value(rowx=row, colx=0)
      # sysdate = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
      # seconds = (sh.cell_value(rowx=row, colx=4) - 25569) * 86400.0
      # v_tgl_kerja = datetime.datetime.utcfromtimestamp(seconds).strftime('%Y-%m-%dT%H:%M:%S')
      # datetime.datetime(2018, 1, 11, 0, 0)
      new_menu = modelGaji.zzz_dummy_table(nik=sh.cell_value(rowx=row, colx=0), tanggal_gajian=sh.cell_value(rowx=row, colx=1), gaji_ke=sh.cell_value(rowx=row, colx=2), salary=sh.cell_value(rowx=row, colx=3))
      db.session.add(new_menu)
      db.session.commit()
    # return jsonify(v_tgl_kerja)
    return redirect('/tabel-gaji')
  # return render_template('/karyawan/uploadFileKaryawan_excel.html')
  
  
  
# ===================================== EXPORT (csv)  
def downloadfileGaji_csv():
		cur = mysql.connection.cursor(curMysql)
		
		cur.execute('''SELECT DATE_FORMAT(tanggal_gajian, '%m-%d-%Y %H:%i:%s') as tanggal_gajian, nik, salary, gaji_ke FROM zzz_dummy_salary ORDER BY nik, gaji_ke''') 
		result = cur.fetchall()

		output = io.StringIO()
		writer = csv.writer(output)
		
		line = ['NIK, Tanggal Gajian, Gaji Ke-, Gaji']
		writer.writerow(line)

		for row in result:
			line = [str(row['nik']) + ',' + row['tanggal_gajian'] + ',' + str(row['gaji_ke']) + ',' + str(row['salary']) ]
			writer.writerow(line)

		output.seek(0)
		
		return Response(output, mimetype="text/csv", headers={"Content-Disposition":"attachment;filename=Salary.csv"})


# # ====================================== EXPORT (Excel)
def downloadfileGaji_excel():
  # return redirect(url_for('tabelGaji'))

    ## create a random Pandas dataframe
    # df_1 = pd.DataFrame(np.random.randint(0,10,size=(10, 4)), columns=list('ABCD'))
    cur = mysql.connect
    df_1 = pd.read_sql_query('''SELECT DATE_FORMAT(tanggal_gajian, '%m-%d-%Y %H:%i:%s') as tanggal_gajian, nik, salary, gaji_ke FROM zzz_dummy_salary ORDER BY nik, gaji_ke''', cur)   # sementara tanpa filter dulu, jadi export whole data from some table 

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
    return send_file(output, attachment_filename="Salary.xlsx", as_attachment=True)
  
  
