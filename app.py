from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
import os

app = Flask(__name__)
CORS(app)

@app.route('/app/contact', methods=[POST])
def contact():
    data = request.json
    