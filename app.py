from flask import Flask, request, make_response, jsonify
from flask_mail import Mail, Message
from datetime import datetime
from twilio.rest import Client
from amocrm.v2 import tokens

from Lead import Lead
import config

app = Flask(__name__)
app.config.from_object(config.Config)
mail = Mail(app)

twilio_num = app.config['TWILIO_NUM']
client = Client(app.config['TWILIO_SID'], app.config['TWILIO_TOKEN'])

tokens.default_token_manager(
    client_id = app.config['AMOCRM_INTEGRATION_ID'],
    client_secret = app.config['AMOCRM_SECRET'],
    subdomain = 'subdomain',
    redirect_url = 'https://<hex>.ngrok.io',
    storage = tokens.FileTokensStorage()
)
tokens.default_token_manager.init(
    code = app.config['AMOCRM_AUTH'],
    skip_error = True
)


def add_lead(name, number, email, date, time):
    """
    Add lead to amoCRM
    :param name: lead's name
    :param number: lead's phone number
    :param email: lead's email
    :param date: date of appointment
    :param time: time of appointment
    """
    lead = Lead(name = name,
                number = number,
                email = email,
                date = date,
                time = time)
    lead.create()

    # Should we use add_note() before or after lead.create() ???
    add_note(lead = lead,
             phone_number = number,
             email = email)


def add_note(lead: Lead, phone_number, email):
    """
    Add note to lead
    :param lead: lead a note will be added to
    :param phone_number: phone number
    :param email: email
    """
    lead.notes.create(text = f'Number for sms: {phone_number}, email: {email}')


def send_email_msg(sender, recipient, subject, text):
    """
    Send email message after appointment intent is executed
    :param sender: sender's email
    :param recipient: recipient's email
    :param subject: subject of message
    :param text: message
    """
    msg: Message = Message(
        subject = subject,
        sender = sender,
        recipients = [recipient],
        html = text
    )
    mail.send(msg)


def send_sms(recipient_num, text):
    """
    Send sms after appointment intent is executed
    :param recipient_num: recipient's phone number
    :param text: sms message
    """
    client.messages.create(
        to = f'+{recipient_num}',
        from_ = twilio_num,
        body = text
    )


def results():
    """
    Get response from appointment intent
    :return: response message
    """
    req = request.get_json(force = True)

    date: datetime = datetime.fromisoformat(req.get('queryResult').get('parameters').get('date'))
    time = datetime.fromisoformat(req.get('queryResult').get('parameters').get('time'))
    day: str = str(date).split(' ')[0]
    time: time = time.time()
    email: str = req.get('queryResult').get('parameters').get('email')
    name: str = req.get('queryResult').get('parameters').get('name')
    recipient_num: int = int(req.get('queryResult').get('parameters').get('number'))

    text: str = f'Hello, {name}. Your appointment is scheduled for {day} at {time}'

    send_email_msg(app.config['MAIL_USERNAME'], email, 'Appointment', text)
    send_sms(recipient_num, text)
    add_lead(name, recipient_num, email, day, time)

    return {'fulfillmentText': f'Your appointment is scheduled for {day} at {time}, {name}.'}


@app.route('/webhook', methods = ['GET', 'POST'])
def webhook():
    return make_response(jsonify(results()))


if __name__ == '__main__':
    app.run()
