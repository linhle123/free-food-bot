# from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import os
import datetime
import pickle

#global var
today = datetime.date.today()


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
        try:
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//label[contains(text(), 'Free Food')]")))
        finally:
            #click to filter for free food
            driver.find_element_by_xpath("//label[contains(text(), 'Free Food')]").click()
            time.sleep(3) #wait for free food filter to take effect, this is stupid solution tho
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
    
    eventDetails = []
    #can somehow use list comprehension to filter for eventDetail?
    for event in eventList:
        temp = event.findAll(string=True)
        temp.append(event['href'])
        eventDetails.append(temp)
    
    return eventDetails



# datetime given from data does not specify the year, need to add the correct year
def convert_to_datetime(event_time):
    given_datetime = datetime.datetime.strptime(event_time,'%A, %B %d at %I:%M %p CST')
    correct_datetime = given_datetime.replace(year=datetime.datetime.now().year)
    return correct_datetime


def print_events_info():
    free_food_events = get_free_food_events()
    # convert time of event to datetime object
    for event in free_food_events:
        event[1] = convert_to_datetime(event[1])
    for event in free_food_events:
        event_info = "{}\nTime: {}\nLocation: {}\n".format(
            event[0],event[1].strftime("%I:%M %p"),event[2])
        print(event_info)


def get_events_on_date(events, date):
    events_on_date = []
    for event in events:
        if event[1].day == (date).day:
            events_on_date.append(event)
    return events_on_date

#get events in this week
def get_events_in_week(events):
    start = today - datetime.timedelta(days=today.weekday())
    end = start + datetime.timedelta(days=6)
    events_in_week = []
    for event in events:
        if start <= event[1].date() <= end:
            events_in_week.append(event)
    return events_in_week
    

#update the events of today and tomorrow
def update_events_info():
    global today
    today = datetime.date.today()
    print("update event info")
    free_food_events = get_free_food_events()
    #convert datetime text to datetime objects
    #convert navigable string of bs4 to str, else it breaks shelve module
    for event in free_food_events:
        event[1] = convert_to_datetime(event[1])
        event[0] = str(event[0].encode('utf-8'))
        event[2] = str(event[2].encode('utf-8'))
        event[3] = str(event[3].encode('utf-8'))
    
    #update events_today to contain events today
    #variables are in app.py
    events_today = get_events_on_date(free_food_events, today)
    f_today = open( "events_today.pkl", "wb" )
    pickle.dump(events_today, f_today,protocol=2)#save to file
    f_today.close()
    print("#events today", len(events_today))

    tomorrow = today + datetime.timedelta(days=1)
    f_tmr = open( "events_tomorrow.pkl", "wb" )
    events_tomorrow = get_events_on_date(free_food_events, tomorrow)
    pickle.dump(events_tomorrow, f_tmr, protocol=2)#save to file
    f_tmr.close()
    print("#events tmr", len(events_tomorrow))   

    f_week = open( "events_this_week.pkl", "wb" )
    events_this_week = get_events_in_week(free_food_events)
    pickle.dump(events_this_week, f_week, protocol=2)#save to file
    f_week.close()    
    print("#events this week", len(events_this_week))

# update_events_info()
