# from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

from selenium.common.exceptions import NoSuchElementException        

import datetime
import requests

def check_exists_by_xpath(driver, xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


#return the anchorlink html page with free food event filter applied
def get_member_list_page():
    #this line is for heroku deployment, can also use this if added phantomjs file to executable_path
    #i.e. use "export PATH=$PATH:/home/linhle/phantomjs-2.1.1-linux-x86_64/bin/phantomjs"
    # driver = webdriver.PhantomJS()
    
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
    driver = webdriver.Chrome(executable_path='/home/linhle/chromedriver')

    # set browser size to be big, otherwise some elements get hidden by responsive design
    driver.set_window_size(1124, 850) 
    driver.get("https://anchorlink.vanderbilt.edu/organization/branscombquad/roster")

    # params = {'pf.username': 'honglil', 'pf.pass':'Fucking1!'}
    # r = requests.post("https://sso.vanderbilt.edu/idp/sd1SF/resumeSAML20/idp/SSO.ping", data=params)
    # print(r.text)
    print("waiting for sign in")
    try:
        #wait until we can select perks of events
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Sign In')]")))
    finally:
        #click to open the perks option
        driver.find_element_by_xpath("//span[contains(text(), 'Sign In')]").click()
        try:
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "username")))
            #"waiting for form to appear"
        finally:
            #fill in username and password
            driver.find_element_by_id("username").send_keys("honglil")
            driver.find_element_by_id("password").send_keys("Fucking1!")
            print("gonna click sign on")
            driver.find_element_by_link_text("Sign On").click()
            print("clicked")            
            try:
                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "roster-members")))
            finally:
                #click load more members to show all members
                # load_more = driver.find_element_by_xpath("//span[contains(text(), 'Load More Members')]")
                # while check_exists_by_xpath(driver,"//span[contains(text(), 'Load More Members')]"):
                #     driver.find_element_by_xpath("//span[contains(text(), 'Load More Members')]").click()
                #     print("load more")
                #     time.sleep(1)
                
                print("should list all members now")
                # time.sleep(3)

                #find the div with id = roster-members, then go 1 div into that
                #then get all the divs at this level, those are the people we need
                members = driver.find_elements_by_xpath("//div[@id='roster-members']/div/div")
                output_file = open('branscomb_emails.txt','w')
                print("# emails to collect:", len(members))
                for element in members:
                    element.click() #click on the member
                    try:
                        print("waiting for pop up")
                        #wait for member's email to pop up
                        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,  "//a[contains(@href,'mailto')]")))
                    # except Exception,e:
                    #     driver.save_screenshot('screenshot.png')
                    finally:
                        email = driver.find_element_by_xpath("//a[contains(@href,'mailto')]").text
                        print(email)
                        print(email, file=output_file)
                        
                        #press esc to quit the pop up that shows the email
                        ActionChains(driver).send_keys(Keys.ESCAPE).perform()
                        time.sleep(1)
                    # print(element.text)

                # bsObj = BeautifulSoup(members.page_source, "html.parser")
                # print(bsObj.children)
                # print(members)
                # print("len of members", len(members.get(0)))

            #click to filter for free food
            # driver.find_element_by_xpath("//label[contains(text(), 'Free Food')]").click()
            # return driver.page_source
            # print(driver.find_element_by_id("event-discovery-list"))
            # print(driver.find_element_by_id("event-discovery-list").text)
            # driver.close()


#return array of array containing details of free food events in each element
def get_member_emails():
    #contains html of page as seen in browser
    bsObj = BeautifulSoup(get_member_list_page(), "html.parser")
    memberList = bsObj.find("", {"id":"roster-members"}).findChildren()
    for member in memberList:
        print(member.text)
    # print(memberList)
    # eventList = bsObj.findAll("a", {"href":re.compile("\/event\/")})
    # print(eventList[0]['href'])
    #within the html of each event, find tags with string contents
    # eventDetails is an array of arrays, each element contains info for an event 
    
    # eventDetails = [event.findAll(string=True) for event in eventList]
    # eventDetails = []
    # #can somehow use list comprehension to filter for eventDetail?
    # for event in eventList:
    #     temp = event.findAll(string=True)
    #     temp.append(event['href'])
    #     eventDetails.append(temp)
    
    # return eventDetails
   
get_member_list_page()

