import os
import sys
import json
# from datetime import datetime
import datetime

# from getdata import get_free_food_events
# from misc import misc_function

import requests
from flask import Flask, request


app = Flask(__name__)


@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events

    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = messaging_event["message"]["text"]  # the message's text
                    
                    if (message_text == "buttons"):
                        send_button_message(sender_id)
                    else:
                        #make up a day
                        today = datetime.date(2018, 1, 12)
                        # today = datetime.datetime.now()
                        today_info = "Assume today is " + today.strftime('%m/%d/%Y')
                        send_message(sender_id, today_info)
                        send_message(sender_id, "free-food events tomorrow are")
                                            
                        events_tomorrow = get_events_tomorrow(get_free_food_events(), today)
                        if events_tomorrow:
                            for event in events_tomorrow:#add indentation here
                                event_info = "{}\nTime: {}\nLocation: {}\nCategory: {}\n".format(event[0],event[1],event[2],event[3])
                                send_message(sender_id, event_info)
                        else:
                            send_message(sender_id, "there are no events tomorrow")

                    #make up some date to test bot
                    # today = datetime.date(2018, 1, 12)
                    # free_food_events_tomorrow = get_events_tomorrow(get_free_food_events(), today)
                    # for event in free_food_events_tomorrow:
                    #     event_info = "{}\nTime: {}\nLocation: {}\nCategory: {}\n".format(
                    #                 event[0],event[1],event[2],event[3])
                    #     send_message(sender_id, event_info)
                    
                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    if (messaging_event['postback']['payload'] == 'first message sent'):
                        sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                        send_message(sender_id, "Hi there! I'll tell you when the free food events are on campus.")                        

    return "ok", 200


def get_events_tomorrow(events, today):
    events_tomorrow = []
    for event in events:
        #this can be improved
        if event[1].day == (today + datetime.timedelta(days=1)).day:
            events_tomorrow.append(event)
    return events_tomorrow


# datetime given from data does not specify the year, need to add the correct year
def convert_to_datetime(event_time):
    given_datetime = datetime.datetime.strptime(event_time,'%A, %B %d at %I:%M %p CST')
    correct_datetime = given_datetime.replace(year=datetime.datetime.now().year)
    return correct_datetime

def get_free_food_events():
    free_food_events = [['Research Connections', 'Monday, January 8 at 12:00 PM CST', 'Light Hall', 'Learning'], ['Welcome Back Brunch!', 'Monday, January 8 at 11:00 AM CST', 'KC Potter Center', 'Social'], ['GCC Career Talk Series with Mason Ji', 'Tuesday, January 9 at 5:15 PM CST', 'Kissam MPR', 'Group Business'], ['Journal Club: Concussions and CTE (Chronic Traumatic Encephalopathy)', 'Wednesday, January 10 at 5:00 PM CST', 'Light Hall', 'Learning'], ['Literature, Arts, & Medicine: Cultural Series', 'Thursday, January 11 at 12:00 PM CST', 'Light Hall 208', 'Arts & Music'], ['[Wellness] January Social Rounds!', 'Friday, January 12 at 5:00 PM CST', 'Light Hall Student Lounge', 'Social'], ['2018 MLK Weekend of Service', 'Saturday, January 13 at 8:00 AM CST', 'Fisk University', 'Service'], ['APAMSA Mooncake Making Night', 'Saturday, January 13 at 6:00 PM CST', "Kate's Home", 'Cultural'], ['Gabbe Roars Into the New Year', 'Saturday, January 13 at 6:30 PM CST', "Dr. Allos's Home ", 'Social'], ['Health Guardians of America: Fitlifeflow Outreach Event', 'Tuesday, January 16 at 5:30 PM CST', 'Commons Atrium', 'Social'], ['Winning Strategies for the Global Health Case Competition ', 'Wednesday, January 17 at 5:00 PM CST', 'Buttrick Hall 202 ', 'Group Business'], ['TOM:Vanderbilt Makeathon', 'Friday, January 19 at 12:00 PM CST', "The Wond'ry", 'Service'], ['An Evening in Ecuador: MEDLIFE Public Health Fair', 'Thursday, January 25 at 5:00 PM CST', 'Kissam: Warren and More', 'Cultural'], ['GHHS Induction Ceremony', 'Thursday, January 25 at 6:00 PM CST', 'Student Life Center - Board of Trust Room (140)', 'Social'], ['Vandy Cooks - Warm Up with Soups', 'Friday, January 26 at 12:00 PM CST', 'Vanderbilt Recreation & Wellness Center', 'Learning']]

    for event in free_food_events:
        event[1] = convert_to_datetime(event[1])
    return free_food_events
    
#raw message is a json
# button_message = '{
#     "recipient"
#     "buttons":[
#     {
#         "type":"postback",
#         "title":"Bookmark Item",
#         "payload":"DEVELOPER_DEFINED_PAYLOAD"
#     }
#     ]
# }'

def send_button_message(recipient_id):
    
    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text="button message"))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    # data = json.dumps(raw_message)
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment":{
                "type":"template",
                "payload":{
                    "template_type":"button",
                    "text":"What do you want?",
                    "buttons":[
                        {
                            "type":"web_url",
                            "url":"google.com",
                            "title":"show website"
                        },
                        {
                            "type":"postback",
                            "title":"Start chatting",
                            "payload":"someshit to modify"
                        }
                    ]
                }
            }
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def send_message(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def log(msg, *args, **kwargs):  # simple wrapper for logging to stdout on heroku
    try:
        if type(msg) is dict:
            msg = json.dumps(msg)
        else:
            msg = unicode(msg).format(*args, **kwargs)
        print u"{}: {}".format(datetime.datetime.now(), msg)
    except UnicodeEncodeError:
        pass  # squash logging errors in case of non-ascii text
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
