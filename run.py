from App import app   # --- Menjalankan app dari file App/_init_.py yang sudah di deklarasi --- #

app.secret_key = 'inipassword' # untuk proteksi extra

app.config['MYSQL_HOST']='localhost'  # dikoneksikan dengan database
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='ubs_univ'

if __name__ == '__main__':
    app.run()
