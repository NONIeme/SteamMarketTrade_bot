#test git
import os
import telebot
import steampy
from steampy.client import SteamClient
from steampy.exceptions import TooManyRequests
from steampy.models import GameOptions, Currency
from steampy.utils import load_credentials
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


@bot.message_handler(commands=['get_skins'])
def get_skins(message):
    skin_name = 'M4A1-S | Cyrex (Factory New)'
    skins = get_best_skins(skin_name)

    if skins:
        bot.send_message(message.chat.id, skins)
    else:
        bot.send_message(message.chat.id, 'At this moment bot has no offers')


def get_best_skins(skin_name):
    try:
        best_buy_offers = steam_client.market.get_best_buy_offers(skin_name, GameOptions.CS)
        return best_buy_offers
    except Exception as e:
        print("error", e)
        return {}




bot.polling(non_stop=True)
