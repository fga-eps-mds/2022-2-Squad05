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
from bot_cursos import Callback



class CallbackSemDados(Callback):

    

    def get_callback_str(self):
        return f'{self.__class__.__name__}'
