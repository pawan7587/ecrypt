from flask import Flask, render_template, request, send_file, after_this_request
from werkzeug.utils import secure_filename
import pyAesCrypt
import os
app = Flask(__name__)

@app.route('/upload')
def upload_file():
   return render_template('upload.html')

@app.route('/encrypt', methods = ['POST'])
def uploadenc():
   bufferSize = 64 * 1024
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      uploads = os.path.join(os.getcwd(), f.filename)       
      password = request.form['text']
      encfile = f.filename + ".aes"
      pyAesCrypt.encryptFile(uploads, encfile , password , bufferSize) 
      @after_this_request
      def remove_enc(response):
         os.remove(uploads)
         os.remove(encfile)
         return response
      return send_file(encfile, as_attachment=True) 

@app.route('/reload', methods = ['POST'])
def reload():
   if request.method == 'POST':
      return render_template('upload.html') 

@app.route('/decrypt', methods = ['POST'])
def uploaddec():
   bufferSize = 64 * 1024
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      uploads = os.path.join(os.getcwd(), f.filename)       
      password = request.form['text']
      decfile = f.filename.split('.aes')
      pyAesCrypt.decryptFile(uploads, decfile[0], password, bufferSize) 
      @after_this_request
      def remove_dec(response):
         os.remove(uploads)
         os.remove(decfile[0])
         return response
      return send_file(decfile[0], as_attachment=True)


if __name__ == '__main__':
   app.run(debug = True)
