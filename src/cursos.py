from geral import *
from estados_do_usuario import EstadoDoUsuario,set_estado_do_usuario
from nosso_inline_keyboard_button import NossoInlineKeyboardButton
from callback_sem_dados import *
from callback_com_dados import *
from menu_principal import MenuPrincipal
import csv
# Criação de curso



    
class NaoDesejaCriarCurso(CallbackSemDados):
    def __init__(self) -> None:
        super().__init__()

    async def lida_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):

        """
        função para quando o usuário não deseja criar uma conta ou interagir com o bot agora
        """
        return await send_message_or_edit_last(text="Tudo certo!\n\nQuando quiser utilizar meus serviços digite /start nesse chat e eu virei te ajudar!\n\nTenha um bom dia :D")

class CriarCurso(CallbackSemDados):
    async def lida_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):

        set_estado_do_usuario(update.effective_chat.id,MandandoNomeCurso())

        return await send_message_on_new_block("Ok, vamos criar seu curso!\n\nQual título você quer em seu curso?",buttons=[
            [NossoInlineKeyboardButton("voltar ao menu",callback=MenuPrincipal(""))]
        ])

class MandandoNomeCurso(EstadoDoUsuario):
    async def lida_com_mensagem(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        context.user_data["nome"] = update.effective_message.text

        await send_message_on_new_block(text="Ok! Agora me diga uma breve descrição do seu curso",
                buttons=[
                    [
                        NossoInlineKeyboardButton("voltar ao menu",callback=MenuPrincipal(""))
                    ]
                ]
            )
        set_estado_do_usuario(update.effective_chat.id,MandandoDescricaoCurso())

    
class NaoDesejaColocarSenhaEmCurso(CallbackSemDados):
    async def lida_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
        
        id_curso = hash_string(str(update.effective_chat.id) + "curso" + context.user_data['nome'])
        call_database_and_execute("INSERT INTO cursos (nome,descricao,hash_senha,id_dono,id) VALUES (?,?,?,?,?)",[
            context.user_data["nome"],
            context.user_data["descricao"],
            "",
            update.effective_chat.id,
            id_curso
        ])

        set_estado_do_usuario(update.effective_chat.id,EstadoDoUsuario())

        await MenuPrincipal.lida_callback(update,context,"Ok seu curso foi adicionado!\n\n")


class MandandoDescricaoCurso(EstadoDoUsuario):
    async def lida_com_mensagem(self, update: Update, context: ContextTypes.DEFAULT_TYPE):

        context.user_data["descricao"] = update.effective_message.text_markdown_v2

        await send_message_on_new_block(text="Ok! Agora me diga a senha para os alunos entrarem no seu curso",
            buttons=[
                [
                    NossoInlineKeyboardButton("não desejo colocar",callback=NaoDesejaColocarSenhaEmCurso())
                ],
                [
                    NossoInlineKeyboardButton("voltar ao menu",callback=MenuPrincipal(""))
                ]
            ]
        )

        set_estado_do_usuario(update.effective_chat.id,MandandoSenhaCurso())

    
class MandandoSenhaCurso(EstadoDoUsuario):

    async def lida_com_mensagem(self, update: Update, context: ContextTypes.DEFAULT_TYPE):

        id_curso = hash_string(str(update.effective_chat.id) + "curso" + context.user_data['nome'])
        call_database_and_execute("INSERT INTO cursos (nome,descricao,hash_senha,id_dono,id) VALUES (?,?,?,?,?)",[
            context.user_data["nome"],
            context.user_data["descricao"],
            hash_string(update.effective_message.text),
            update.effective_chat.id,
            id_curso
        ])

        set_estado_do_usuario(update.effective_chat.id,EstadoDoUsuario())

        await MenuPrincipal.lida_callback(update,context,"Ok seu curso foi adicionado!\n\n")

# Edição de curso

class EditarNomeCurso(CallbackComDados):
    async def lida_callback(update: Update, context: ContextTypes.DEFAULT_TYPE, dados):

        
        context.user_data["id_curso"] = dados
        set_estado_do_usuario(update.effective_chat.id,EditandoNomeCurso())

        return await send_message_or_edit_last(text="Ok! Qual nome você deseja associar a esse curso?",
            buttons=[
                [
                    NossoInlineKeyboardButton(text="voltar",callback=VerCursoEspecifico(dados))
                ]
            ]
        )
    
class EditarDescricaoCurso(CallbackComDados):
    async def lida_callback(update: Update, context: ContextTypes.DEFAULT_TYPE, dados):

        context.user_data['id_curso'] = dados
        set_estado_do_usuario(update.effective_chat.id,EditandoDescricaoCurso())

        return await send_message_or_edit_last(text="Ok! Me diga qual descrição você gostaria de colocar nesse curso...",
            buttons=[
                [
                    
                    NossoInlineKeyboardButton(text="voltar",callback=VerCursoEspecifico(dados))
                ]
            ]
        )

class EditarSenhaCurso(CallbackComDados):
    async def lida_callback(update: Update, context: ContextTypes.DEFAULT_TYPE, dados):

        buttons = [
                [
                    NossoInlineKeyboardButton(text="voltar",callback=VerCursoEspecifico(dados))
                ]
            ]
        dados_curso = call_database_and_execute("SELECT hash_senha FROM cursos WHERE id = ?",[dados])
        if dados_curso[0]["hash_senha"] != "":
            buttons.append([
                    NossoInlineKeyboardButton(text="quero remover a senha",callback=RemoverSenha(dados))
                ])
            buttons.reverse()

        context.user_data["id_curso"] = dados
        set_estado_do_usuario(update.effective_chat.id,EditandoSenhaCurso())

        return await send_message_or_edit_last(text="Ok! Me diga a nova senha para entrar nesse curso (os usuários antigos continuarão cadastrados)...",
            buttons=buttons
        )
    
class ReceberIdCurso(CallbackComDados):
    async def lida_callback(update: Update, context: ContextTypes.DEFAULT_TYPE, dados):
        

        return await context.bot.send_message(chat_id=update.effective_chat.id,text=dados)     


class VerCursos(CallbackSemDados):
    async def lida_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):

        data = call_database_and_execute("SELECT nome,id FROM cursos WHERE id_dono = ?",[update.effective_chat.id])

        print(list(map(lambda i: len(f'ver_curso_especifico {i["id"]}'.encode('utf-8')),data)))

        buttons = [[NossoInlineKeyboardButton(text=i['nome'],callback=f'VerCursoEspecifico {i["id"]}')] for i in data]

        buttons.append([NossoInlineKeyboardButton(text="voltar ao menu",callback=MenuPrincipal(""))])

        return await send_message_or_edit_last(text="Qual curso você deseja editar?",buttons=buttons)
            


    
