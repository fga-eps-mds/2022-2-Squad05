

from geral import *
from callback_sem_dados import *
from callback_com_dados import *
from nosso_inline_keyboard_button import *
from cursos_aluno import *


class VerAulasAFazerAluno(CallbackComDados):
    async def lida_callback(update: Update, context: ContextTypes.DEFAULT_TYPE, id_curso):
        
        aulas_por_curso = call_database_and_execute("SELECT * FROM aulas_por_curso WHERE id_curso = ?",[id_curso])
        aulas_completas = call_database_and_execute("SELECT id_aula FROM aulas_por_aluno WHERE id_aluno = ? AND id_curso = ?",[update.effective_chat.id,id_curso])
        aulas_completas = list(map(lambda x: x['id_aula'],aulas_completas))

        aulas_a_fazer = filter(lambda x: x["id_aula"] not in aulas_completas,aulas_por_curso)


        message = "Qual aula você quer ver hoje?"

        buttons = [[NossoInlineKeyboardButton(text=i["titulo"],callback=VerAulaEspecificaAluno(i["id_aula"]))] for i in aulas_a_fazer]
        
        return await send_message_or_edit_last(message,buttons)

class VerAulasCompletasAluno(CallbackComDados):
    async def lida_callback(update: Update, context: ContextTypes.DEFAULT_TYPE, id_curso):
        aulas_completas = call_database_and_execute("SELECT * FROM aulas_por_aluno INNER JOIN aulas_por_curso ON  aulas_por_curso.id_aula = aulas_por_aluno.id_aula WHERE aulas_por_aluno.id_aluno = ? AND aulas_por_aluno.id_curso = ?",[update.effective_chat.id,id_curso])

        message = "Qual aula você quer rever hoje?"

        buttons = [[NossoInlineKeyboardButton(text=i["titulo"],callback=VerAulaEspecificaAluno(i["id_aula"]))] for i in aulas_completas]

        return await send_message_or_edit_last(message,buttons)

class VerAulaEspecificaAluno(CallbackComDados):
    async def lida_callback(update: Update, context: ContextTypes.DEFAULT_TYPE, id_aula):
        
        dados_aula = call_database_and_execute("SELECT * FROM aulas_por_curso WHERE id_aula = ?",[id_aula])[0]
        completa = call_database_and_execute("SELECT * FROM aulas_por_aluno WHERE id_aluno = ? AND id_aula = ? AND id_curso = ?",[update.effective_chat.id,id_aula,dados_aula['id_curso']])


        buttons = [
            
        ]

        if len(completa) == 0:
            buttons.append([
                NossoInlineKeyboardButton(text="completar",callback=CompletarAulaAluno(id_aula))
            ])

        buttons.append([
            NossoInlineKeyboardButton(text="voltar",callback=VerCursoEspecificoAluno(dados_aula['id_curso']))
        ])
        

        return await send_message_or_edit_last(text=f"{dados_aula['titulo']}\n\n{dados_aula['descricao']}\n\nMateriais extras:\n{dados_aula['links']}",buttons=buttons)

class CompletarAulaAluno(CallbackComDados):
    async def lida_callback(update: Update, context: ContextTypes.DEFAULT_TYPE, id_aula):

        dados_aula = call_database_and_execute("SELECT * FROM aulas_por_curso WHERE id_aula = ?",[id_aula])[0]

        call_database_and_execute("INSERT INTO aulas_por_aluno (id_aula,id_aluno,id_curso) VALUES (?,?,?)",[id_aula,update.effective_chat.id,dados_aula["id_curso"]])

        await send_message_on_new_block(f'Parabéns por completar a aula "{dados_aula["titulo"]}"!')

        return await VerCursoEspecificoAluno.lida_callback(update,context,dados_aula["id_curso"])

