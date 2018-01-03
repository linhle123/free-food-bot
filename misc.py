from urllib.request import urlretrieve
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# driver = webdriver.PhantomJS()
driver = webdriver.Chrome(executable_path='/home/linhle/chromedriver')

driver.set_window_size(1124, 850)
driver.get("https://www.youtube.com/watch?v=zIcPprAOfw0")
try:
    #wait until we can select perks of events
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "html5-video-container")))
finally:
    print("done waiting")
    bsObj = BeautifulSoup(driver.page_source, "html.parser")
    videoLocation = bsObj.find("", {"class" : "html5-video-container"}).find("video").['src']
    urlretrieve(videoLocation, "video.mp4")
    # time.sleep(2)
    # driver.find_element_by_class_name("video-stream html5-main-video").click()
    # print(bsObj)


#     #click to open the perks option
#     try:
#         WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//label[contains(text(), 'Free Food')]")))
#     finally:
#         #click to filter for free food
#         driver.find_element_by_xpath("//label[contains(text(), 'Free Food')]").click()
#         time.sleep(3) #wait for free food filter to take effect, this is stupid solution tho
#         # print(driver.find_element_by_id("event-discovery-list").text)
#         return driver.find_element_by_id("event-discovery-list").text
#         driver.close()

# html = urlopen("https://www.youtube.com/watch?v=zIcPprAOfw0")

# print(videoLocation)
