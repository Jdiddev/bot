import os
import time
import random
import spintax
import requests


import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from credentials import username as usr, password as passw
from webdriver_manager.firefox import GeckoDriverManager as GM
from random import seed
from random import randint
import pandas as pd


class Bot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        user_agent = "Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16"
        profile = webdriver.FirefoxProfile()
        profile.set_preference("general.useragent.override", user_agent)
        self.bot = webdriver.Firefox(profile, executable_path=GM().install())
        self.bot.set_window_size(1000,1000)
        with open(r'tags.txt', 'r') as f:
            tagsl = [line.strip() for line in f]
        self.tags = tagsl
        self.urls = []
    
    def exit(self):
        bot = self.bot
        bot.quit()

    def login(self):
        bot = self.bot
        bot.get('https://instagram.com/')
        time.sleep(3)
        print('yoyo')
        
        print('yoyo2')
        time.sleep(5)
       
            
        #// COOOOKIEEEES
        bot.find_element_by_xpath('/html/body/div[4]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[3]/div[1]/div/button').click()
        print("Accepted cookies")
        time.sleep(4)
          #// Cliccck logiiin
        bot.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/article/div/div/div/div/div[2]/div[3]/button[1]').click()
        
        print("Logging in...")     
        time.sleep(2)              
           
           
        if check_exists_by_xpath(bot, '/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/article/div/div/div/div/div[2]/form/div[1]/div[3]/div'):
            username_field = bot.find_element_by_xpath( '/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/article/div/div/div/div/div[2]/form/div[1]/div[3]/div/label/input')
            print("notfound path username")
            username_field.send_keys(self.username)
        print("not entred")   
        find_pass_field = (
            By.XPATH, '/html/body/div[1]/section/main/div[1]/div/div/div/form/div[1]/div[4]/div/label/input')
        WebDriverWait(bot, 50).until(
            EC.presence_of_element_located(find_pass_field))
        pass_field = bot.find_element(*find_pass_field)
        WebDriverWait(bot, 50).until(
            EC.element_to_be_clickable(find_pass_field))
        pass_field.send_keys(self.password)
        

        
        
       
        if check_exists_by_xpath(bot, '/html/body/div[1]/section/main/article/div/div/div/form/div[1]/div[6]/button'):
            bot.find_element_by_xpath('/html/body/div[1]/section/main/div[1]/div/div/div/form/div[1]/div[6]/button').click()
            
            
       # if check_exists_by_xpath(bot , '/html/body/div[1]/section/main/article/div/div/div/form/div[1]/div[6]/button'):
      #      bot.find_element_by_xpath('/html/body/div[1]/section/main/article/div/div/div/form/div[1]/div[6]/button').click()
       
       
       
       
       
       
       
       
        time.sleep(10)

    def get_posts(self):
        print('Searching post by tag...')
        bot = self.bot
        tags = self.tags
        i=0
        tag = tags.pop()
        t = pd.read_csv('listcommented290621.csv')
        dt = pd.DataFrame(t , columns=['link'])
        print(dt)
        link = 'https://www.instagram.com/'+tag+'/tagged/'
        for k in dt['link']:
           
            print(k)
            bot.get(k)
            time.sleep(randint(5,10))

        
            if check_exists_by_xpath(bot, '/html/body/div[1]/div/div/section/main/div/div/article/div[3]/section[1]/span[1]/button/div/span/svg'):
                print('clicked')
                bot.find_elements_by_class_name('wpO6b  ')[2].click()
            


            
            if check_exists_by_xpath(bot,'/html/body/div[1]/section/main/section/div/form/textarea'):
                comments_field = bot.find_element_by_class_name('Ypffh')
                
               
            #   bot.find_element_by_class_name('Ypffh').click()
                WebDriverWait(bot, 1000000).until(EC.element_to_be_clickable((By.CLASS_NAME, 'Ypffh'))).click()
             #   bot.implicitly_wait(6)
                comments_field = bot.find_element_by_class_name('Ypffh')
                
                comments_field.send_keys(random_comment())
                i=i+1
                bot.find_elements_by_xpath("/html/body/div[1]/section/main/section/div/form/button")[0].click()
                
                
            else:
                 print('notfounded')
                 continue
            time.sleep(randint(60,180))
            print(i)
        print(i)
           
def random_comment():
    
       # commentsl = [line.strip() for line in f]
       # comments = commentsl
    listme = ['']
    listmeNotags = ['']

    comment = random.choice(listme)
    
    return comment





def check_exists_by_xpath(driver, xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return True

    return False


run = Bot(usr, passw)
run.login()

if __name__ == '__main__':
    if run.tags == []:
        print("Finished")
    else:
        run.get_posts()
