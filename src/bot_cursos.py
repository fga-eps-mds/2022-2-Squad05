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
from callback_com_dados import CallbackComDados
from callback_sem_dados import CallbackSemDados

from geral import *


from estados_do_usuario import EstadoDoUsuario, lida_com_todos_os_estados_do_usuario,set_estado_do_usuario
from callback import Callback,import_all_callbacks
from lida_com_excel import lida_com_arquivo_excel
from menu_principal import *
from nosso_inline_keyboard_button import NossoInlineKeyboardButton
from estados_do_usuario import make_sure_estado_is_init
from cursos import *
from aulas import *

# definindo como o log vai ser salvo
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """função chamada quando uma conversa nova é iniciada ou ao mandar um /start"""
    
    data = call_database_and_execute("SELECT * FROM users WHERE id_user = ?",(update.effective_user.id,))
    reset_flags(update.effective_chat.id)
    reset_last_message(update.effective_chat.id)
    make_sure_estado_is_init(update)
    message = """Olá! Sou o Bote, o salva-vidas dos seus cursos!
    
"""
    message += "Sou um bot para criar e administrar cursos pelo Telegram!\n\n"
    if len(data) == 0:
        message += "Gostaria de criar um curso?"
        call_database_and_execute("INSERT INTO users (id_user) VALUES (?)",[update.effective_chat.id])
        await send_message_or_edit_last(text=message,buttons=[
        [
            NossoInlineKeyboardButton(text="Sim",callback=CriarCurso()),
        ],
        [
            #telegram.InlineKeyboardButton(text="Não",callback_data='nao_deseja_criar_curso')
            NossoInlineKeyboardButton('Não',callback=NaoDesejaCriarCurso())
        ]
        ])
    else:

        await MenuPrincipal.lida_callback(update,context,message)

def inicializa_bot_cursos(application):
    start_handler = CommandHandler('start',add_set_update_and_context_to_function_call(start))

    application.add_handler(start_handler)
    
    CadastrarAulaExcel.add_to_application(application)
    CallbackSemDados.add_to_application(application)
    CallbackComDados.add_to_application(application)
    EstadoDoUsuario.add_to_application(application)
    
    application.run_polling()
    
if __name__ == '__main__':
    import_all_callbacks(globals())

    application = ApplicationBuilder().token('5507439323:AAGiiQ0_vnqIilIRBPRBtGnS54eje4D5xVE').build()
    
    start_handler = CommandHandler('start',add_set_update_and_context_to_function_call(start))

    application.add_handler(start_handler)
    
    CadastrarAulaExcel.add_to_application(application)
    CallbackSemDados.add_to_application(application)
    CallbackComDados.add_to_application(application)
    EstadoDoUsuario.add_to_application(application)
    
    application.run_polling()