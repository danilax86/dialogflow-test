### Instructions

- install all dependencies: \
  `pip install -r requirements.txt`
- run flask server \
  `python app.py`
- run ngrok with the same port as a flask server \
  `ngrok http <port>`

#### Dialogflow:

- setup webhook in Dialogflow \
  URL should be something like `https://<hex>.ngrok.io/webhook`
- enable webhooks for intents in Dialogflow

#### Twilio:

- add URL from previous steps to your Twilio service
- also get your Twilio SID, auth token and phone number

#### amoCRM:

- create an integration
- add URL from previous steps to your integration (without "/webhook")
- get an auth token, integration id and secret key
  (auth token gets refreshed each time you run an application or you are not sending requests while it is alive)