class VerCursoEspecifico(CallbackComDados):
    async def lida_callback(update: Update, context: ContextTypes.DEFAULT_TYPE, id_curso):
        print(id_curso)
        dados_curso = call_database_and_execute("SELECT * FROM cursos WHERE id = ?",[id_curso])
        print(dados_curso)
        buttons = [
                [
                    #InlineKeyboardButton(text="ver id do curso",callback_data=f"receber_id_curso {id_curso}")
                    NossoInlineKeyboardButton(text="ver id do curso",callback=ReceberIdCurso(id_curso))
                ],
                [
                    NossoInlineKeyboardButton(text="editar nome",callback=EditarNomeCurso(id_curso))
                ],
                [
                    NossoInlineKeyboardButton(text="editar senha",callback=EditarSenhaCurso(id_curso))
                ],
                [
                    NossoInlineKeyboardButton(text="editar descrição",callback=EditarDescricaoCurso(id_curso))
                ],
                [
                    NossoInlineKeyboardButton(text="progresso dos alunos",callback=ProgressoDosAlunosPorCurso(id_curso))
                ],
                [
                    NossoInlineKeyboardButton(text="ver aulas",callback=f"VerAulas {id_curso}")
                ],
                [
                    NossoInlineKeyboardButton(text="voltar ao menu",callback=MenuPrincipal(""))
                ],
            ]
        text = f"O que você gostaria de editar?\n\nCurso atual: {dados_curso[0]['nome']}\n\nPrecisa de senha? {dados_curso[0]['hash_senha'] != ''}\n\nDescrição do curso:\n{dados_curso[0]['descricao']}"
        return await send_message_or_edit_last(text=text,buttons=buttons)


class ProgressoDosAlunosPorCurso(CallbackComDados):
    async def lida_callback(update: Update, context: ContextTypes.DEFAULT_TYPE, id_curso):

        dados_alunos = call_database_and_execute("SELECT * FROM alunos_por_curso WHERE id_curso = ?",[id_curso])
       

        message = f'Seu curso possui {len(dados_alunos)} alunos cadastrados\n\nGostaria de exportar os dados para um arquivo excel?'

        buttons = [
            [
                NossoInlineKeyboardButton(text="sim",callback=ExportarProgressoDosAlunos(id_curso))
            ],
            [
                NossoInlineKeyboardButton(text="voltar",callback=VerCursoEspecifico(id_curso))
            ]
        ]

        return await send_message_or_edit_last(message,buttons)

class ExportarProgressoDosAlunos(CallbackComDados):
    async def lida_callback(update: Update, context: ContextTypes.DEFAULT_TYPE, id_curso):
        dados_alunos = call_database_and_execute("SELECT * FROM alunos_por_curso WHERE id_curso = ?",[id_curso])
        aulas_por_curso = call_database_and_execute("SELECT * FROM aulas_por_curso WHERE id_curso = ?",[id_curso])
        await send_message_or_edit_last("Ok! Aguarde um momento...")
        file_name = f'{update.effective_chat.id}_{time.time()}.csv'
        with open(file_name,'w') as f:
            writer = csv.writer(f)   


            writer.writerow(["Nome Aluno\\Titulo Aula"] + [i['titulo'] for i in aulas_por_curso])
            for i in dados_alunos:
                aulas_finalizadas = list(map(lambda x: x["id_aula"],call_database_and_execute("SELECT id_aula FROM aulas_por_aluno WHERE id_aluno = ?",[i['id_aluno']])))

                writer.writerow([(await context.bot.get_chat(i['id_aluno'])).full_name] + [1 if data['id_aula'] in aulas_finalizadas else 0 for i,data in enumerate(aulas_por_curso)])
            
        dados_curso = call_database_and_execute("SELECT * FROM cursos WHERE id = ?",[id_curso])
        await context.bot.send_document(update.effective_chat.id,open(file_name,'rb'),filename=f'{dados_curso[0]["nome"]}.csv')

        os.remove(file_name)

        await send_message_on_new_block(f'Aqui estão os dados sobre o curso {dados_curso[0]["nome"]}')

        return await VerCursoEspecifico.lida_callback(update,context,id_curso)



class RemoverSenha(CallbackComDados):
    async def lida_callback(update: Update, context: ContextTypes.DEFAULT_TYPE, dados):

        call_database_and_execute("UPDATE cursos SET hash_senha = ? WHERE id = ?",["",dados])

        await send_message_on_new_block("Senha atualizada!")

        await VerCursoEspecifico.lida_callback(update,context,dados)


class EditandoNomeCurso(EstadoDoUsuario):
    async def lida_com_mensagem(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        #TODO
        id = context.user_data['id_curso']
        call_database_and_execute("UPDATE cursos SET nome = ? WHERE id = ?",[update.effective_message.text,id])
        await send_message_on_new_block(text="Nome atualizado!")

        return await VerCursoEspecifico.lida_callback(update,context,context.user_data['id_curso'])


class EditandoDescricaoCurso(EstadoDoUsuario):
    async def lida_com_mensagem(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        #TODO

        id = context.user_data['id_curso']
        call_database_and_execute("UPDATE cursos SET descricao = ? WHERE id = ?",[update.effective_message.text,id])
        await send_message_on_new_block(text="Descrição atualizada!")

        return await VerCursoEspecifico.lida_callback(update,context,context.user_data['id_curso'])
    
class EditandoSenhaCurso(EstadoDoUsuario):

    async def lida_com_mensagem(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        #TODO
        id = context.user_data['id_curso']
        call_database_and_execute("UPDATE cursos SET hash_senha = ? WHERE id = ?",[hash_string(update.effective_message.text),id])

        await send_message_on_new_block(text="Senha atualizada!")

        return await VerCursoEspecifico.lida_callback(update,context,context.user_data['id_curso'])