from flask import render_template
from App import app

# ------------------------------------- Home 
# Routes di level 0 akan rendering tampilan home
@app.route('/')                       # otomatis memetakan ke URL default (localhost) 127.0.0.1:5000
def home():                           # fungsi home() dipanggil ketika URL default di akses
  return render_template('home.php')
