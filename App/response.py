from flask import jsonify, make_response # import library jsonify dan make response dari flask

# ketika sukses akan mengambil parameter nilai (values) dan message (pesan)
def success (values, message):
  res = {
    'data' : values,
    'message' : message
  }
  return make_response(jsonify(res)), 200 # akan return data 'res' dengan format jsonify, dengan kode 200 (berhasil)


# ketika gagal akan mengambil parameter nilai (values) dan message (pesan)
def badRequest (values, message):
  res = {
    'data' : values,
    'message' : message
  }
  return make_response(jsonify(res)), 400 # akan return data 'res' dengan format jsonify, dengan kode 400 (gagal)

