import random
from geral import *
from estados_do_usuario import EstadoDoUsuario,set_estado_do_usuario,get_estado_do_usuario
from callback_com_dados import *
from callback_sem_dados import *
from lida_com_excel import lida_com_arquivo_excel
from nosso_inline_keyboard_button import NossoInlineKeyboardButton

# Cadastro Aulas

class CadastrarAulaIndividualmente(CallbackComDados):
    async def lida_callback(update: Update, context: ContextTypes.DEFAULT_TYPE, id_curso):
        context.user_data['id_curso'] = id_curso

        set_estado_do_usuario(update.effective_chat.id,MandandoTituloAula())

        return await send_message_or_edit_last( text = "Ok, vamos adicionar uma aula!\n\nQual título você quer dar para a aula?",
            buttons=[
                [
                    NossoInlineKeyboardButton("voltar ao menu",callback=VerAulas(id_curso))
                ]
            ]
        )


class MandandoTituloAula(EstadoDoUsuario):
    async def lida_com_mensagem(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
        id_curso = context.user_data["id_curso"]


        context.user_data["titulo_aula"] = update.effective_message.text

        set_estado_do_usuario(update.effective_chat.id,MandandoDescricaoAula())

        return await send_message_on_new_block(text="Ok! Agora me diga uma breve descrição da aula",
            buttons=[
                [
                     NossoInlineKeyboardButton("voltar ao menu",callback=VerAulas(id_curso))
                ]
            ]
        )

        
    
class MandandoDescricaoAula(EstadoDoUsuario):
    async def lida_com_mensagem(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        id_curso = context.user_data["id_curso"]

        context.user_data["descricao_aula"] = update.effective_message.text_markdown_v2

        set_estado_do_usuario(update.effective_chat.id,MandandoLinksAula())

        return await send_message_on_new_block(text="Ok! Agora me diga os links que você deseja colocar",
                buttons=[
                    [
                        NossoInlineKeyboardButton("voltar ao menu",callback=VerAulas(id_curso))
                    ]
                ]
            )

   
    


class MandandoLinksAula(EstadoDoUsuario):

    async def lida_com_mensagem(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        id_curso = context.user_data["id_curso"]
        id_aula = hash_string(f'{id_curso} {random.random()}')

        call_database_and_execute("INSERT INTO aulas_por_curso (id_aula, id_curso, titulo, descricao,links) VALUES (?,?,?,?,?)",
                [
                id_aula,
                id_curso,
                context.user_data['titulo_aula'],
                context.user_data['descricao_aula'],
                update.effective_message.text
                ]) 
        
        await send_message_on_new_block("Aula adicionada!")
        
        return await VerAulaEspecifica.lida_callback(update,context,id_aula)
        
# Visualização aulas


class CadastrandoAulaExcel(EstadoDoUsuario):
    async def lida_com_mensagem(self, update: Update, context: ContextTypes.DEFAULT_TYPE):

        set_estado_do_usuario(update.effective_chat.id,CadastrandoAulaExcel())

        return await super().lida_com_mensagem(update, context)

class CadastrarAulaExcel(CallbackComDados):
    async def lida_callback(update: Update, context: ContextTypes.DEFAULT_TYPE,id_curso):



        context.user_data['id_curso'] = id_curso

        set_estado_do_usuario(update.effective_chat.id,CadastrandoAulaExcel())

        return await send_message_or_edit_last(text="""Ok! Para enviar as suas aulas no arquivo excel, por favor crie as colunas

        TITULO | DESCRICAO | LINK
            
        em letra maiúscula exatamente como está escrito acima em um arquivo ".xlsx" ou ".csv" (podem haver várias colunas com o titulo LINK). Ai só mandar aqui que eu vou adicionar lá!""",buttons=[
            [
                NossoInlineKeyboardButton(text="voltar",callback=VerAulas(id_curso))
            ]
        ])  
    
    @staticmethod
    async def handle_excel_file(update: Update,context: ContextTypes.DEFAULT_TYPE):
        if type(get_estado_do_usuario(update.effective_chat.id)) == type(CadastrandoAulaExcel()):
            file =(await context.bot.get_file(update.message.document))
            
            path = await file.download_to_drive()

            try:
                rows, conseguiu = lida_com_arquivo_excel(path)
                if not conseguiu:
                    return await send_message_on_new_block(text=f"O seu arquivo não está no formato correto. Por favor, cheque os nomes das colunas e tente novamente")
                    

                for row in rows:
                    call_database_and_execute("INSERT INTO aulas_por_curso (id_aula,id_curso,titulo,descricao,links) VALUES (?,?,?,?,?)",[
                        hash_string(f'{update.effective_chat.id}_{time.time()}'),
                        context.user_data['id_curso'],
                        row["TITULO"],
                        row["DESCRICAO"],
                        "\n".join(list(filter(lambda x: x != "",[str(row[i]) if i.startswith("LINK") else "" for i in row.keys()])))
                    ])

                os.remove(path)
                return await VerAulas.lida_callback(update,context,context.user_data['id_curso'])
            except Exception as e:
                os.remove(path)
                return await send_message_on_new_block(text=f"Um erro ocorreu enquanto eu lia esse arquivo. Por favor envie esse log para os donos do bot!\n\nError: {e}")
        return None

    @staticmethod
    def add_to_application(application):
        application.add_handler(MessageHandler(callback=add_set_update_and_context_to_function_call(CadastrarAulaExcel.handle_excel_file),filters=filters.Document.FileExtension("xlsx") | filters.Document.FileExtension('csv')))

        
class CadastrarAulas(CallbackComDados):
    async def lida_callback(update: Update, context: ContextTypes.DEFAULT_TYPE,id_curso):

        aulas_cadastradas = call_database_and_execute("SELECT * FROM aulas_por_curso WHERE id_curso = ?",[id_curso])

        if len(aulas_cadastradas) == 0:
            message = """Vejo que você não cadastrou nenhuma aula nesse curso ainda, gostaria de cadastrar novas aulas?"""
        else:
            message = """Como você gostaria de adicionar a(s) aula(s)?"""
        return await send_message_or_edit_last(text=message,buttons=[
            [
                NossoInlineKeyboardButton(text="sim, usando Excel",callback=CadastrarAulaExcel(id_curso))
            ],
            [
                NossoInlineKeyboardButton(text="sim, uma por uma",callback=CadastrarAulaIndividualmente(id_curso))
            ],
            [
                NossoInlineKeyboardButton(text='voltar ao menu',callback=f'VerCursoEspecifico {id_curso}')
            ]
        ])

class VerAulas(CallbackComDados):
    async def lida_callback(update: Update, context: ContextTypes.DEFAULT_TYPE, id_curso):
       
        dados = call_database_and_execute("SELECT * FROM aulas_por_curso WHERE id_curso = ?",[id_curso])
        if len(dados) == 0:
            return await CadastrarAulas.lida_callback(update,context,id_curso,1)
        else:
            buttons = [[NossoInlineKeyboardButton(f'{data["titulo"]}',callback=VerAulaEspecifica(data["id_aula"]))] for i,data in enumerate(dados)]

            #TODO
            buttons.append([NossoInlineKeyboardButton('adicionar aula',callback=f"CadastrarAulas {id_curso}")])

            buttons.append([NossoInlineKeyboardButton("voltar",callback=f"VerCursoEspecifico {id_curso}")])


            return await send_message_or_edit_last(text="Qual aula você gostaria de ver?",buttons=buttons)
        


class VerAulaEspecifica(CallbackComDados):
    async def lida_callback(update: Update, context: ContextTypes.DEFAULT_TYPE, id_aula):

        dados_aula = call_database_and_execute("SELECT * FROM aulas_por_curso WHERE id_aula = ?",[id_aula])
        id_curso = dados_aula[0]['id_curso']

        await send_message_or_edit_last(text=f"Titulo da aula:\n{dados_aula[0]['titulo']}\n\nDescrição:\n{dados_aula[0]['descricao']}\n\nLinks extras:\n{dados_aula[0]['links']}",buttons=[
            [
                NossoInlineKeyboardButton(text="editar titulo",callback=EditarTituloAula(id_aula))
            ],
            [
                NossoInlineKeyboardButton(text="editar descrição",callback=EditarDescricaoAula(id_aula))
            ],
            [
                NossoInlineKeyboardButton(text="editar links",callback=EditarLinksAula(id_aula))
            ],
            [
                NossoInlineKeyboardButton(text="remover aula",callback=RemoverAula(id_aula))
            ],
            [
                NossoInlineKeyboardButton(text="voltar",callback=VerAulas(id_curso))
            ]
        ])

        return await VerAulaEspecifica.lida_callback(update,context,id_aula)
    
# Edição Aulas

class EditandoTituloAula(EstadoDoUsuario):
    async def lida_com_mensagem(self, update: Update, context: ContextTypes.DEFAULT_TYPE):

        call_database_and_execute("UPDATE aulas_por_curso SET titulo = ? WHERE id_aula = ?",[update.effective_message.text,context.user_data["id_aula"]])

        await send_message_on_new_block("Título atualizado!")


        return await VerAulaEspecifica.lida_callback(update,context,context.user_data['id_aula'])
    
class EditandoDescricaoAula(EstadoDoUsuario):
    async def lida_com_mensagem(self, update: Update, context: ContextTypes.DEFAULT_TYPE):

        call_database_and_execute("UPDATE aulas_por_curso SET descricao = ? WHERE id_aula = ?",[update.effective_message.text,context.user_data["id_aula"]])

        await send_message_on_new_block("Descrição atualizada!")

        return await VerAulaEspecifica.lida_callback(update,context,context.user_data['id_aula'])

class EditandoLinksAula(EstadoDoUsuario):
    async def lida_com_mensagem(self, update: Update, context: ContextTypes.DEFAULT_TYPE):

        call_database_and_execute("UPDATE aulas_por_curso SET links = ? WHERE id_aula = ?",[update.effective_message.text,context.user_data["id_aula"]])

        await send_message_on_new_block("Links atualizados!")

        return await VerAulaEspecifica.lida_callback(update,context,context.user_data['id_aula'])

class EditarTituloAula(CallbackComDados): 
    async def lida_callback(update: Update, context: ContextTypes.DEFAULT_TYPE, id_aula):
        context.user_data['id_aula'] = id_aula
        set_estado_do_usuario(update.effective_chat.id,EditandoTituloAula())
        return await send_message_on_new_block("Me diga o título que você deseja colocar...",buttons=[
            [
                NossoInlineKeyboardButton("voltar",VerAulaEspecifica(context.user_data['id_aula']))
            ]
        ])


class EditarDescricaoAula(CallbackComDados):
    async def lida_callback(update: Update, context: ContextTypes.DEFAULT_TYPE, id_aula):
        context.user_data['id_aula'] = id_aula
        set_estado_do_usuario(update.effective_chat.id,EditandoDescricaoAula())
        return await send_message_on_new_block("Me diga a descrição que você deseja colocar...",buttons=[
            [
                NossoInlineKeyboardButton("voltar",VerAulaEspecifica(context.user_data['id_aula']))
            ]
        ])

class EditarLinksAula(CallbackComDados):
    async def lida_callback(update: Update, context: ContextTypes.DEFAULT_TYPE, id_aula):
        context.user_data['id_aula'] = id_aula
        set_estado_do_usuario(update.effective_chat.id,EditandoLinksAula())
        return await send_message_on_new_block("Me diga o(s) link(s) que você deseja colocar...\n\n*Eles serão posicionados embaixo da descrição da aula",buttons=[
            [
                NossoInlineKeyboardButton("voltar",VerAulaEspecifica(context.user_data['id_aula']))
            ]
        ])

class RemoverAula(CallbackComDados):
    async def lida_callback(update: Update, context: ContextTypes.DEFAULT_TYPE, id_aula):
        
        id_curso = call_database_and_execute("SELECT id_curso FROM aulas_por_curso WHERE id_aula = ?",[id_aula])[0]['id_curso']

        call_database_and_execute("DELETE FROM aulas_por_curso WHERE id_aula = ?",[id_aula])

        await VerAulas.lida_callback(update,context,id_curso)

class VerAulasCompletas(CallbackComDados):
    async def lida_callback(update: Update, context: ContextTypes.DEFAULT_TYPE, id_curso):
        #return await super().lida_callback(context, *dados)
        
        pass


