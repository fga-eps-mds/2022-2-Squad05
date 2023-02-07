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

async def handle_generic_callback(update: Update,context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query.data

    if len(query.split(' ')) > 1:
        descricao_ordem, dados = query.split(' ')
        if dados == ";":
            dados = ""
        if len(dados.split(',')) > 1:
            dados = dados.split(',')
        for subclass in get_all_subclasses(CallbackComDados):
            if descricao_ordem == subclass.__name__:
                await add_set_update_and_context_to_function_call(subclass.lida_callback)(update,context,dados)

class CallbackComDados(Callback):
    async def lida_callback(update: Update, context: ContextTypes.DEFAULT_TYPE,*dados):
        pass
        return await super().lida_callback(update,context)

    def __init__(self,*dados):
        self._dados = dados
    
    def get_callback_str(self):
        return f'{self.__class__.__name__} {",".join(list(map(lambda x: str(x),self._dados)))}'
    
    @staticmethod
    def add_to_application(application):
        application.add_handler(CallbackQueryHandler(callback=handle_generic_callback))

