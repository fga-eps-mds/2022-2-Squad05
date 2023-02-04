from geral import *
from callback_com_dados import *
from ver_aula_especifica_curso_alunos import *
from ver_aulas_curso_alunos import *
from nosso_inline_keyboard_button import *


class VerCursoEspecificoAluno(CallbackComDados):
    async def lida_callback(update: Update, context: ContextTypes.DEFAULT_TYPE,id_curso):

        dados_curso = call_database_and_execute("SELECT * FROM cursos WHERE id = ?",[id_curso])[0]
        dados_aluno = call_database_and_execute("SELECT * FROM alunos_por_curso WHERE aluno_id = ? AND curso_id = ?",[update.effective_chat.id,id_curso])[0]
        pass
        text= f"Bem vindo ao curso {dados_curso['nome']}!\n\n{dados_curso['descricao']}\n\nPara qual área você deseja seguir?"

        buttons= [
            [
                #TODO mudar para que as aulas sejam vistas uma por uma em sequência
                NossoInlineKeyboardButton(text="ver aulas",callback_data=VerAulasCursoAlunos(id_curso))
            ]
        ]
        aulas_completas = dados_aluno['aulas_completas'].split(" ")
        if len(aulas_completas) > 0:
            buttons.append(
                [
                    #TODO fazer as aulas serem visiveis
                    InlineKeyboardButton(text=f"continuar aula {len(aulas_completas)}",callback_data="ver_aula {}")
                ]
            )

        await send_message_or_edit_last(update,context,text,buttons)

        return await super().lida_callback(context)