import os
import time
import random
import pandas as pd
from selenium.webdriver.common.by import By

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.firefox import GeckoDriverManager

from credentials import username as usr, password as passw

class Bot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        user_agent = "Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16"
        profile = webdriver.FirefoxProfile()
        profile.set_preference("general.useragent.override", user_agent)
        self.bot = webdriver.Firefox(profile, executable_path=GeckoDriverManager().install())
        self.bot.set_window_size(1000, 1000)
        with open(r'tags.txt', 'r') as f:
            self.tags = [line.strip() for line in f]
    
    def exit(self):
        self.bot.quit()

    def login(self):
        bot = self.bot
        bot.get('https://instagram.com/')
        time.sleep(3)
        print('Navigated to Instagram')
        
        # Accept cookies
      #  bot.find_element_by_xpath('/html/body/div[4]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[3]/div[1]/div/button').click()
        print("Accepted cookies")
        time.sleep(4)
        
        # Click login
        bot.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/article/div/div/div/div/div[2]/div[3]/button[1]/div').click()
        print("Clicked login")
        time.sleep(2)
        
        # Enter username   ok
        username_field = bot.find_element_by_name('username')
        username_field.send_keys(self.username)
        print("Entered username")
        
        # Enter password    ok
        pass_field = bot.find_element_by_name('password')
        pass_field.send_keys(self.password)
        print("Entered password")
        
        # Submit login   failed
        bot.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/article/div/div/div/div/div[2]/form/div[1]/div[6]/button/div').click()
        print("Logging in...")
        time.sleep(10)

    def get_posts(self):
        print('Searching posts by tag...')
        bot = self.bot
        tags = self.tags
        i = 0
        for tag in tags:
            bot.get(f'https://www.instagram.com/explore/tags/{tag}/')
            time.sleep(random.randint(5, 10))
            
            # Get post links
            posts = bot.find_elements_by_css_selector('a[href^="/p/"]')
            post_links = [post.get_attribute('href') for post in posts]
            
            for link in post_links:
                print(f'Visiting post: {link}')
                bot.get(link)
                time.sleep(random.randint(5, 10))
                
                # Click comment button
                try:
                    bot.find_element_by_css_selector('button[type="button"] > svg[aria-label="Comment"]').click()
                    time.sleep(random.randint(3, 5))
                    
                    # Enter comment
                    comment_field = bot.find_element_by_css_selector('textarea[aria-label="Add a comment…"]')
                    comment_field.send_keys(random_comment())
                    time.sleep(1)
                    
                    # Submit comment
                    comment_field.send_keys(Keys.ENTER)
                    print('Commented')
                    i += 1
                except NoSuchElementException:
                    print('Comment button not found')
                    continue
                
                time.sleep(random.randint(60, 180))
        print(f'Total comments added: {i}')

def random_comment():
    comments = ['Great post!', 'Amazing!', 'Nice shot!', 'Love it!', 'Keep it up!']
    return random.choice(comments)

if __name__ == '__main__':
    run = Bot(usr, passw)
    run.login()
    run.get_posts()
