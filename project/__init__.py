from flask import Flask


app = Flask(__name__)
app.secret_key='mayur'


import project.com.controller