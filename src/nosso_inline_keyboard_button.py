import logging
from telegram import Update,InlineKeyboardButton
from telegram.ext import ApplicationBuilder,MessageHandler, ContextTypes, CommandHandler,CallbackQueryHandler
import telegram.ext.filters as filters
import telegram
import random
from telegram.constants import ParseMode
import sqlite3 as sql
import os
from typing import List
from copy import deepcopy
import pandas as pd
import time

from callback import Callback


class NossoInlineKeyboardButton:
    def __init__(self,text:str,callback: Callback) -> None:
        self._button = InlineKeyboardButton(text=text,callback_data=callback.get_callback_str())

    def get_button(self):
        return self._button