from callback_sem_dados import *
from geral import *
from ver_curso_especifico_aluno import *
from nosso_inline_keyboard_button import *

class VerCursosAluno(CallbackSemDados):
    async def lida_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):

        cursos_participantes = call_database_and_execute("SELECT curso_id FROM alunos_por_curso WHERE aluno_id = ?",[update.effective_chat.id])
        dados_cursos = call_database_and_execute(f"SELECT * FROM cursos WHERE curso_id IN ({','.join(list(map(lambda p: '?',cursos_participantes)))})",list(map(lambda p: p['curso_id'],cursos_participantes)))
        print(cursos_participantes)
        buttons = [[NossoInlineKeyboardButton(text=curso['nome'],callback=VerCursoEspecificoAluno(curso["curso_id"]))] for curso in dados_cursos]

        buttons.append([
            InlineKeyboardButton(text="voltar ao menu",callback_data="voltar_ao_menu")
        ])

        text = "Qual curso você gostaria de ver hoje?"

        await send_message_or_edit_last(update,context,text=text,buttons=buttons)

        return await super().lida_callback(context)