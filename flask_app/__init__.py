from flask import Flask

UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = "thisismysecretkey"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER