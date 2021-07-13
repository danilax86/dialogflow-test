### Instructions

- install all dependencies: \
  `pip install -r requirements.txt`
- run flask server \
  `python app.py`
- run ngrok with the same port as a flask server \
  `ngrok http <port>`
- setup webhook in Dialogflow \
  URL should be something like `https://<hex>.ngrok.io/webhook`
- enable webhooks for intents in Dialogflow