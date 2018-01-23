from dotenv import load_dotenv, find_dotenv
import os
import sys
import json
from datetime import datetime
import requests
from flask import Flask, request
import pprint

load_dotenv(find_dotenv())

PAGE_ACCESS_TOKEN = os.environ.get('PAGE_ACCESS_TOKEN')
VERIFY_TOKEN = os.environ.get('VERIFY_TOKEN')

app = Flask(__name__)


'''
When the endpoint is registered as a webhook, it must echo back
the 'hub.challenge' value it receives in the query arguments
'''


@app.route('/', methods=['GET'])
def verify():
    # Parse the query params
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = requests.args.get('hub.challenge')

    if mode and token:
        # Checks the mode and token sent is correct
        if mode == 'subscribe' and token == VERIFY_TOKEN:
            # Responds with the challenge token from the request
            print('WEBHOOK_VERIFIED')
            return challenge, 200
        # Responds with '403 Forbidden' if verify tokens do not match
        return 'Verification token mismatch', 403

    # If the API is pinged from a browser
    return 'Welcome to Stock Guru!', 200


def callSendAPI(sender_psid, response):
    # Construct the message body
    request_body = {'recipient': {'id': sender_psid}, 'message': response}

    # Send the HTTP request to the Messenger Platform
    # r = requests.post('https://graph.facebook.com/v2.6/me/messages', data={
    #     'access_token': PAGE_ACCESS_TOKEN
    # }, json=request_body)
    API_URL = f'https://graph.facebook.com/v2.6/me/messages?access_token={PAGE_ACCESS_TOKEN}'
    r = requests.post(API_URL, json=request_body)

    if r.status_code != requests.codes.ok:
        print(f'The POST request encountered an error: {r.text} ({r.status_code})')


def handleMessage(sender_psid, received_message):
    response = {}
    # Check if the message contains text
    # if received_message['text']:
    if 'text' in received_message:
        # Create the payload for a basic text message
        response['text'] = f'You sent the message: "{received_message["text"]}". Now send me an image!'
    else:
        print('Error: Invalid message type!')

    # Sends the response message
    callSendAPI(sender_psid, response)


@app.route('/', methods=['POST'])
def webhook():
    # Parse the request body from the POST
    body = request.get_json()
    print(body)

    # Check the webhook event is from a Page subscription
    if body['object'] == 'page':
        # Iterate over each entry - there may be multiple if batched
        for entry in body['entry']:
            for webhook_event in entry['messaging']:
                # Get the sender PSID
                sender_psid = webhook_event['sender']['id']
                print(f'Sender PSID: {sender_psid}')

                # Check if the event is a message or postback and
                # pass the event to the appropriate handler function
                if webhook_event['message']:
                    handleMessage(sender_psid, webhook_event['message'])

        # Return a '200 OK' response to all events
        return 'EVENT_RECEIVED', 200
    else:
        # Return a '404 Not Found' if event is not from a page subscription
        return '', 404


# @app.route('/', methods=['POST'])
# def webhook():

#     # endpoint for processing incoming messaging events

#     data = request.get_json()
#     log(data)  # you may not want to log every incoming message in production, but it's good for testing

#     if data["object"] == "page":

#         for entry in data["entry"]:
#             for messaging_event in entry["messaging"]:

#                 if messaging_event.get("message"):  # someone sent us a message

#                     sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
#                     recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
#                     message_text = messaging_event["message"]["text"]  # the message's text

#                     send_message(sender_id, "roger that!")

#                 if messaging_event.get("delivery"):  # delivery confirmation
#                     pass

#                 if messaging_event.get("optin"):  # optin confirmation
#                     pass

#                 if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
#                     pass

#     return "ok", 200


# def send_message(recipient_id, message_text):

#     log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

#     params = {
#         "access_token": os.environ["PAGE_ACCESS_TOKEN"]
#     }
#     headers = {
#         "Content-Type": "application/json"
#     }
#     data = json.dumps({
#         "recipient": {
#             "id": recipient_id
#         },
#         "message": {
#             "text": message_text
#         }
#     })
#     r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
#     if r.status_code != 200:
#         log(r.status_code)
#         log(r.text)


# def log(msg, *args, **kwargs):  # simple wrapper for logging to stdout on heroku
#     try:
#         if type(msg) is dict:
#             msg = json.dumps(msg)
#         else:
#             msg = str(msg).format(*args, **kwargs)
#         print(u'{}: {}'.format(datetime.now(), msg))
#     except UnicodeEncodeError:
#         pass  # squash logging errors in case of non-ascii text
#     sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
