from geral import *
from callback_com_dados import *
from nosso_inline_keyboard_button import *

class MenuPrincipal(CallbackComDados):

    def __init__(self, message):
        if message == "":
            print('message is now ;')
            message = ";"
        super().__init__(message)

    async def lida_callback(update: Update, context: ContextTypes.DEFAULT_TYPE,message):

        numero_de_cursos = call_database_and_execute("SELECT COUNT(*) FROM cursos WHERE id_dono = ?",[update.effective_chat.id])[0]
        buttons = [
                [
                NossoInlineKeyboardButton(text="criar novo curso",callback="CriarCurso"),
                ]
            ]
        print(numero_de_cursos["COUNT(*)"])
        if numero_de_cursos["COUNT(*)"] > 0:
            buttons.append([
                    NossoInlineKeyboardButton(text='ver seus cursos',callback="VerCursos")
            ])


        return await send_message_or_edit_last(text=message + "Como posso ajudar hoje?",buttons=buttons)



