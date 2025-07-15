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
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')

    content = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
    msg = MIMEText(content)
    msg['Subject'] = 'New Message from Portfolio Contact Form'
    msg['From'] = os.environ['EMAIL_USER']
    msg['To'] = os.environ['EMAIL_TO']

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(os.environ['EMAIL_USER'], os.environ['EMAIL_PASS'])
            smtp.send_message(msg)
        return jsonify({'status': 'sent'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

