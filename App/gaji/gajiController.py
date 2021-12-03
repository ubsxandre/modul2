from App import app, response, mysql, curMysql
from flask import request, jsonify

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