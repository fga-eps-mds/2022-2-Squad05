
from callback_sem_dados import CallbackSemDados
from telegram import Update
from telegram.ext import ContextTypes
from geral import *

class NaoDesejaCriarCurso(CallbackSemDados):
    def __init__(self) -> None:
        super().__init__()

    async def lida_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):

        """
        função para quando o usuário não deseja criar uma conta ou interagir com o bot agora
        """
        await send_message_or_edit_last(update,context,text="Tudo certo!\n\nQuando quiser utilizar meus serviços digite /start nesse chat e eu virei te ajudar!\n\nTenha um bom dia :D")

        return await CallbackSemDados.lida_callback(update,context)