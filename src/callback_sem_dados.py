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

from geral import call_database_and_execute, hash_string,get_all_subclasses,add_set_update_and_context_to_function_call
from callback import Callback

import os
import inspect

class CallbackSemDados(Callback):

    
    def get_callback_str(self):
        return f'{self.__class__.__name__}'
    
    @staticmethod
    def add_to_application(application):
        for subclasse in get_all_subclasses(CallbackSemDados):
            application.add_handler(CallbackQueryHandler(callback=add_set_update_and_context_to_function_call(subclasse.lida_callback),pattern=subclasse.__name__))
    
