from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import datetime
import cPickle as pickle
import os
# import urlparse
# import psycopg2

# urlparse.uses_netloc.append("postgres")
# url = urlparse.urlparse(os.environ["DATABASE_URL"])
# conn = psycopg2.connect(
#     database=url.path[1:],
#     user=url.username,
#     password=url.password,
#     host=url.hostname,
#     port=url.port
# )
# cur = conn.cursor()

#global var
today = datetime.date.today()
#how many days ahead we wanna get events
days_ahead = 3

#return the anchorlink html page with free food event filter applied
def get_free_food_events_page():
    #this line is for heroku deployment, can also use this if added phantomjs file to executable_path
    # driver = webdriver.Chrome(executable_path='/home/linhle/Desktop/chromedriver')
    # below is for use in heroku
    # https://github.com/heroku/heroku-buildpack-google-chrome/issues/26
    chrome_bin = os.environ.get('GOOGLE_CHROME_SHIM', None)
    opts = ChromeOptions()
    opts.binary_location = chrome_bin
    driver = webdriver.Chrome(executable_path="chromedriver", chrome_options=opts)

    # set browser size to be big, otherwise some elements get hidden by responsive design
    driver.set_window_size(1124, 850) 
    driver.get("https://anchorlink.vanderbilt.edu/events")
    try:
        #wait until we can select perks of events
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Open Perks List']")))
    finally:
        #click to open the perks option
        driver.find_element_by_xpath("//button[@aria-label='Open Perks List']").click()
    try: #wait until perks menu opens
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//label[contains(text(), 'Free Food')]")))
    finally:
        #click to filter for free food
        driver.find_element_by_xpath("//label[contains(text(), 'Free Food')]").click()
        time.sleep(1.5) #wait for free food filter to take effect, this is stupid solution tho
    try:    #load more events on page
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Load More')]")))
    finally:
        driver.find_element_by_xpath("//span[contains(text(), 'Load More')]").click()
        time.sleep(1) #wait to load more, this is stupid solution tho        
        html = driver.page_source
        driver.close()
        return html


#return array of array containing details of free food events in each element
def get_free_food_events():
    #contains html of page as seen in browser
    bsObj = BeautifulSoup(get_free_food_events_page(), "html.parser")

    #contains html of the list of free food events
    # events are the "a"" tags with href like this: href="/event/1629631"
    eventList = bsObj.findAll("a", {"href":re.compile("\/event\/")})
    #within the html of each event, find tags with string contents
    # eventDetails is an array of arrays, each element contains info for an event 
    free_food_events = []
    #each event is a bunch of html
    #info we care about are the strings, so find all of those
    #also we care about the link to event on anchorlink, so add the href attribute
    for event in eventList:
        event_info = event.findAll(string=True)
        event_info.append(event['href'])
        free_food_events.append(event_info)
    
    #all details of each event are navigable strings
    #convert them to strings, event[1] should be datetime (for timing)
    #encode to get bytestring,then decode to get unicode string
    for event in free_food_events:
        event[0] = (event[0].encode('utf-8')).decode('utf-8')
        event[1] = convert_to_datetime(event[1])
        event[2] = (event[2].encode('utf-8')).decode('utf-8')
        event[3] = (event[3].encode('utf-8')).decode('utf-8')   
        # event[4] is alr a str   
    return free_food_events



# datetime given from data does not specify the year, need to add the correct year
def convert_to_datetime(event_time):
    given_datetime = datetime.datetime.strptime(event_time,'%A, %B %d at %I:%M %p CST')
    correct_datetime = given_datetime.replace(year=datetime.datetime.now().year)
    return correct_datetime

#pretty print info for each event in parameter
#for testing purposes
def print_events_info(events):
    for event in events:
        event_info = "{}\nTime: {}\nLocation: {}\n".format(
            event[0].encode('utf-8'),event[1].strftime("%I:%M %p"),event[2].encode('utf-8'))
        print(event_info)
    

#filter out events which are on the date provided as parameter
#event[1] must be datetime object
def get_events_on_date(events, date):
    return [event for event in events if event[1].day == (date).day]


#get events from today until days_ahead later
#e.g. days_ahead = 1, then it's today and tmr
#event[1] must be datetime object
def get_events_next_n_days(events):
    start = datetime.date.today()
    end = start + datetime.timedelta(days=days_ahead)
    return [event for event in events if start <= event[1].date() <= end]


#update the events of today and tomorrow
def update_events_info():
    print("daily update of event info")
    #update global variable "today"
    global today
    today = datetime.date.today()
    free_food_events = get_free_food_events()
    print("scraped data done")
    #update events_today to contain events today
    #variables are in app.py

    events_today = get_events_on_date(free_food_events, today)
    
    with open( "events_today.pkl", "wb" ) as f_today:
        print("write events today to file")
        pickle.dump(events_today, f_today,protocol=2)#save to file
    
    tomorrow = today + datetime.timedelta(days=1)
    events_tomorrow = get_events_on_date(free_food_events, tomorrow)
    with open( "events_tomorrow.pkl", "wb" ) as f_tmr:
        print("write events tmr to file")        
        pickle.dump(events_tomorrow, f_tmr, protocol=2)#save to file

    events_further_ahead = get_events_next_n_days(free_food_events)
    with open( "events_further_ahead.pkl", "wb" ) as f_further:
        print("write events further ahead to file")        
        pickle.dump(events_further_ahead, f_further, protocol=2)#save to file
    
    print("info scraped:")
    print("#events tmr", len(events_tomorrow))   
    print("#events today", len(events_today))
    print("#events {} days ahead".format(days_ahead), len(events_further_ahead))


#do not call any functions here when push, only for debugging:
# free_food_events = get_free_food_events()
# print(free_food_events)
# print_events_info(free_food_events)
# events_further_ahead = get_events_next_n_days(free_food_events)
# print_events_info(events_further_ahead)

#before pushing, execute below, then comment it out, then push to heroku
update_events_info()
