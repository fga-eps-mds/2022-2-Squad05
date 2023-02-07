import importlib
import inspect
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
from estados_do_usuario import EstadoDoUsuario
import importlib.util as util
from geral import *

class Callback:

    def get_callback_str(self):
        return ''
    
    async def lida_callback(update: Update,context: ContextTypes.DEFAULT_TYPE):
        pass
    



def import_all_callbacks(global_dict,src_folder='src'):
    for file in os.listdir(src_folder):
        try:
            a = importlib.import_module(file.split('.')[0])
        except ValueError as e:
            continue
            
        for key in a.__dict__.keys():
            if inspect.isclass(a.__dict__[key]) and issubclass(a.__dict__[key],Callback) and key not in global_dict:
                global_dict[key] = a.__dict__[key]