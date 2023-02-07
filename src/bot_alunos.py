


from copy import deepcopy
import logging
from telegram import Update,InlineKeyboardButton
from telegram.ext import ApplicationBuilder,MessageHandler, ContextTypes, CommandHandler,CallbackQueryHandler
import telegram.ext.filters as filters
import telegram
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from callback_sem_dados import CallbackSemDados
from geral import *
from hashlib import sha256
from estados_do_usuario import make_sure_estado_is_init

from menu_principal_alunos import *
from estados_do_usuario import lida_com_todos_os_estados_do_usuario,set_estado_do_usuario
from callback import Callback,import_all_callbacks
from nosso_inline_keyboard_button import NossoInlineKeyboardButton
from cursos_aluno import *
from aulas_aluno import *




logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)




async def start(update: Update,context: ContextTypes.DEFAULT_TYPE):
    MessagesManager.set_update_and_context(update,context)
    make_sure_estado_is_init(update)
    
    dados = call_database_and_execute("SELECT * FROM users WHERE id_user = ?",[update.effective_chat.id])

    if len(dados) == 0:

        await send_message_on_new_block(text="Olá! Sou o Botezinho, um bot para te levar pelo rio do conhecimento!\n\nGostaria de entrar em um curso?",buttons=[
            [
                NossoInlineKeyboardButton(text="sim",callback=PegarCodigoCurso())
            ],
            [
                NossoInlineKeyboardButton(text="não",callback=NaoDesejaEntrarEmCurso())
            ]
        ])
    else:
        await MenuPrincipalAlunos.lida_callback(update,context,"")


def inicializa_bot_alunos(application):
    start_handler = CommandHandler('start', add_set_update_and_context_to_function_call(start))


    application.add_handler(start_handler)
    
    CallbackSemDados.add_to_application(application)
    CallbackComDados.add_to_application(application)
    EstadoDoUsuario.add_to_application(application)

    application.run_polling()


if __name__ == '__main__':
    import_all_callbacks(globals())
    application = ApplicationBuilder().token(TokenHolder.alunos_token).build()
    
    inicializa_bot_alunos(application)