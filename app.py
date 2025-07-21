from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.message import EmailMessage
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://ursulashrestha.com.np"}})

@app.route('/contact', methods=['POST'])
def contact():
    if request.method == 'OPTIONS':
        # Handle preflight request
        return '', 204
    data = request.json
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')

    if not all([name, email, message]):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        send_email(name, email, message)
        return jsonify({'success': 'Message sent successfully'}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': 'Failed to send message'}), 500

def send_email(name, email, message):
    SMTP_SERVER = 'smtp-relay.brevo.com'
    SMTP_PORT = 587
    SMTP_LOGIN = os.environ.get('BREVO_LOGIN')  
    SMTP_PASSWORD = os.environ.get('BREVO_SMTP_KEY')
    RECEIVER_EMAIL = os.environ.get('RECEIVER_EMAIL')

    msg = EmailMessage()
    msg['Subject'] = f'New message from {name}'
    msg['From'] = SMTP_LOGIN
    msg['To'] = RECEIVER_EMAIL
    msg.set_content(f"""
    Name: {name}
    Email: {email}
    Message:
    {message}
    """)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(SMTP_LOGIN, SMTP_PASSWORD)
        smtp.send_message(msg)

if __name__ == '__main__':
    app.run(debug=True)
