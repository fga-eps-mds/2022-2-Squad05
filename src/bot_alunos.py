


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
from ver_cursos_aluno import VerCursosAluno



BOT_TOKEN = "5624757690:AAGmsRPmRfEhBnEqKhIfW9pcBjNXsMeDeVY"


from estados_do_usuario import lida_com_todos_os_estados_do_usuario,set_estado_do_usuario
from callback import Callback,import_all_callbacks
from nosso_inline_keyboard_button import NossoInlineKeyboardButton
from pegar_codigo_curso import *
from nao_deseja_entrar_em_curso import *




logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)




async def start(update: Update,context: ContextTypes.DEFAULT_TYPE):
    make_sure_flags_are_init(update.effective_chat.id)
    make_sure_estado_is_init(update)
    
    dados = call_database_and_execute("SELECT * FROM users WHERE user_id = ?",[update.effective_chat.id])

    if len(dados) == 0:

        await send_message_or_edit_last(update,context,text="Olá! Sou o Botezinho, um bot para te levar pelo rio do conhecimento!\n\nGostaria de entrar em um curso?",buttons=[
            [
                NossoInlineKeyboardButton(text="sim",callback=PegarCodigoCurso())
            ],
            [
                NossoInlineKeyboardButton(text="não",callback=NaoDesejaEntrarEmCurso())
            ]
        ])
    else:
        await main_menu(update,context)



async def main_menu(update: Update,context: ContextTypes.DEFAULT_TYPE):
    make_sure_flags_are_init(update.effective_chat.id)
    cursos_usuario = call_database_and_execute("SELECT curso_id FROM alunos_por_curso WHERE aluno_id = ?",[update.effective_chat.id])
    #TODO
    buttons = [
        [
            NossoInlineKeyboardButton("entrar em um curso",callback=PegarCodigoCurso())
        ]
    ]
    print(cursos_usuario)
    if len(cursos_usuario) > 0:
        buttons.append([
            NossoInlineKeyboardButton("ver meus cursos",callback=VerCursosAluno())
        ])
    
    await send_message_or_edit_last(update,context,text="Olá! Sou o Botezinho, um bot para te levar pelo rio do conhecimento!\n\nComo posso te ajudar hoje?",buttons=buttons)



async def handler_generic_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    make_sure_flags_are_init(update.effective_chat.id)

    await lida_com_todos_os_estados_do_usuario(update,context)

async def voltar_ao_menu(update: Update,context: ContextTypes.DEFAULT_TYPE):
    make_sure_flags_are_init(update.effective_chat.id)
    await main_menu(update,context)


if __name__ == '__main__':
    import_all_callbacks(globals())
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    start_handler = CommandHandler('start', start)

    for subclasse in get_all_subclasses(CallbackSemDados):
        application.add_handler(CallbackQueryHandler(callback=subclasse.lida_callback,pattern=subclasse.__name__))
    
        
    application.add_handler(start_handler)
    application.add_handler(CallbackQueryHandler(voltar_ao_menu,pattern="voltar_ao_menu"))
    
    application.add_handler(MessageHandler(filters.TEXT,handler_generic_message))

    application.run_polling()