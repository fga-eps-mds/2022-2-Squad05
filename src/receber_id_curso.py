
from callback_com_dados import CallbackComDados
from telegram import Update
from telegram.ext import ContextTypes
from geral import *


class ReceberIdCurso(CallbackComDados):
    async def lida_callback(update: Update, context: ContextTypes.DEFAULT_TYPE, dados):
        
        await context.bot.send_message(chat_id=update.effective_chat.id,text=dados)

        return await CallbackComDados.lida_callback(update,context,dados)
