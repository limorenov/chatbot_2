#https://hackernoon.com/beginners-guide-simple-chat-bot-fb-based-on-flask-and-heroku-2g7v32ab
import random
from flask import Flask, request
from pymessenger.bot import Bot

#from tensorflow import keras
from keras.models import load_model
from keras.models import model_from_json

app = Flask(__name__)       # Initializing our Flask application
ACCESS_TOKEN = 'EAAJvluWmu6sBALTZAbxio5QqmgoSKvhZCfdGiySm9PY1Ue4s4brgJLI8elYxjNTKLjjDZByaaxuTj4H9YFAX1RHZBZB1CZBwFrzeJx7mH4VZAmC4Becg9RhiJZBsDcnZBjBL1sSZAxru467lu7l9nnZBeZBI7Mk5F7QZCQBVZAwmbqmEByhwZDZD'
VERIFY_TOKEN = 'EAAJvluWmu6sBALTZAbxio5QqmgoSKvhZCfdGiySm9PY1Ue4s4brgJLI8elYxjNTKLjjDZByaaxuTj4H9YFAX1RHZBZB1CZBwFrzeJx7mH4VZAmC4Becg9RhiJZBsDcnZBjBL1sSZAxru467lu7l9nnZBeZBI7Mk5F7QZCQBVZAwmbqmEByhwZDZDAS'
bot = Bot(ACCESS_TOKEN)

#load the model
#model = load_model('training_model.h5')
json_file = open("model.json", 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
model.load_weights('model.h5')

# Importing standard route and two requst types: GET and POST.
# We will receive messages that Facebook sends our bot at this endpoint
@app.route('/', methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        # Before allowing people to message your bot Facebook has implemented a verify token
        # that confirms all requests that your bot receives came from Facebook.
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    # If the request was not GET, it  must be POSTand we can just proceed with sending a message
    # back to user
    else:
            # get whatever message a user sent the bot
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('message'):
                    # Facebook Messenger ID for user so we know where to send response back to
                    recipient_id = message['sender']['id']
                    if message['message'].get('text'):
                        response_sent_text = get_message()
                        send_message(recipient_id, response_sent_text)
                    # if user send us a GIF, photo, video or any other non-text item
                    if message['message'].get('attachments'):
                        response_sent_text = get_message()
                        send_message(recipient_id, response_sent_text)
    return "Message Processed"


def verify_fb_token(token_sent):
    # take token sent by Facebook and verify it matches the verify token you sent
    # if they match, allow the request, else return an error
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


def get_message():
    sample_responses = ["You are stunning!", "We're proud of you",
                        "Keep on being you!", "We're greatful to know you :)"]
    # return selected item to the user
    return random.choice(sample_responses)


# Uses PyMessenger to send response to the user
def send_message(recipient_id, response):
    # sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

# Add description here about this if statement.
if __name__ == "__main__":
    app.run()
