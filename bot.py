import requests
import os
import ConfigParser

from flask import Flask
from flask import request

app = Flask(__name__)

config = ConfigParser.ConfigParser()
config.read("/etc/bot_conf.ini")
page_access_token = config.get('default', 'page_access_token')
validation_token = config.get('default', 'validation_token')

@app.route('/webhook', methods=['GET'])
def web_hook():
    hub_mode = request.args.get('hub.mode')
    verify_token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    if hub_mode == 'subscribe' and verify_token == validation_token:
	return challenge
    return 'Failed validation. Make sure the validation tokens match.', 403


@app.route('/webhook', methods=['POST'])
def web_hook_post():
    for entry in request.get_json()['entry']:
        print(entry)
        for messaging_struct in entry['messaging']:
            if 'message' in messaging_struct:
               message = messaging_struct['message']
               sender = messaging_struct['sender']
                 
               print(message['text'], sender['id'])    
               prefix = 'Simon says'
               requests.post('https://graph.facebook.com/v2.7/me/messages', params={ 'access_token': page_access_token }, json={ 'recipient':{'id': sender['id']}, 'message': { 'text': prefix + ': ' + message['text'] } })
    return 'ok'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
