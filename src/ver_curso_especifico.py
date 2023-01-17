from callback_sem_dados import CallbackSemDados
from callback_com_dados import CallbackComDados
from telegram import Update
from telegram.ext import ContextTypes
from geral import *
from nosso_inline_keyboard_button import NossoInlineKeyboardButton
from receber_id_curso import ReceberIdCurso
from ver_aulas import VerAulas


class VerCursoEspecifico(CallbackComDados):
    async def lida_callback(update: Update, context: ContextTypes.DEFAULT_TYPE, dados,manda_em_novo_bloco=False):
        id_curso = dados
        dados_curso = call_database_and_execute("SELECT * FROM cursos WHERE id = ?",[id_curso])
        print(dados_curso)
        buttons = [
                [
                    #InlineKeyboardButton(text="ver id do curso",callback_data=f"receber_id_curso {id_curso}")
                    NossoInlineKeyboardButton(text="ver id do curso",callback=ReceberIdCurso(id_curso))
                ],
                [
                    InlineKeyboardButton(text="editar nome",callback_data=f"editar_nome_curso {id_curso}")
                ],
                [
                    InlineKeyboardButton(text="editar senha",callback_data=f"editar_senha {id_curso}")
                ],
                [
                    InlineKeyboardButton(text="editar descrição",callback_data=f"editar_descricao_curso {id_curso}")
                ],
                [
                    InlineKeyboardButton(text="ver aulas",callback_data=f"editar_aulas {id_curso}")
                ],
                [
                    InlineKeyboardButton(text="voltar ao menu",callback_data="voltar_ao_menu")
                ],
            ]
        text = f"O que você gostaria de editar?\n\nCurso atual: {dados_curso[0]['nome']}\n\nPrecisa de senha? {dados_curso[0]['hash_senha'] != ''}\n\nDescrição do curso: {dados_curso[0]['descricao']}"
        if manda_em_novo_bloco:
            send_message_on_new_block(update,context,text=text,buttons=buttons)
        else:
            await send_message_or_edit_last(update,context,text=text,buttons=buttons)
