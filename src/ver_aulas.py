from callback_sem_dados import CallbackSemDados
from callback_com_dados import CallbackComDados
from telegram import Update
from telegram.ext import ContextTypes
from geral import *


class VerAulas(CallbackComDados):
    async def lida_callback(update: Update, context: ContextTypes.DEFAULT_TYPE, dados):
        
        id_curso = dados
        dados = call_database_and_execute("SELECT * FROM aulas_por_curso WHERE curso_id = ?",[id_curso])
        if len(dados) == 0:
            await send_message_or_edit_last(update,context,text="""Vejo que você não cadastrou nenhuma aula nesse curso ainda, gostaria de cadastrar novas aulas?""",buttons=[
                [
                    InlineKeyboardButton(text="sim, usando Excel",callback_data=f"enviar_aulas_excel {id_curso}")
                ],
                [
                    InlineKeyboardButton(text="sim, uma por uma",callback_data=f"enviar_aulas_individualmente {id_curso}")
                ],
                [
                    InlineKeyboardButton(text='voltar ao menu',callback_data='voltar_ao_menu')
                ]
            ])
        else:
            buttons = [[InlineKeyboardButton(f'{data["titulo"]}',callback_data=f"ver_aula {data['aula_id']}")] for i,data in enumerate(dados)]

            #TODO
            buttons.append([InlineKeyboardButton('adicionar aula',callback_data=f"adicionar_aula {id_curso}")])

            buttons.append([InlineKeyboardButton("voltar",callback_data=f"ver_curso_especifico {id_curso}")])


            await send_message_or_edit_last(update,context,text="Qual aula você gostaria de ver?",buttons=buttons)
            return

        