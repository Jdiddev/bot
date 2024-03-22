import json
import time
import random
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager

class InstagramBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.bot = webdriver.Firefox(executable_path=GeckoDriverManager().install())

    def login(self):
        bot = self.bot
        bot.get('https://instagram.com/')
        time.sleep(3)

        # Accepter les cookies
        # À ajuster selon votre interface
        # bot.find_element_by_xpath('/html/body/div[4]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[3]/div[1]/div/button').click()
        time.sleep(2)

        # Cliquer sur le bouton de connexion
        #bot.find_element(By.CSS_SELECTOR, 'button[type="button"]').click()  # Utilisation du type de bouton pour le bouton de connexion
        time.sleep(2)

        # Remplir les champs d'identification
        bot.find_element_by_name('username').send_keys(self.username)
        bot.find_element_by_name('password').send_keys(self.password)
        bot.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[3]/button/div').click()  # Utilisation du type de bouton pour le bouton de soumission
        time.sleep(4)

    def get_post_links_by_tag(self, tag, num_posts):
        bot = self.bot
        bot.get(f'https://www.instagram.com/explore/tags/{tag}/')
        time.sleep(3)

        post_links = set()  # Utilisation d'un ensemble pour éviter les doublons
        while len(post_links) < num_posts:
            # Faire défiler la page pour charger plus de publications
            bot.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(random.randint(2, 4))

            # Collecter les liens des publications visibles
            posts = bot.find_elements(By.CSS_SELECTOR, 'a[href^="/p/"]')
            for post in posts:
                print(post.get_attribute('href'))
                print('im adding link')
                post_links.add(post.get_attribute('href'))
            print('im heeere')
            # Vérifier si on a atteint le nombre de publications désiré
            if len(post_links) >= num_posts:
                break

        return list(post_links)[:num_posts]

    def write_links_to_csv(self, links, filename='instagram_links.csv'):
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Post Links'])
            writer.writerows([[link] for link in links])

    def close(self):
        self.bot.quit()

if __name__ == "__main__":
    # Lecture des informations de connexion depuis le fichier de configuration JSON
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
    username = config['hype.fashiontr']['username']
    password = config['hype.fashiontr']['password']

    tag = input("Entrez le tag que vous souhaitez explorer : ")
    num_posts = int(input("Entrez le nombre de liens de publications à récupérer : "))

    bot = InstagramBot(username, password)
    bot.login()

    post_links = bot.get_post_links_by_tag(tag, num_posts)
    print(f"{len(post_links)} liens de publications récupérés avec succès.")

    bot.write_links_to_csv(post_links)
    print("Les liens ont été enregistrés dans le fichier 'instagram_links.csv'.")

    bot.close()
