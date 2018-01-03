# from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

def get_sample_events():
    return "sample event yo"

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
   
   
def get_free_food_events1():
    return [['Research Connections', 'Monday, January 8 at 12:00 PM CST', 'Light Hall', 'Learning'], ['Welcome Back Brunch!', 'Monday, January 8 at 11:00 AM CST', 'KC Potter Center', 'Social'], ['GCC Career Talk Series with Mason Ji', 'Tuesday, January 9 at 5:15 PM CST', 'Kissam MPR', 'Group Business'], ['Journal Club: Concussions and CTE (Chronic Traumatic Encephalopathy)', 'Wednesday, January 10 at 5:00 PM CST', 'Light Hall', 'Learning'], ['Literature, Arts, & Medicine: Cultural Series', 'Thursday, January 11 at 12:00 PM CST', 'Light Hall 208', 'Arts & Music'], ['[Wellness] January Social Rounds!', 'Friday, January 12 at 5:00 PM CST', 'Light Hall Student Lounge', 'Social'], ['2018 MLK Weekend of Service', 'Saturday, January 13 at 8:00 AM CST', 'Fisk University', 'Service'], ['APAMSA Mooncake Making Night', 'Saturday, January 13 at 6:00 PM CST', "Kate's Home", 'Cultural'], ['Gabbe Roars Into the New Year', 'Saturday, January 13 at 6:30 PM CST', "Dr. Allos's Home ", 'Social'], ['Health Guardians of America: Fitlifeflow Outreach Event', 'Tuesday, January 16 at 5:30 PM CST', 'Commons Atrium', 'Social'], ['Winning Strategies for the Global Health Case Competition ', 'Wednesday, January 17 at 5:00 PM CST', 'Buttrick Hall 202 ', 'Group Business'], ['TOM:Vanderbilt Makeathon', 'Friday, January 19 at 12:00 PM CST', "The Wond'ry", 'Service'], ['An Evening in Ecuador: MEDLIFE Public Health Fair', 'Thursday, January 25 at 5:00 PM CST', 'Kissam: Warren and More', 'Cultural'], ['GHHS Induction Ceremony', 'Thursday, January 25 at 6:00 PM CST', 'Student Life Center - Board of Trust Room (140)', 'Social'], ['Vandy Cooks - Warm Up with Soups', 'Friday, January 26 at 12:00 PM CST', 'Vanderbilt Recreation & Wellness Center', 'Learning']]

free_food_events = get_free_food_events1()
# print(free_food_events)
print("there are",len(free_food_events), "events")
for index, event in enumerate(free_food_events):
    print("event", index + 1, ":")
    event_info = "{}\nTime: {}\nLocation: {}\nCategory: {}\n".format(
                event[0],event[1],event[2],event[3])
    print(event_info)
                
    # print(info[0])
    # print("Time:", info[1])
    # print("Location:", info[2])
    # print("Category:", info[3])
    # print()