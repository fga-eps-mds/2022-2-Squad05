from geral import *
from callback_sem_dados import *


class NaoPossuiCodigo(CallbackSemDados):
    async def lida_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):

        await send_message_or_edit_last(update,context,text="Esse código é o id do curso em que você deseja entrar.\n\nPara obte-lo, solicite-o ao dono do curso.")

        return await super().lida_callback(context)