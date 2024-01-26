from flask import Flask


app= Flask(__name__)
app.secret_key = '1234567890123456'

from flask_app import routes