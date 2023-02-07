from geral import *
from callback_com_dados import *
from callback_sem_dados import *
from nosso_inline_keyboard_button import *
from estados_do_usuario import *
from menu_principal_alunos import *

#entrando em curso

class EntrandoEmCurso(EstadoDoUsuario):
    async def lida_com_mensagem(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        
        return await MandandoCodigoCurso().lida_com_mensagem(update,context)
        

class MandandoSenhaCurso(EntrandoEmCurso):
    async def lida_com_mensagem(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        
        dados_curso = call_database_and_execute("SELECT hash_senha FROM cursos WHERE id = ?",[context.user_data["codigo"]])

        if dados_curso["hash_senha"] == hash_string(update.effective_message.text):
            call_database_and_execute("INSERT INTO alunos_por_curso (id_aluno,id_curso) VALUES (?,?)",[update.effective_chat.id,context.user_data["codigo"]])
            await VerCursoEspecificoAluno.lida_callback(update,context,context.user_data["codigo"])
        else:
            set_estado_do_usuario(update.effective_chat.id,MandandoSenhaCurso())
            return await send_message_on_new_block(text="A senha está incorreta, por favor tente novamente...",buttons=[
                [
                    NossoInlineKeyboardButton(text="voltar ao menu",callback_data=MenuPrincipalAlunos(""))
                ]
            ])
            



class MandandoCodigoCurso(EntrandoEmCurso):
    async def lida_com_mensagem(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        curso_existe = call_database_and_execute("SELECT * FROM cursos WHERE id = ?",[update.effective_message.text])
        if len(curso_existe) == 0:
            await send_message_on_new_block(text="Não consegui encontrar um curso com esse id, por favor tente novamente...",buttons=[
                [
                    NossoInlineKeyboardButton(text="voltar ao menu",callback=MenuPrincipalAlunos(""))
                ]
            ])
            set_estado_do_usuario(update.effective_chat.id,MandandoCodigoCurso())
            return
        if curso_existe[0]["hash_senha"] != "":
            await send_message_on_new_block(text="Parece que esse curso precisa de uma senha para entrar, por favor digite a senha para entrar no curso...")
            set_estado_do_usuario(update.effective_chat.id,MandandoSenhaCurso())
            return
        call_database_and_execute("INSERT INTO alunos_por_curso (id_aluno,id_curso) VALUES (?,?)",[update.effective_chat.id,update.effective_message.text])

        return await VerCursoEspecificoAluno.lida_callback(update,context,update.effective_message.text)


class NaoPossuiCodigo(CallbackSemDados):
    async def lida_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):

        return await send_message_or_edit_last(text="Esse código é o id do curso em que você deseja entrar.\n\nPara obte-lo, solicite-o ao dono do curso.")


class NaoDesejaEntrarEmCurso(CallbackSemDados):
    async def lida_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
        
        return await send_message_or_edit_last(text="Tudo certo! Se precisar de mim, só mandar uma mensagem com /start nesse chat e eu virei te ajudar!")

class PegarCodigoCurso(CallbackSemDados):
    async def lida_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):


        set_estado_do_usuario(update.effective_chat.id,EntrandoEmCurso())

        return await send_message_or_edit_last(text="Ok. Por favor me diga o código do curso que você deseja entrar...",buttons=[
            [
                NossoInlineKeyboardButton(text="não tenho código",callback=NaoPossuiCodigo())
            ]
        ])

# aulas

# cursos

class VerCursosAluno(CallbackSemDados):
    async def lida_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):

        cursos_participantes = call_database_and_execute("SELECT id_curso FROM alunos_por_curso WHERE id_aluno = ?",[update.effective_chat.id])
        dados_cursos = call_database_and_execute(f"SELECT * FROM cursos WHERE id IN ({','.join(list(map(lambda p: '?',cursos_participantes)))})",list(map(lambda p: p['id_curso'],cursos_participantes)))
        print(cursos_participantes)
        buttons = [[NossoInlineKeyboardButton(text=curso['nome'],callback=VerCursoEspecificoAluno(curso["id"]))] for curso in dados_cursos]

        buttons.append([
            NossoInlineKeyboardButton(text="voltar ao menu",callback=MenuPrincipalAlunos(""))
        ])

        text = "Qual curso você gostaria de ver hoje?"

        return await send_message_or_edit_last(text=text,buttons=buttons)

        
    
class VerCursoEspecificoAluno(CallbackComDados):
    async def lida_callback(update: Update, context: ContextTypes.DEFAULT_TYPE,id_curso):

        dados_curso = call_database_and_execute("SELECT * FROM cursos WHERE id = ?",[id_curso])[0]
        dados_aluno = call_database_and_execute("SELECT * FROM alunos_por_curso WHERE id_aluno = ? AND id_curso = ?",[update.effective_chat.id,id_curso])[0]
        aulas_completas = call_database_and_execute("SELECT * FROM aulas_por_aluno WHERE id_aluno = ?",[update.effective_chat.id])
        aulas_por_curso = call_database_and_execute("SELECT id_aula FROM aulas_por_curso WHERE id_curso = ?",[id_curso])

        text= f"Bem vindo ao curso {dados_curso['nome']}!\n\naulas completas = {len(aulas_completas)}\n\n{dados_curso['descricao']}\n\nPara qual área você deseja seguir?"

        buttons= [
        ]

        if len(aulas_completas) > 0:
            buttons.append([
                NossoInlineKeyboardButton(text="ver aulas completas",callback=f"VerAulasCompletasAluno {id_curso}")
            ])
        if len(aulas_completas) != len(aulas_por_curso):
            buttons.append(
                [
                    NossoInlineKeyboardButton(text=f"ver aulas a fazer",callback=f"VerAulasAFazerAluno {id_curso}")
                ]
            )

        buttons.append([
            NossoInlineKeyboardButton(text="sair do curso",callback=SairDoCursoAluno(id_curso))
        ])

        buttons.append([
            NossoInlineKeyboardButton(text="voltar",callback=VerCursosAluno())
        ])

        return await send_message_or_edit_last(text,buttons)

       
class SairDoCursoAluno(CallbackComDados):
    async def lida_callback(update: Update, context: ContextTypes.DEFAULT_TYPE, id_curso):

        call_database_and_execute("DELETE FROM alunos_por_curso WHERE id_aluno = ? AND id_curso = ?",[update.effective_chat.id,id_curso])
        call_database_and_execute("DELETE FROM aulas_por_aluno WHERE id_aluno = ? AND id_curso = ?",[update.effective_chat.id,id_curso])


        return await MenuPrincipalAlunos.lida_callback(update,context,"Removido do curso!\n\n")