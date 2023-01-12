


from copy import deepcopy
import logging
from telegram import Update,InlineKeyboardButton
from telegram.ext import ApplicationBuilder,MessageHandler, ContextTypes, CommandHandler,CallbackQueryHandler
import telegram.ext.filters as filters
import telegram
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from geral import *
from hashlib import sha256
from estados_do_usuario import make_sure_estado_is_init



BOT_TOKEN = "5624757690:AAGmsRPmRfEhBnEqKhIfW9pcBjNXsMeDeVY"


from estados_do_usuario import lida_com_todos_os_estados_do_usuario,set_estado_do_usuario
from callback import Callback
from callback_com_dados import CallbackComDados
from callback_sem_dados import CallbackSemDados
from nosso_inline_keyboard_button import NossoInlineKeyboardButton





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
                InlineKeyboardButton(text="sim",callback_data="pegar_codigo_curso")
            ],
            [
                InlineKeyboardButton(text="não",callback_data="nao_deseja_entrar")
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
            InlineKeyboardButton("entrar em um curso",callback_data="pegar_codigo_curso")
        ]
    ]
    print(cursos_usuario)
    if len(cursos_usuario) > 0:
        buttons.append([
            InlineKeyboardButton("ver meus cursos",callback_data="ver_cursos")
        ])
    
    await send_message_or_edit_last(update,context,text="Olá! Sou o Botezinho, um bot para te levar pelo rio do conhecimento!\n\nComo posso te ajudar hoje?",buttons=buttons)

async def pegar_codigo_curso(update: Update,context: ContextTypes.DEFAULT_TYPE):
    make_sure_flags_are_init(update.effective_chat.id)
    await send_message_or_edit_last(update,context,text="Ok. Por favor me diga o código do curso que você deseja entrar...",buttons=[
        [
            InlineKeyboardButton(text="não tenho código",callback_data="nao_possui_codigo")
        ]
    ])
    flags_per_user[update.effective_chat.id]["entrando_em_curso"] = True
    flags_per_user[update.effective_chat.id]["mandando_codigo"] = True

async def nao_deseja_entrar(update: Update,context: ContextTypes.DEFAULT_TYPE):
    make_sure_flags_are_init(update.effective_chat.id)
    await send_message_or_edit_last(update,context,text="Tudo certo! Se precisar de mim, só mandar uma mensagem com /start nesse chat e eu virei te ajudar!")
    reset_flags(update.effective_chat.id)

async def ver_cursos(update: Update,context: ContextTypes.DEFAULT_TYPE):
    make_sure_flags_are_init(update.effective_chat.id)

    cursos_participantes = call_database_and_execute("SELECT curso_id FROM alunos_por_curso WHERE aluno_id = ?",[update.effective_chat.id])
    dados_cursos = call_database_and_execute(f"SELECT * FROM cursos WHERE curso_id IN ({','.join(list(map(lambda p: '?',cursos_participantes)))})",list(map(lambda p: p['curso_id'],cursos_participantes)))
    print(cursos_participantes)
    buttons = [[InlineKeyboardButton(text=curso['nome'],callback_data=f"ver_curso {curso['curso_id']}")] for curso in dados_cursos]

    buttons.append([
        InlineKeyboardButton(text="voltar ao menu",callback_data="voltar_ao_menu")
    ])

    text = "Qual curso você gostaria de ver hoje?"

    await send_message_or_edit_last(update,context,text=text,buttons=buttons)

