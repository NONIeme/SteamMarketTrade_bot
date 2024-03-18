import os
import time
import telebot
from http import client
from typing import List, Dict, Any
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import urllib3
from bs4 import BeautifulSoup
import requests
import json
from html.parser import HTMLParser

# TOKENS
BOT_TOKEN = os.environ['BOT_TOKEN'] = '6762721742:AAGLld-llWTKuIFnw9qD41HURM_5oMwG8GU'
bot = telebot.TeleBot(BOT_TOKEN)

USER_DATA_FILE = 'user_data.json'

url = 'https://sih.app/?marketsMax=%5B19%5D&profitSort=%22percentDESC%22&appId=730&priceGreaterThanSteam=true&marketsMin=%5B18%5D&commissionsIsActive=true&tags=%5B%7B%22value%22%3A%22Player%20Autograph%22%2C%22name%22%3A%22Sticker%20Type%22%7D%2C%7B%22value%22%3A%22Team%20Logo%22%2C%22name%22%3A%22Sticker%20Type%22%7D%2C%7B%22value%22%3A%22Tournament%22%2C%22name%22%3A%22Sticker%20Type%22%7D%2C%7B%22value%22%3A%2210%20Year%20Birthday%20Sticker%20Capsule%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%222020%20RMR%20Challengers%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%222020%20RMR%20Contenders%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%222020%20RMR%20Legends%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%222021%20Community%20Sticker%20Capsule%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22Ambush%20Sticker%20Capsule%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22Antwerp%202022%20Challengers%20Stickers%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22Antwerp%202022%20Contenders%20Stickers%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22Antwerp%202022%20Legends%20Stickers%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22Antwerp%202022%20Player%20Autographs%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22Atlanta%202017%20Challengers%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22Atlanta%202017%20Legends%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22Atlanta%202017%20Player%20Autographs%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22Battlefield%202042%20Sticker%20Capsule%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22Berlin%202019%20Legends%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22Berlin%202019%20Minor%20Challengers%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22Berlin%202019%20Player%20Autographs%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22Berlin%202019%20Returning%20Challengers%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22Bestiary%20Capsule%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22Boston%202018%20Legends%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22Boston%202018%20Minor%20Challengers%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22Boston%202018%20Player%20Autographs%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22Boston%202018%20Returning%20Challengers%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22Broken%20Fang%20Sticker%20Collection%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22Chicken%20Capsule%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22Cologne%202016%20Challengers%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22Cologne%202016%20Legends%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22Cologne%202016%20Player%20Autographs%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22Community%20Capsule%202018%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22Community%20Sticker%20Capsule%201%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22CS20%20Sticker%20Capsule%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22DreamHack%202014%20Challengers%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22DreamHack%202014%20Legends%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22DreamHack%20Cluj-Napoca%202015%20Challengers%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22DreamHack%20Cluj-Napoca%202015%20Legends%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22DreamHack%20Cluj-Napoca%202015%20Player%20Autographs%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22EMS%20Katowice%202014%20Challengers%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22EMS%20Katowice%202014%20Legends%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22Enfu%20Sticker%20Capsule%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22ESL%20One%20Cologne%202014%20Challengers%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22ESL%20One%20Cologne%202014%20Legends%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22ESL%20One%20Cologne%202015%20Challengers%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22ESL%20One%20Cologne%202015%20Legends%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22ESL%20One%20Cologne%202015%20Player%20Autographs%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22ESL%20One%20Katowice%202015%20Challengers%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22ESL%20One%20Katowice%202015%20Legends%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22Espionage%20Sticker%20Capsule%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22Feral%20Predators%20Capsule%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22Half-Life%3A%20Alyx%20Sticker%20Capsule%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22Halo%20Capsule%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22Katowice%202019%20Legends%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22Katowice%202019%20Minor%20Challengers%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22Katowice%202019%20Player%20Autographs%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22Katowice%202019%20Returning%20Challengers%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22Krakow%202017%20Challengers%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22Krakow%202017%20Legends%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22Krakow%202017%20Player%20Autographs%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22London%202018%20Legends%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22London%202018%20Minor%20Challengers%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22London%202018%20Player%20Autographs%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22London%202018%20Returning%20Challengers%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22MLG%20Columbus%202016%20Challengers%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22MLG%20Columbus%202016%20Legends%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22MLG%20Columbus%202016%20Player%20Autographs%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22Operation%20Riptide%20Sticker%20Collection%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22Paris%202023%20Challengers%20Stickers%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22Paris%202023%20Contenders%20Stickers%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22Paris%202023%20Legends%20Stickers%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22Paris%202023%20Player%20Autographs%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22Perfect%20World%20Sticker%20Capsule%201%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22Perfect%20World%20Sticker%20Capsule%202%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22Pinups%20Capsule%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22Poorly%20Drawn%20Capsule%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22Recoil%20Sticker%20Collection%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22Rio%202022%20Challengers%20Stickers%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22Rio%202022%20Contenders%20Stickers%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22Rio%202022%20Legends%20Stickers%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22Rio%202022%20Player%20Autographs%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22Riptide%20Surf%20Shop%20Sticker%20Collection%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22Shattered%20Web%20Sticker%20Collection%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22Skill%20Groups%20Capsule%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22Slid3%20Capsule%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22Sticker%20Capsule%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22Sticker%20Capsule%202%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22Stockholm%202021%20Challengers%20Stickers%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22Stockholm%202021%20Contenders%20Stickers%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22Stockholm%202021%20Legends%20Stickers%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22Stockholm%202021%20Player%20Autographs%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22Sugarface%20Capsule%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22Team%20Roles%20Capsule%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22The%20Boardroom%20Sticker%20Capsule%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%2C%7B%22value%22%3A%22Warhammer%2040%2C000%20Sticker%20Capsule%22%2C%22name%22%3A%22Sticker%20Collection%22%7D%5D'
headers = {
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}
driver = webdriver.Chrome()
driver.get(url)

def get_html(url, params=None):
    r = requests.get(url, headers=headers, params=params)
    return r

# DATABASE
def save_user_data(user_data):
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(user_data, file)

def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as file:
            return json.load(file)
    else:
        return {}

# BOT ACTIONS
@bot.message_handler(commands=['start'])
def start(message):
    mess = f'Hi <b>{message.from_user.first_name}</b>, lets find your cs2 skins'
    bot.send_message(message.chat.id, mess, parse_mode='html')

@bot.message_handler(commands=['help'])
def help(message):
    mess = (f'<i>/start</i> - start/restart our bot \n<i>/find_skin</i> - finding the most profitable skin by %')
    bot.send_message(message.chat.id, mess, parse_mode='html')

@bot.message_handler(commands=['find_skin'])
def find_best_skin(message):
    bot.reply_to(message, "Finding the best skin...")
    time.sleep(10)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    item = soup.find('div', class_='gap-y-5px')["title"]
    profit_percent = soup.find('span', class_='lt-md:font-400').text
    profit_dollar = soup.find('div', class_='lt-md:text-12px').text
    bot.send_message(message.chat.id, str(item)+ '\nYour % profit is: '+ str(profit_percent) + '\nYour $ profit is: '+ str(profit_dollar), 'html')


bot.polling(non_stop=True)
