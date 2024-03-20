# bot.py

import os
import time
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.firefox import GeckoDriverManager
from credentials import username as usr, password as passw
from comment_generator import random_comment

class Bot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        user_agent = "Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16"
        profile = webdriver.FirefoxProfile()
        profile.set_preference("general.useragent.override", user_agent)
        self.bot = webdriver.Firefox(profile, executable_path=GeckoDriverManager().install())
        self.bot.set_window_size(1000, 1000)
        with open('tags.txt', 'r') as f:
            self.tags = [line.strip() for line in f]

    def exit(self):
        self.bot.quit()

    def login(self):
        bot = self.bot
        bot.get('https://instagram.com/')
        time.sleep(3)
        print('Navigated to Instagram')
        
        # Accept cookies
        # bot.find_element_by_xpath('/html/body/div[4]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[3]/div[1]/div/button').click()
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

    def search_by_hashtag(self, hashtag):
        print(f'Searching posts by #{hashtag}...')
        bot = self.bot
        bot.get(f'https://www.instagram.com/explore/tags/{hashtag}/')
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
            except NoSuchElementException:
                print('Comment button not found')
                continue

            time.sleep(random.randint(60, 180))

    def search_by_all_hashtags(self):
        for tag in self.tags:
            self.search_by_hashtag(tag)

if __name__ == '__main__':
    run = Bot(usr, passw)
    run.login()
    run.search_by_all_hashtags()
