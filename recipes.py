import selenium
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import re
from selenium.webdriver.common.action_chains import ActionChains
from gensim.models import Word2Vec
import pandas as pd

import re

from sklearn.decomposition import PCA

from matplotlib import pyplot as plt
import plotly.graph_objects as go

import numpy as np

import warnings

driver = selenium.webdriver.Chrome()
driver.get("https://www.bbc.co.uk/food/collections/affordable_30-minute_meals_for_four")
time.sleep(2)
# finding the button using ID

#find list of all links
links = driver.find_elements(By.TAG_NAME, 'a')
link_list = []
for i in links:
    link_list.append(i.text)
link_list = list(filter(None, link_list))
link_list = link_list[30:34]  #for quick testing use this
#link_list = link_list[30:] #for full list


total_list = []
for recipe in link_list:
    wait = WebDriverWait(driver, 5)
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
    #print(ingredient_list)
    total_list.append(ingredient_list)
    #print(total_list)
    #driver.navigate().back() #less reliable way for back button
    driver.execute_script("window.history.go(-1)")
    time.sleep(2)
print(total_list)

# train word2vec model
model = (Word2Vec(total_list, min_count=1, vector_size = 3))
print(model)

# find similar words
sims = model.wv.most_similar('kale', topn=10)
print(sims)

#close browser
#driver.quit()