from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
import imaplib
import email

app = Flask(__name__)

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your_password'
mail = Mail(app)

# Email fetching function
def fetch_emails():
    # Connect to the email server
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login('your_email@gmail.com', 'your_password')
    mail.select('inbox')

    # Search for all emails
    result, data = mail.search(None, 'ALL')
    email_ids = data[0].split()

    emails = []
    for e_id in email_ids[-10:]:  # Fetch the last 10 emails
        result, msg_data = mail.fetch(e_id, '(RFC822)')
        msg = email.message_from_bytes(msg_data[0][1])
        emails.append({
            'subject': msg['subject'],
            'from': msg['from'],
            'date': msg['date'],
            'body': msg.get_payload(decode=True).decode()
        })

    mail.logout()
    return emails

@app.route('/')
def index():
    emails = fetch_emails()
    return render_template('index.html', emails=emails)

@app.route('/send', methods=['POST'])
def send_email():
    subject = request.form['subject']
    body = request.form['body']
    msg = Message(subject, sender='your_email@gmail.com', recipients=['recipient@example.com'])
    msg.body = body
    mail.send(msg)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
