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
from estados_do_usuario import EstadoDoUsuario


#TODO Colocar nos bots

class CadastrandoAula(EstadoDoUsuario):
    def lida_com_mensagem(self,update: Update, context: ContextTypes.DEFAULT_TYPE):

        print('faz as coisas')

        return super().lida_com_mensagem(context)


class MandandoTituloAula(CadastrandoAula):
    def lida_com_mensagem(self,update: Update, context: ContextTypes.DEFAULT_TYPE):

        print('lida com estado...')

        return super().lida_com_mensagem(context)

class MandandoDescricaoAula(CadastrandoAula):
    def lida_com_mensagem(self,update: Update, context: ContextTypes.DEFAULT_TYPE):

        pass
        return super().lida_com_mensagem(context)