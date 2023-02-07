from geral import *
from callback_com_dados import *
from nosso_inline_keyboard_button import NossoInlineKeyboardButton

class MenuPrincipalAlunos(CallbackComDados):
    async def lida_callback(update: Update, context: ContextTypes.DEFAULT_TYPE, *dados):


        cursos_usuario = call_database_and_execute("SELECT id_curso FROM alunos_por_curso WHERE id_aluno = ?",[update.effective_chat.id])
        #TODO
        buttons = [
            [
                NossoInlineKeyboardButton("entrar em um curso",callback="PegarCodigoCurso")
            ]
        ]
        print(cursos_usuario)
        if len(cursos_usuario) > 0:
            buttons.append([
                NossoInlineKeyboardButton("ver meus cursos",callback="VerCursosAluno")
            ])
        
        return await send_message_or_edit_last(text="Olá! Sou o Botezinho, um bot para te levar pelo rio do conhecimento!\n\nComo posso te ajudar hoje?",buttons=buttons)

