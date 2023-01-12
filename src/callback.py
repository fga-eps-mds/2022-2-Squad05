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

from geral import call_database_and_execute, hash_string



class Callback:


    def get_callback_str(self):
        ""

    async def lida_callback(update: Update,context: ContextTypes.DEFAULT_TYPE):
        pass