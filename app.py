#Python libraries that we need to import for our bot
import string
import re
from flask import Flask, request
from pymessenger.bot import Bot
from google import google
import os
import random
from random import randint

app = Flask(__name__)
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
bot = Bot(ACCESS_TOKEN)

#We will receive messages that Facebook sends our bot at this endpoint
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook."""
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
       output = request.get_json()
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    response_sent_text = get_message(message['message'].get('text'))
                    send_message(recipient_id, response_sent_text)
                #if user sends us a GIF, photo,video, or any other non-text item
                if message['message'].get('attachments'):
                    response_sent_nontext = get_message(message['message'])
                    send_message(recipient_id, response_sent_nontext)
    return "Message Processed"


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


#chooses message to send to the user
def get_message(msg):
    # write to file here the msg
    try:
        userinput = msg.lower()
        list=[]
        list.append(userinput)
        var chatLog
        for i in list:
            chatLog =chatLog + i
        if re.search("^hi", userinput) or re.search("hello", userinput):
            response = "hello, I am Ephara! I can give you directions and basic information about any topic!"
        elif re.search("^where is", userinput):
            location = re.split("where is ", userinput, 1)
            print(location)
            location = "+".join(location[1].split())
            print(location)
            response = ("Click the link below!\nwww.google.com/maps/search/%s" % location)
        elif re.search("^what is", userinput):
            thing = re.split("what is ", userinput, 1)
            print(thing)
            num_page = 1
            search_results = google.search(thing[1], num_page)
            response = search_results[0].description
        elif re.search("^define", userinput):
            thing = re.split("define ", userinput, 1)
            print(thing)
            num_page = 1
            search_results = google.search(thing[1], num_page)
            response = search_results[0].description
        elif re.search("^bye", userinput) or re.search("^goodbye", userinput):
            response = "Have a Good Day!"
        elif re.search("how(.*)you", userinput) or re.search("how(.*)going", userinput):
            response = "I'm doing quite fine!"
        elif re.search("your creator", userinput) or re.search("your maker", userinput) or re.search("made you", userinput):
            response = "I was made by Reza, Eugene, and Joe!"
        elif re.search("i(.*)good", userinput) or re.search("i(.*)happy", userinput):
            response = "That's great to hear!"
        elif re.search("i(.*)sad", userinput) or re.search("i(.*)don't(.*)good", userinput) or re.search("i(.*)not(.*)good", userinput):
            response = "I'm sorry to hear about that."         
        elif re.search("fuck", userinput) or re.search("shit", userinput) or re.search("bitch", userinput):
            response = "Please be polite to me :("
        elif re.search("give me a random number", userinput):
            random_num = randint(0, 100)
            response = "here is your random number " + str(random_num) + chatLog
        else:
            response = "Sorry, I didn't understand what you said"
            
    except:
        response = "I don't understand that special symbol"
        
    # return selected item to the user
    return (response)

    
#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == "__main__":
    app.run()
