# from urllib.request import urlopen
# from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time

def get_sample_events():
    return "sample event yo"

def get_free_food_events():
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
            # print(driver.find_element_by_id("event-discovery-list").text)
            return driver.find_element_by_id("event-discovery-list").text
            driver.close()

# get_free_food_events()