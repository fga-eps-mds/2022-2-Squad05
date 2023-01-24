from callback_sem_dados import CallbackSemDados
from callback_com_dados import CallbackComDados
from telegram import Update
from telegram.ext import ContextTypes
from geral import *
from ver_aulas import VerAulas
from ver_curso_especifico import VerCursoEspecifico


class RemoverAula(CallbackComDados):
    async def lida_callback(update: Update, context: ContextTypes.DEFAULT_TYPE, dados):
        
        id_curso,id_aula = dados.split(',')
        call_database_and_execute("DELETE FROM aulas_por_curso WHERE aula_id = ?",[id_aula])

        await VerCursoEspecifico.lida_callback(update,context,id_curso)
        

