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



class EstadoDoUsuario:
        __estados_dos_usuarios = {}
        def get_estados_dos_usuarios():
            return EstadoDoUsuario.__estados_dos_usuarios
       
        def lida_com_mensagem(self,update: Update,context: ContextTypes.DEFAULT_TYPE):
            pass

def make_sure_estado_is_init(update: Update):
    if update.effective_chat.id not in EstadoDoUsuario.get_estados_dos_usuarios():
            EstadoDoUsuario.get_estados_dos_usuarios()[update.effective_chat.id] = EstadoDoUsuario()


def get_estados_dos_usuarios():
    return EstadoDoUsuario.get_estados_dos_usuarios()

def clear_estados_dos_usuarios():
    EstadoDoUsuario.get_estados_dos_usuarios().clear()

def lida_com_todos_os_estados_do_usuario(update: Update,context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id in EstadoDoUsuario.get_estados_dos_usuarios():
        EstadoDoUsuario.get_estados_dos_usuarios()[update.effective_chat.id].lida_com_mensagem(update,context)

def set_estado_do_usuario(usuario_id,estado: EstadoDoUsuario):
    EstadoDoUsuario.get_estados_dos_usuarios()[usuario_id] = estado