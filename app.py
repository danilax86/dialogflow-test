from flask import Flask, request, make_response, jsonify
from flask_mail import Mail, Message
from datetime import datetime

import config

app = Flask(__name__)
app.config.from_object(config.Config)
mail = Mail(app)


def send_msg(sender, recipient, subject, text):
    msg = Message(
        subject = subject,
        sender = sender,
        recipients = [recipient],
        html = text
    )
    mail.send(msg)


def results():
    # build a request object
    req = request.get_json(force = True)

    # fetch action from json
    date = datetime.fromisoformat(req.get('queryResult').get('parameters').get('date'))
    time = datetime.fromisoformat(req.get('queryResult').get('parameters').get('time'))
    day = str(date).split(' ')[0]
    time = time.time()
    email = req.get('queryResult').get('parameters').get('email')
    name = req.get('queryResult').get('parameters').get('name')

    # send an email msg
    send_msg(app.config['MAIL_USERNAME'], email, 'Appointment',
             f'<p> Hello, {name}. Your appointment is scheduled for {day} at {time} </p>')

    # return a fulfillment response
    return {'fulfillmentText': 'This is a response from webhook.'}


# create a route for webhook
@app.route('/webhook', methods = ['GET', 'POST'])
def webhook():
    # return response
    return make_response(jsonify(results()))


if __name__ == '__main__':
    app.run()
