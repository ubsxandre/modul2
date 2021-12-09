from App import db

class zzz_dummy_table(db.Model):
    nik = db.Column(db.String(6), primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    golongan = db.Column(db.String(100), nullable=False)
    tgl_kerja = db.Column(db.DateTime)
    status_aktif = db.Column(db.String(10), nullable=False)
    tgl_input = db.Column(db.DateTime, nullable=False)
    note = db.Column(db.String(100))

def __repr__(self):
  return '<zzz_dummy_table {}>'.format(self.name) # return ke Dosen {Andreas} misalnya
  
