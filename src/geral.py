


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

def buttons_to_inline_keyboard(buttons: list):
    for row in range(len(buttons)):
        for column in range(len(buttons[row])):
            if buttons[row][column].__class__.__name__ == "NossoInlineKeyboardButton":
                buttons[row][column] = buttons[row][column].get_button()

    return buttons

# dicionario para guardar o id da ultima mensagem mandada p/ cada usuário
# serve para evitar mandarmos muitas mensagens
last_messages = {}

# flags por usuário para controlar em qual estágio da conversa ele está
flags_per_user = {}




flags = {
    "entrando_em_curso":False,
        "mandando_codigo":False,
        "mandando_senha":False,

    "mandando_arquivo":False,

    "cadastrando_aula":False,
        "mandando_titulo_aula":False,
        "mandando_descricao_aula":False,
        "mandando_links_aula":False
}


temp_dados_curso = {}


def reset_temp_curso(id_user):
    temp_dados_curso[id_user] = {"nome":"","descricao":"","senha":"","id":""}

def make_sure_flags_are_init(id_user):
    """função auxiliar para garantir que não vamos acessar um usuário não existente"""
    if id_user not in flags_per_user:
        flags_per_user[id_user] = deepcopy(flags)




# função auxiliar para evitar mudar uma mensagem muito atrás
def reset_last_message(id_user):
    if id_user in last_messages:
        del last_messages[id_user]

def reset_flags(id_user):
    """função auxiliar para resetar as flags"""
    flags_per_user[id_user] = deepcopy(flags)



class MessagesManager:
    current_update = None
    current_context = None

    logging_calls_to_messages = False
    logger_data = []

    @staticmethod
    def enable_testing():
        MessagesManager.logging_calls_to_messages = True

    @staticmethod
    def disable_testing():
        MessagesManager.logging_calls_to_messages = False

    @staticmethod
    def set_update_and_context(update: Update,context: ContextTypes.DEFAULT_TYPE):
        MessagesManager.current_context = context
        MessagesManager.current_update = update

class TokenHolder:
    alunos_token = "5624757690:AAGmsRPmRfEhBnEqKhIfW9pcBjNXsMeDeVY"
    cursos_token = '5507439323:AAGiiQ0_vnqIilIRBPRBtGnS54eje4D5xVE'


    @staticmethod
    def set_alunos_token(token):
        TokenHolder.alunos_token = token

    @staticmethod
    def set_cursos_token(token):
        TokenHolder.cursos_token = token


def add_set_update_and_context_to_function_call(function):
    def wrapper(*args, **kwargs):
        MessagesManager.set_update_and_context(*args[:2])
        
        retval = function(*args, **kwargs)
        return retval
    return wrapper

async def send_message_on_new_block(text:str,buttons = [],parse_mode = ''):
    buttons = buttons_to_inline_keyboard(buttons)

    
    reset_last_message(MessagesManager.current_update.effective_chat.id)
    return await MessagesManager.current_context.bot.send_message(chat_id=MessagesManager.current_update.effective_chat.id,text=text,reply_markup=telegram.InlineKeyboardMarkup(inline_keyboard=buttons),parse_mode=parse_mode)
    

async def send_message_or_edit_last(text:str,buttons = [],parse_mode = ''):
    """função auxiliar para enviar uma mensagem mais facilmente ou editar a última se possível"""

    buttons = buttons_to_inline_keyboard(buttons)



    if MessagesManager.current_update.effective_chat.id in last_messages:
        return await MessagesManager.current_context.bot.edit_message_text(chat_id=MessagesManager.current_update.effective_chat.id,message_id=last_messages[MessagesManager.current_update.effective_chat.id],text=text,reply_markup=telegram.InlineKeyboardMarkup(inline_keyboard=buttons))
    else:
        message = await MessagesManager.current_context.bot.send_message(chat_id=MessagesManager.current_update.effective_chat.id,text=text,reply_markup=telegram.InlineKeyboardMarkup(inline_keyboard=buttons),parse_mode=parse_mode)
        last_messages[MessagesManager.current_update.effective_chat.id] = message.id
        return message

