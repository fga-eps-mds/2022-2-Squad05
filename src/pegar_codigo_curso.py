from geral import *
from callback_sem_dados import *
from nosso_inline_keyboard_button import *
from nao_possui_codigo import *
from entrando_em_curso import *

class PegarCodigoCurso(CallbackSemDados):
    async def lida_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):

        await send_message_or_edit_last(update,context,text="Ok. Por favor me diga o código do curso que você deseja entrar...",buttons=[
            [
                NossoInlineKeyboardButton(text="não tenho código",callback=NaoPossuiCodigo())
            ]
        ])

        set_estado_do_usuario(update.effective_chat.id,EntrandoEmCurso())

        return await super().lida_callback(context)