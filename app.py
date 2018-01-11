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

#global values, to be updated every day
updated = False #to prevent updating twice or more, will be faulty
today = datetime.date(2018, 1, 12)
events_today = []
events_tomorrow = []
events_this_week = []

#hard coded for test run
free_food_events = [['Research Connections', 'Monday, January 8 at 12:00 PM CST', 'Light Hall', 'Learning', '/event/1629631'], ['Welcome Back Brunch!', 'Monday, January 8 at 11:00 AM CST', 'KC Potter Center', 'Social', '/event/1670361'], ['GCC Career Talk Series with Mason Ji', 'Tuesday, January 9 at 5:15 PM CST', 'Kissam MPR', 'Group Business', '/event/1671339'], ['Journal Club: Concussions and CTE (Chronic Traumatic Encephalopathy)', 'Wednesday, January 10 at 5:00 PM CST', 'Light Hall', 'Learning', '/event/1744861'], ['Literature, Arts, & Medicine: Cultural Series', 'Thursday, January 11 at 12:00 PM CST', 'Light Hall 208', 'Arts & Music', '/event/1614211'], ['[Wellness] January Social Rounds!', 'Friday, January 12 at 5:00 PM CST', 'Light Hall Student Lounge', 'Social', '/event/1692579'], ['2018 MLK Weekend of Service', 'Saturday, January 13 at 8:00 AM CST', 'Fisk University', 'Service', '/event/1643195'], ['APAMSA Mooncake Making Night', 'Saturday, January 13 at 6:00 PM CST', "Kate's Home", 'Cultural', '/event/1673020'], ['Gabbe Roars Into the New Year', 'Saturday, January 13 at 6:30 PM CST', "Dr. Allos's Home ", 'Social', '/event/1713544'], ['Health Guardians of America: Fitlifeflow Outreach Event', 'Tuesday, January 16 at 5:30 PM CST', 'Commons Atrium', 'Social', '/event/1671343'], ['Winning Strategies for the Global Health Case Competition ', 'Wednesday, January 17 at 5:00 PM CST', 'Buttrick Hall 202 ', 'Group Business', '/event/1671347'], ['TOM:Vanderbilt Makeathon', 'Friday, January 19 at 12:00 PM CST', "The Wond'ry", 'Service', '/event/1649716'], ['An Evening in Ecuador: MEDLIFE Public Health Fair', 'Thursday, January 25 at 5:00 PM CST', 'Kissam: Warren and More', 'Cultural', '/event/1671360'], ['GHHS Induction Ceremony', 'Thursday, January 25 at 6:00 PM CST', 'Student Life Center - Board of Trust Room (140)', 'Social', '/event/1652304'], ['Vandy Cooks - Warm Up with Soups', 'Friday, January 26 at 12:00 PM CST', 'Vanderbilt Recreation & Wellness Center', 'Learning', '/event/1676927']]


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
    global today
    global updated
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
                    
                    message = messaging_event["message"]
                    payload = ""
                    #if user use quick reply
                    if message.get("quick_reply"):
                        payload = message["quick_reply"]["payload"]
                        # today_info = "Today is " + today.strftime('%m/%d/%Y')
                        if (payload == 'events today'):
                            #send info for events on today
                            if events_today:
                                send_message(sender_id, "events today are:")
                                for event in events_today:
                                    send_event_info_new(sender_id, event)
                                send_message(sender_id, "Note: Some events need RSVP, please check their details")
                            else:
                                send_message(sender_id, "The good news is the best things in life are free. The bad news is they're not available today. I'll make it up to you another time.")                                                     
                        elif (payload == 'events tomorrow'):
                            if events_tomorrow:
                                #send info for events on tomorrow
                                send_message(sender_id, "events tomorrow are:")
                                for event in events_tomorrow:
                                    send_event_info_new(sender_id, event)
                                send_message(sender_id, "Note: Some events need RSVP, please check their details")
                                
                            else:
                                send_message(sender_id, "The good news is the best things in life are free. The bad news is they're not available tomorrow. I'll make it up to you another time.")                   
                        elif (payload == 'events this week'):
                            if events_this_week:
                                send_message(sender_id, "events this week are:")
                                send_message(sender_id, "Note: Some events need RSVP, please check their details")                             
                            else:
                                # user_name = get_user_name(recipient_id)
                                send_message(sender_id, "The good news is the best things in life are free. The bad news is they're not available this week. I'll make it up to you another time")                            
                    else:
                        if message_text == 'update' and not updated:#update information when we tell it to
                            update_all_events_info(today)#simulate fetching data for today
                            #actually done only once per day
                            send_message(sender_id, "updated")
                        else:
                            send_message(sender_id, "I'm sorry I can't do much beyond letting you know where to find free food")
                    
                    #after getting user's preference, keep asking again`
                    send_quick_reply_message(sender_id, "When are you down to have some free food?")
                    
                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    payload = messaging_event['postback']['payload']
                    sender_id = messaging_event["sender"]["id"]
                    if (payload == 'first message sent'):
                        send_quick_reply_message(sender_id, "Hi there! Let's cut to the chase. When are you down to have some free food?")
                    elif (payload == 'events today'):
                        #send info for events on today
                        if events_today:
                            send_message(sender_id, "events today are:")
                            for event in events_today:
                                send_event_info_new(sender_id, event)
                        else:
                            send_message(sender_id, "The good news is the best things in life are free. The bad news is they're not available today. I'll make it up to you another time.")                            
                    elif (payload == 'events tomorrow'):
                        #send info for events on tomorrow
                        if events_tomorrow:
                            send_message(sender_id, "events tomorrow are:")
                            for event in events_tomorrow:
                                send_event_info_new(sender_id, event)
                        else:
                            send_message(sender_id, "The good news is the best things in life are free. The bad news is they're not available tomorrow. I'll make it up to you another time.")                            
                    elif (payload == 'events this week'):
                        if events_this_week:
                            send_message(sender_id, "events this week are:")
                        else:
                            send_message(sender_id, "The good news is the best things in life are free. The bad news is they're not available this week. I'll make it up to you another time.")                            
    return "ok", 200

