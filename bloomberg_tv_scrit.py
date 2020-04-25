from selenium import webdriver

# incognito window

driver = webdriver.Chrome(r"C:\Users\Tyler Wooten\Documents\chromedriver.exe")
driver.get("http://www.bloomberg.com/live/us")
driver.implicitly_wait(5)
driver.fullscreen_window()

driver.implicitly_wait(40)
fullscreen = driver.find_element_by_xpath('//*[@id="bvp-multim-983323"]/div[8]/div[3]/button[2]')
fullscreen.click()
driver.implicitly_wait(2700)

driver.quit()
