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


estados_dos_usuarios = {

}

class EstadoDoUsuario:

        def __chamar_subclasses(self,classe_desejada,update: Update,context: ContextTypes.DEFAULT_TYPE):
            for subclasse in self.__class__.__subclasses__():
                if issubclass(subclasse,classe_desejada) or subclasse.__name__ == self.__class__.__name__:
                    temp = subclasse()
                    temp.lida_com_mensagem()
                    temp.__chamar_subclasses(classe_desejada)

        def lida_com_mensagem(update: Update,context: ContextTypes.DEFAULT_TYPE):
            pass

def make_sure_estado_is_init(update: Update):
    if update.effective_chat.id not in estados_dos_usuarios:
            estados_dos_usuarios[update.effective_chat.id] = EstadoDoUsuario()


def lida_com_todos_os_estados_do_usuario(update: Update,context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id in estados_dos_usuarios:
        estados_dos_usuarios[update.effective_chat.id].__chamar_subclasses(estados_dos_usuarios[update.effective_chat.id].__class__,update,context)

def set_estado_do_usuario(usuario_id,estado: EstadoDoUsuario):
    estados_dos_usuarios[usuario_id] = estado