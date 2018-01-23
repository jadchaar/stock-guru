from dotenv import load_dotenv, find_dotenv
import os
import requests
from flask import Flask, request

from functionality.stock_time_series import retrieve_current_key_statistics
from functionality.helpers import utils

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


def getKeyStats(ticker):
        # Get Key Stats
        keyStats = retrieve_current_key_statistics.getKeyStatistics(ticker)
        payload = f'''
        {keyStats["companyName"]} ({keyStats["symbol"]}) as of {keyStats["lastUpdated"]}
        * Latest Price: {keyStats["latestPrice"]}
        * Previous Close: {keyStats["previousClose"]}
        * Open: {keyStats["open"]}
        * Day\'s Range: {keyStats["dayRange"]}
        * 52 Week Range: {keyStats["week52Range"]}
        * Market Cap: {keyStats["marketCap"]}
        * Volume: {keyStats["latestVolume"]}
        * Avg Volume: {keyStats["avgTotalVolume"]}
        * P/E Ratio: {keyStats["peRatio"]}
        * EPS: {keyStats["eps"]}
        * Beta: {keyStats["beta"]}
        '''
        if 'dividend' in keyStats:
            payload += f'''
            \n* Dividend: {keyStats["dividend"]}
            * Ex-Dividend Date: {keyStats["exDividendDate"]}
            '''


def handleMessage(sender_psid, received_message):
    response = {}
    # Check if the message contains text
    # if received_message['text']:
    if 'text' in received_message:
        # Create the payload for a basic text message
        # response['text'] = f'You sent the message: "{received_message["text"]}". Now send me an image!'
        response['text'] = getKeyStats(received_message)
    else:
        errorMsg = 'Error: Invalid message type!'
        response['text'] = errorMsg
        print(errorMsg)

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
                if 'message' in webhook_event:
                    handleMessage(sender_psid, webhook_event['message'])

        # Return a '200 OK' response to all events
        return 'EVENT_RECEIVED', 200
    else:
        # Return a '404 Not Found' if event is not from a page subscription
        return '', 404


if __name__ == '__main__':
    app.run(debug=True)
