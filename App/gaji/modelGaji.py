from App import db

class zzz_dummy_salary(db.Model):
    nik = db.Column(db.String(6), primary_key=True)
    gaji_ke = db.Column(db.BigInteger, nullable=False)
    tanggal_gajian = db.Column(db.Date)
    salary = db.Column(db.Float, nullable=False)
    
def __repr__(self):
  return '<zzz_dummy_salary {}>'.format(self.name) # return ke Salary {NIK} misalnya
  