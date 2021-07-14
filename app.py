from flask import Flask, request, make_response, jsonify
from flask_mail import Mail, Message
from datetime import datetime
from twilio.rest import Client

import config

app = Flask(__name__)
app.config.from_object(config.Config)
mail = Mail(app)

twilio_num = app.config['TWILIO_NUM']
client = Client(app.config['TWILIO_SID'], app.config['TWILIO_TOKEN'])


def send_email_msg(sender, recipient, subject, text):
    msg = Message(
        subject = subject,
        sender = sender,
        recipients = [recipient],
        html = text
    )
    mail.send(msg)


def send_sms(recipient_num, text):
    client.messages.create(
        to = f'+{recipient_num}',
        from_ = twilio_num,
        body = text
    )


def results():
    req = request.get_json(force = True)

    date = datetime.fromisoformat(req.get('queryResult').get('parameters').get('date'))
    time = datetime.fromisoformat(req.get('queryResult').get('parameters').get('time'))
    day = str(date).split(' ')[0]
    time = time.time()
    email = req.get('queryResult').get('parameters').get('email')
    name = req.get('queryResult').get('parameters').get('name')
    recipient_num = int(req.get('queryResult').get('parameters').get('number'))

    text = f'Hello, {name}. Your appointment is scheduled for {day} at {time}'

    send_email_msg(app.config['MAIL_USERNAME'], email, 'Appointment', text)
    send_sms(recipient_num, text)

    return {'fulfillmentText': 'This is a response from webhook.'}


@app.route('/webhook', methods = ['GET', 'POST'])
def webhook():
    return make_response(jsonify(results()))


if __name__ == '__main__':
    app.run()