def send_event_info(sender_id, event):
    #give time in 12 hr format
    event_info = "{}\nTime: {}\nLocation: {}\n".format(
                    event[0],event[1].strftime("%I:%M %p"),event[2])
    send_message(sender_id, event_info)


def get_events_on_date(events, date):
    events_on_date = []
    for event in events:
        if event[1].day == (date).day:
            events_on_date.append(event)
    return events_on_date


# datetime given from data does not specify the year, need to add the correct year
def convert_to_datetime(event_time):
    given_datetime = datetime.datetime.strptime(event_time,'%A, %B %d at %I:%M %p CST')
    correct_datetime = given_datetime.replace(year=datetime.datetime.now().year)
    return correct_datetime

# get_free_food_events
#this is called at the start of everyday, to update the info
#to be given out to users
#e.g what free food events for today are, for tomorrow are, for this week are
def update_all_events_info(today):
    global events_today
    global events_tomorrow
    global free_food_events

    #convert datetime text to datetime objects
    for event in free_food_events:
        event[1] = convert_to_datetime(event[1])
    
    #update events_today to contain events today
    events_today = get_events_on_date(free_food_events, today)
    tomorrow = today + datetime.timedelta(days=1)
    events_tomorrow = get_events_on_date(free_food_events, tomorrow)

def send_event_info_new(recipient_id, event):
    event_info = "{}\nTime: {}\nLocation: {}\n".format(
                    event[0],event[1].strftime("%I:%M %p"),event[2])

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
                    "text":event_info,
                    "buttons":[
                        {
                            "type":"web_url",
                            "url":"https://anchorlink.vanderbilt.edu"+event[4],
                            "title":"Details",
                            "webview_height_ratio": "compact",
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


#can't get this to work, key error always
def get_user_name(recipient_id):
    log("getting user's name")
    
    
    command = "https://graph.facebook.com/v2.6/<"+recipient_id+">?fields=first_name,last_name,profile_pic&access_token=EAACNsF2oEyABAEpRsZBkjELZCRUUuTZAJVRodGwM7OZCjgPquG4Bc8svqZBBdntgBxRmlIIsGM6dc3SzVo7NRG3pDU8HZB7ZAfZAUzJ01rZCHjXNQL3TaS8thGtrQMaT3axvj7kFaPflRcSkUtMV8gyHkLxhgHdk7I7EDOgtJZBPyUxjqno4yhbkH1"

    data = requests.get(command) #.json() #need to convert Response object returned into json
    log(data.content)
    return data.json()["first_name"]

    # curl -X GET "https://graph.facebook.com/v2.6/<PSID>?fields=first_name,last_name,profile_pic&access_token=<PAGE_ACCESS_TOKEN>"


def send_quick_reply_message(recipient_id, message_text):
    
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
            "text":message_text,
            "quick_replies":[
                {
                    "content_type":"text",
                    "title":"Today",
                    "payload":"events today"
                },
                {
                    "content_type":"text",
                    "title":"Tomorrow",
                    "payload":"events tomorrow"
                },
                {
                    "content_type":"text",
                    "title":"This week",
                    "payload":"events this week"
                }
            ]
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
