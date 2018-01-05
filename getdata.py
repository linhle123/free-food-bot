# from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

import datetime


#return the anchorlink html page with free food event filter applied
def get_free_food_events_page():
    #this line is for heroku deployment, can also use this if added phantomjs file to executable_path
    #i.e. use "export PATH=$PATH:/home/linhle/phantomjs-2.1.1-linux-x86_64/bin/phantomjs"
    driver = webdriver.PhantomJS()
    
    #try chrome headless
    # options = webdriver.ChromeOptions()
    # options.set_headless(True)
    # options.binary_location'/usr/bin/chromedriver')
    # options.add_argument('headless')
    # options.add_argument('start-maximized')
    
    # options.add_argument('window-size=1200x800')
    # driver = webdriver.Chrome(chrome_options=options)
    # driver = webdriver.Chrome()   this is for head-ful option, just 1 line 

    #below line is for local use, phantomjs    
    # driver = webdriver.PhantomJS(executable_path='/home/linhle/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')

    #below line is for local use, chrome    
    # driver = webdriver.Chrome(executable_path='/home/linhle/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')

    # set browser size to be big, otherwise some elements get hidden by responsive design
    driver.set_window_size(1124, 850) 
    driver.get("https://anchorlink.vanderbilt.edu/events")
    try:
        #wait until we can select perks of events
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Open Perks List']")))
    finally:
        #click to open the perks option
        driver.find_element_by_xpath("//button[@aria-label='Open Perks List']").click()
        try:
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//label[contains(text(), 'Free Food')]")))
        finally:
            #click to filter for free food
            driver.find_element_by_xpath("//label[contains(text(), 'Free Food')]").click()
            time.sleep(3) #wait for free food filter to take effect, this is stupid solution tho
            return driver.page_source
            # print(driver.find_element_by_id("event-discovery-list"))
            # return driver.find_element_by_id("event-discovery-list").text
            driver.close()


#return array of array containing details of free food events in each element
def get_free_food_events():
    #contains html of page as seen in browser
    bsObj = BeautifulSoup(get_free_food_events_page(), "html.parser")

    #contains html of the list of free food events
    # events are the "a"" tags with href like this: href="/event/1629631"
    eventList = bsObj.findAll("a", {"href":re.compile("\/event\/")})

    #within the html of each event, find tags with string contents
    # eventDetails is an array of arrays, each element contains info for an event 
    eventDetails = [event.findAll(string=True) for event in eventList]
    
    return eventDetails
   

def get_free_food_events_hard_coded():
    return [['Research Connections', 'Monday, January 8 at 12:00 PM CST', 'Light Hall', 'Learning'], ['Welcome Back Brunch!', 'Monday, January 8 at 11:00 AM CST', 'KC Potter Center', 'Social'], ['GCC Career Talk Series with Mason Ji', 'Tuesday, January 9 at 5:15 PM CST', 'Kissam MPR', 'Group Business'], ['Journal Club: Concussions and CTE (Chronic Traumatic Encephalopathy)', 'Wednesday, January 10 at 5:00 PM CST', 'Light Hall', 'Learning'], ['Literature, Arts, & Medicine: Cultural Series', 'Thursday, January 11 at 12:00 PM CST', 'Light Hall 208', 'Arts & Music'], ['[Wellness] January Social Rounds!', 'Friday, January 12 at 5:00 PM CST', 'Light Hall Student Lounge', 'Social'], ['2018 MLK Weekend of Service', 'Saturday, January 13 at 8:00 AM CST', 'Fisk University', 'Service'], ['APAMSA Mooncake Making Night', 'Saturday, January 13 at 6:00 PM CST', "Kate's Home", 'Cultural'], ['Gabbe Roars Into the New Year', 'Saturday, January 13 at 6:30 PM CST', "Dr. Allos's Home ", 'Social'], ['Health Guardians of America: Fitlifeflow Outreach Event', 'Tuesday, January 16 at 5:30 PM CST', 'Commons Atrium', 'Social'], ['Winning Strategies for the Global Health Case Competition ', 'Wednesday, January 17 at 5:00 PM CST', 'Buttrick Hall 202 ', 'Group Business'], ['TOM:Vanderbilt Makeathon', 'Friday, January 19 at 12:00 PM CST', "The Wond'ry", 'Service'], ['An Evening in Ecuador: MEDLIFE Public Health Fair', 'Thursday, January 25 at 5:00 PM CST', 'Kissam: Warren and More', 'Cultural'], ['GHHS Induction Ceremony', 'Thursday, January 25 at 6:00 PM CST', 'Student Life Center - Board of Trust Room (140)', 'Social'], ['Vandy Cooks - Warm Up with Soups', 'Friday, January 26 at 12:00 PM CST', 'Vanderbilt Recreation & Wellness Center', 'Learning']]


# datetime given from data does not specify the year, need to add the correct year
def convert_to_datetime(event_time):
    given_datetime = datetime.datetime.strptime(event_time,'%A, %B %d at %I:%M %p CST')
    correct_datetime = given_datetime.replace(year=datetime.datetime.now().year)
    return correct_datetime

#use list comprehension here instead    
def get_events_tomorrow(events, today):
    events_tomorrow = []
    for event in events:
        #this can be improved
        if event[1].day == (today + datetime.timedelta(days=1)).day:
            events_tomorrow.append(event)
    return events_tomorrow

free_food_events = get_free_food_events_hard_coded()
myevent = free_food_events[3]

#convert time of event to datetime object
for event in free_food_events:
    event[1] = convert_to_datetime(event[1])

# today = datetime.time(1,2,3)
today = datetime.date(2018, 1, 12)
tempday = datetime.datetime.now()
today_info = "today is " + tempday.strftime('%m/%d/%Y')
print(today_info)
events_tomorrow = get_events_tomorrow(free_food_events, today)


if events_tomorrow:
    for event in events_tomorrow:
        #notice we print time in 12hr format
        event_info = "{}\nTime: {}\nLocation: {}\n".format(
                    event[0],event[1].strftime("%I:%M %p"),event[2])
        print(event_info)
else:
    print("there are no events tomorrow")
      


# curl -X POST -H "Content-Type: application/json" -d '{
#   "greeting":[
#     {
#       "locale":"default",
#       "text":"Hello {{user_first_name}}! Free lunch is actually a thing, let me show you."
#     }
#   ]
# }' "https://graph.facebook.com/v2.6/me/messenger_profile?access_token=EAACNsF2oEyABAEpRsZBkjELZCRUUuTZAJVRodGwM7OZCjgPquG4Bc8svqZBBdntgBxRmlIIsGM6dc3SzVo7NRG3pDU8HZB7ZAfZAUzJ01rZCHjXNQL3TaS8thGtrQMaT3axvj7kFaPflRcSkUtMV8gyHkLxhgHdk7I7EDOgtJZBPyUxjqno4yhbkH1"


# {  
#    "object":"page",
#    "entry":[  
#       {  
#          "time":1515132086414,
#          "id":"2024616067827339",
#          "messaging":[  
#             {  
#                "recipient":{  
#                   "id":"2024616067827339"
#                },
#                "timestamp":1515132086414,
#                "sender":{  
#                   "id":"1387570081371818"
#                },
#                "postback":{  
#                   "payload":"first message sent",
#                   "title":"Get Started"
#                }
#             }
#          ]
#       }
#    ]
# }