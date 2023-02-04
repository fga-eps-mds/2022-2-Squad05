from geral import *
from estados_do_usuario import *
from ver_curso_especifico_aluno import *
from nosso_inline_keyboard_button import *

class EntrandoEmCurso(EstadoDoUsuario):
    async def lida_com_mensagem(self, update: Update, context: ContextTypes.DEFAULT_TYPE):

        
        return await super().lida_com_mensagem(update, context)

class MandandoSenhaCurso(EntrandoEmCurso):
    async def lida_com_mensagem(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        
        dados_curso = call_database_and_execute("SELECT hash_senha FROM cursos WHERE id = ?",[context.user_data["codigo"]])

        if dados_curso["hash_senha"] == hash_string(update.effective_message.text):
            call_database_and_execute("INSERT INTO alunos_por_curso (aluno_id,curso_id,aulas_completas) VALUES (?,?,?)",[update.effective_chat.id,context.user_data["codigo"],""])
            set_estado_do_usuario(update.effective_chat.id,EstadoDoUsuario())
            await VerCursoEspecificoAluno(context.user_data["codigo"]).lida_callback(update,context,context.user_data["codigo"])
        else:
            await send_message_on_new_block(update,context,text="A senha está incorreta, por favor tente novamente...",buttons=[
                [
                    InlineKeyboardButton(text="voltar ao menu",callback_data="voltar_ao_menu")
                ]
            ])
            return

        return await super().lida_com_mensagem(update, context)


class MandandoCodigoCurso(EntrandoEmCurso):
    async def lida_com_mensagem(self, update: Update, context: ContextTypes.DEFAULT_TYPE):

        curso_existe = call_database_and_execute("SELECT * FROM cursos WHERE id = ?",[update.effective_message.text])
        if len(curso_existe) == 0:
            await send_message_on_new_block(update,context,text="Não consegui encontrar um curso com esse id, por favor tente novamente...",buttons=[
                [
                    InlineKeyboardButton(text="voltar ao menu",callback_data="voltar_ao_menu")
                ]
            ])
            return
        if curso_existe[0]["hash_senha"] != "":
            await send_message_on_new_block(update,context,text="Parece que esse curso precisa de uma senha para entrar, por favor digite a senha para entrar no curso...")
            set_estado_do_usuario(update.effective_chat.id,MandandoSenhaCurso())
            return
        call_database_and_execute("INSERT INTO alunos_por_curso (aluno_id,curso_id,aulas_completas) VALUES (?,?,?)",[update.effective_chat.id,update.effective_message.text,""])

        await VerCursoEspecificoAluno(update.effective_message.text).lida_callback(update,context,update.effective_message.text)

        return await super().lida_com_mensagem(update, context)