async def handler_generic_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    make_sure_flags_are_init(update.effective_chat.id)

    if flags_per_user[update.effective_chat.id]["entrando_em_curso"]:
        if flags_per_user[update.effective_chat.id]["mandando_codigo"]:
            curso_existe = call_database_and_execute("SELECT * FROM cursos WHERE id = ?",[update.effective_message.text])
            if len(curso_existe) == 0:
                await send_message_on_new_block(update,context,text="Não consegui encontrar um curso com esse id, por favor tente novamente...")
                return
            if curso_existe[0]["hash_senha"] != "":
                await send_message_on_new_block(update,context,text="Parece que esse curso precisa de uma senha para entrar, por favor digite a senha para entrar no curso...")
                reset_flags(update.effective_chat.id)
                flags_per_user[update.effective_chat.id]["entrando_em_curso"] = True
                flags_per_user[update.effective_chat.id]["mandando_senha"] = True

                context.user_data['codigo'] = update.effective_message.text
                return
            call_database_and_execute("INSERT INTO alunos_por_curso (aluno_id,curso_id,aulas_completas) VALUES (?,?,?)",[update.effective_chat.id,update.effective_message.text,""])

            await mostrar_curso(update.effective_message.text,update,context)

        if flags_per_user[update.effective_chat.id]["mandando_senha"]:
            dados_curso = call_database_and_execute("SELECT hash_senha FROM cursos WHERE id = ?",[context.user_data["codigo"]])

            if dados_curso["hash_senha"] == hash_string(update.effective_message.text):
                call_database_and_execute("INSERT INTO alunos_por_curso (aluno_id,curso_id,aulas_completas) VALUES (?,?,?)",[update.effective_chat.id,context.user_data["codigo"],""])
                await mostrar_curso(context.user_data["codigo"],update,context)
            else:
                await send_message_on_new_block(update,context,text="A senha está incorreta, por favor tente novamente...")
                return

async def mostrar_curso(id_curso: str,update: Update,context: ContextTypes.DEFAULT_TYPE):
    make_sure_flags_are_init(update.effective_chat.id)
    dados_curso = call_database_and_execute("SELECT * FROM cursos WHERE id = ?",[id_curso])[0]
    dados_aluno = call_database_and_execute("SELECT * FROM alunos_por_curso WHERE aluno_id = ? AND curso_id = ?",[update.effective_chat.id,id_curso])[0]
    pass
    text= f"Bem vindo ao curso {dados_curso['nome']}!\n\n{dados_curso['descricao']}\n\nPara qual área você deseja seguir?"

    buttons= [
        [
            InlineKeyboardButton(text="ver aulas",callback_data=f"ver_aulas_curso {id_curso}")
        ]
    ]
    aulas_completas = dados_aluno['aulas_completas'].split(" ")
    if len(aulas_completas) > 0:
        buttons.append(
            [
                InlineKeyboardButton(text=f"continuar aula {len(aulas_completas)}",callback_data="ver_aula {}")
            ]
        )

    await send_message_or_edit_last(update,context,text,buttons)

async def voltar_ao_menu(update: Update,context: ContextTypes.DEFAULT_TYPE):
    make_sure_flags_are_init(update.effective_chat.id)
    await main_menu(update,context)



async def nao_possui_codigo(update: Update,context: ContextTypes.DEFAULT_TYPE):
    make_sure_flags_are_init(update.effective_chat.id)
    await send_message_or_edit_last(update,context,text="Esse código é o id do curso em que você deseja entrar.\n\nPara obte-lo, solicite-o ao dono do curso.")
 
if __name__ == '__main__':

    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    start_handler = CommandHandler('start', start)

    for subclasse in Callback.__subclasses__():
        application.add_handler(CallbackQueryHandler(callback=subclasse.lida_callback,pattern=subclasse.__name__))
    

    application.add_handler(start_handler)
    application.add_handler(CallbackQueryHandler(pegar_codigo_curso,pattern="pegar_codigo_curso"))
    application.add_handler(CallbackQueryHandler(nao_deseja_entrar,pattern="nao_deseja_entrar"))
    application.add_handler(CallbackQueryHandler(voltar_ao_menu,pattern="voltar_ao_menu"))
    application.add_handler(CallbackQueryHandler(ver_cursos,pattern="ver_cursos"))
    application.add_handler(CallbackQueryHandler(nao_possui_codigo,pattern="nao_possui_codigo"))
    
    application.add_handler(MessageHandler(filters.TEXT,handler_generic_message))

    application.run_polling()