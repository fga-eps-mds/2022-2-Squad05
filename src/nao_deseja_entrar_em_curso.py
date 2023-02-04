from geral import *
from callback_sem_dados import *


class NaoDesejaEntrarEmCurso(CallbackSemDados):
    async def lida_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
        
        await send_message_or_edit_last(update,context,text="Tudo certo! Se precisar de mim, só mandar uma mensagem com /start nesse chat e eu virei te ajudar!")

        return await super().lida_callback(context)