import selenium
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from selenium.webdriver.common.action_chains import ActionChains

driver = selenium.webdriver.Chrome()
driver.get("https://www.bbc.co.uk/food/collections/affordable_30-minute_meals_for_four")
time.sleep(2)
# finding the button using ID

#less ideal way
#driver.find_element(By.XPATH,"//button[@title='Accept All']").click()
#link = browser.find_element(By.LINK_TEXT,"Pasta alla vodka")

#wait definition
wait = WebDriverWait(driver, 3)

#get rid of ad
#driver.switch_to.frame("sp_message_iframe_1109708")
#wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Accept All']"))).click()
#time.sleep(5)

#scroll and find recipe link name
#driver.execute_script("window.scrollTo(0, 1000)")
#element = driver.find_element(By.XPATH, "//h3[text()='Mary Berry's Bakewell Tart']")
#print(element.text)

#click on recipe link
#wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Mary Berry's Bakewell Tart"))).click()
#time.sleep(5)

#find list of all links
links = driver.find_elements(By.TAG_NAME, 'a')
link_list = []
for i in links:
    link_list.append(i.text)
link_list = list(filter(None, link_list))
link_list = link_list[30:35]  #for quick testing use this
#link_list = link_list[30:] #for full list
#print(link_list) #for testing

for recipe in link_list:
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, recipe))).click()
    time.sleep(1)
    items = driver.find_elements(By.XPATH, "//li[@class='recipe-ingredients__list-item']")
    ingredient_list = []
    for item in items:
        text = item.text
        #print(text) #for testing
        text = re.sub(r'\([^)]*\)', "", text) #take out parentheses
        #remove numbers and any tbsp, oz, g, etc
        # if r' tbsp | tsp |oz ' in text:
        if re.search(" tbsp | tsp |oz ", text):
            text_split = re.split(' tbsp | tsp |oz ', text)
            text_split_2 = text_split[1]
        elif re.search(" x ", text):
            text_split = re.split('tins', text)
            text_split_2 = text_split[1]
        elif re.search(r"\dg ", text):
            text_split = re.split('tin', text)
            text_split_2 = text_split[1]
        elif re.search(r"\d ", text):
            text_split = re.split(r'\d ', text)
            text_split_2 = text_split[1]
        else:
            text_split_2 = text
        #print(text_split_2) #for testing

        #now remove anything after commas
        if ',' in text_split_2:
            text_split_3 = text_split_2.rsplit(',', 1)[0]
        else:
            text_split_3 = text_split_2

        ingredient_list.append(text_split_3)
        #print(text_split_3,'\n')

    print(ingredient_list)

    #driver.navigate().back() #less reliable way for back button
    driver.execute_script("window.history.go(-1)")
    time.sleep(2)

#close browser
#driver.quit()
