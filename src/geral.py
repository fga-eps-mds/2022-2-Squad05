


from copy import deepcopy
import logging
from telegram import Update,InlineKeyboardButton
from telegram.ext import ApplicationBuilder,MessageHandler, ContextTypes, CommandHandler,CallbackQueryHandler
import telegram.ext.filters as filters
import telegram
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from hashlib import sha256
from typing import List
import sqlite3 as sql


def get_all_subclasses(cls):
    subclasses = cls.__subclasses__()
    for i in cls.__subclasses__():
        subclasses += get_all_subclasses(i)
    return subclasses
    
def hash_string(senha: str):
    return sha256(senha.encode('utf-8')).hexdigest()[:15]

def call_database_and_execute(statement,parameters = []) -> List[sql.Row]:
    """função para auxiliar no uso do banco de dados SQL"""
    db = sql.connect("database.db")
    db.row_factory = sql.Row
    data = db.cursor().execute(statement,parameters)
    
    final_data =  data.fetchall()
    db.commit()
    db.close()
    return final_data



# dicionario para guardar o id da ultima mensagem mandada p/ cada usuário
# serve para evitar mandarmos muitas mensagens
last_messages = {}

# flags por usuário para controlar em qual estágio da conversa ele está
flags_per_user = {}




flags = {
    "entrando_em_curso":False,
        "mandando_codigo":False,
        "mandando_senha":False
}


temp_dados_curso = {}


def reset_temp_curso(user_id):
    temp_dados_curso[user_id] = {"nome":"","descricao":"","senha":"","id":""}

def make_sure_flags_are_init(user_id):
    """função auxiliar para garantir que não vamos acessar um usuário não existente"""
    if user_id not in flags_per_user:
        flags_per_user[user_id] = deepcopy(flags)




# função auxiliar para evitar mudar uma mensagem muito atrás
def reset_last_message(user_id):
    if user_id in last_messages:
        del last_messages[user_id]

def reset_flags(user_id):
    """função auxiliar para resetar as flags"""
    flags_per_user[user_id] = deepcopy(flags)


async def send_message_on_new_block(update: Update,context: ContextTypes.DEFAULT_TYPE,text:str,buttons = [],parse_mode = ''):
    for column in range(len(buttons)):
        for row in range(len(buttons[column])):
            if buttons[column][row].__class__.__name__ == "NossoInlineKeyboardButton":
                buttons[column][row] = buttons[column][row].get_button()
    
    reset_last_message(update.effective_chat.id)
    await context.bot.send_message(chat_id=update.effective_chat.id,text=text,reply_markup=telegram.InlineKeyboardMarkup(inline_keyboard=buttons),parse_mode=parse_mode)
    

async def send_message_or_edit_last(update: Update,context: ContextTypes.DEFAULT_TYPE,text:str,buttons = [],parse_mode = ''):
    """função auxiliar para enviar uma mensagem mais facilmente ou editar a última se possível"""

    for column in range(len(buttons)):
        for row in range(len(buttons[column])):
            if buttons[column][row].__class__.__name__ == "NossoInlineKeyboardButton":
                buttons[column][row] = buttons[column][row].get_button()
                

    if update.effective_chat.id in last_messages:
        await context.bot.edit_message_text(chat_id=update.effective_chat.id,message_id=last_messages[update.effective_chat.id],text=text,reply_markup=telegram.InlineKeyboardMarkup(inline_keyboard=buttons))
    else:
        message = await context.bot.send_message(chat_id=update.effective_chat.id,text=text,reply_markup=telegram.InlineKeyboardMarkup(inline_keyboard=buttons),parse_mode=parse_mode)
        last_messages[update.effective_chat.id] = message.id