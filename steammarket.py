import os
import time
from http import client
import telebot
import steampy
from steampy.client import SteamClient
from steampy.exceptions import TooManyRequests
from steampy.models import GameOptions, Currency
from steampy.utils import(load_credentials, get_market_listings_from_html)
from bs4 import BeautifulSoup
import requests
import json

# TOKENS
BOT_TOKEN = os.environ['BOT_TOKEN'] = '6762721742:AAGLld-llWTKuIFnw9qD41HURM_5oMwG8GU'
bot = telebot.TeleBot(BOT_TOKEN)

USER_DATA_FILE = 'user_data.json'

STEAM_API_KEY = os.environ['STEAM_API_KEY'] = '16D3DF4E58A4E4A924D0D06A779D5BAA'
steam_client = SteamClient(STEAM_API_KEY)

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

"""def get_best_skins(skin_name):


    try:

        #listings = get_market_listings_from_html(skin_name) with SteamClient('16D3DF4E58A4E4A924D0D06A779D5BAA', 'jennyjohnson5z', 'a7CrHDYAXN1988') as client:

        listings = client.market.get_my_market_listings(skin_name)
        best_buy_offers = client.market.fetch_price(skin_name, GameOptions.CS)
        return listings
    except Exception as e:
        print("error", e)
        return {}
"""
# BOT ACTIONS
@bot.message_handler(commands=['start'])
def start(message):
    mess = f'Hi <b>{message.from_user.first_name}</b>, lets find your cs2 skins'
    bot.send_message(message.chat.id, mess, parse_mode='html')

@bot.message_handler(commands=['help'])
def help(message):
    mess = (f'<i>/start</i> - start/restart our bot \n/start - start/restart our bot')
    bot.send_message(message.chat.id, mess, parse_mode='html')

@bot.message_handler(commands=['current_skin'])
def current_skin(message):
    mess = 'Input current skin, which you like to check: '
    bot.send_message(message.chat.id, mess, parse_mode='html')


""""@bot.message_handler(commands=['get_skins'])
def get_skins(message):
    skin_name = 'M4A1-S | Cyrex (Factory New)'
    skins = get_best_skins(skin_name)
    if skins:
        bot.send_message(message.chat.id, skins)
    else:
        bot.send_message(message.chat.id, 'At this moment bot has no offers')
"""
@bot.message_handler(commands=['find_skin'])
def find_best_skins(message):
    bot.reply_to(message, "Finding the best skins...")

    @bot.message_handler(commands=['find_skins'])
    def find_skins(message):
        # Получаем список всех скинов на Steam Market
        skins = steam_client.get_market_recently_listings(GameOptions.CS,
                                                          'https://steamcommunity.com/market/listings/730/Revolution%20Case')  # '730' - ID игры CS:GO, 'Weapon' - тип скина

        # Сортируем скины по цене в убывающем порядке
        sorted_skins = sorted(skins, key=lambda x: x['sell_price'], reverse=True)

        # Отправляем пользователю информацию о 5 самых дорогих скинах
        count = 0
        for skins in sorted_skins:
            if count < 5:
                bot.reply_to(message, f"Название: {skins['name']}\nЦена: {skins['sell_price']}\n")
                count += 1
            else:
                break

""" def find_skins():
        try:
            # Scrape or fetch data from your storage (replace with actual scraping code)
            data = requests.get("https://steamcommunity.com/market/listings/730/Revolution%20Case")
            soup = BeautifulSoup(data.content, "html.parser")
            # Extract relevant skin data (replace with actual extraction logic)
            skins = []
            for item in soup.find_all("div", class_="market_listing_row"):
                skins.append({
                    "name": item.find("span", class_="market_listing_title_name").text,
                    "price": item.find("span", class_="market_listing_price").text
                })

            # Filter and recommend skins based on criteria (replace with your logic)
            recommended_skins = sorted(skins, key=lambda skin: float(skin["price"]))[:3]

            # Send response to user
            response = "Here are some recommended skins:\n"
            for skin in recommended_skins:
                response += f"- {skin['name']} (price: {skin['price']})\n"
            bot.send_message(message.chat.id, response)
        except Exception as e:
            print("error", e)
            return {}"""

bot.polling(non_stop=True)
