
from geral import *
from callback_com_dados import *
from callback_sem_dados import *



class TesteCallback(CallbackComDados):
    k = "a"
    def __init__(self, dados):
        super().__init__(dados)

    def lida_callback(update: Update, context: ContextTypes.DEFAULT_TYPE, dados):
        TesteCallback.k = "b"

class TesteCallbackSemDados(CallbackSemDados):

    def lida_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
        pass

def teste_callback_com_dados():
    callback = TesteCallback(2)

    assert callback.get_dados() == 2

def teste_callback_sem_dados():

    callback = TesteCallbackSemDados()

    assert callback.get_callback_str() == "TesteCallbackSemDados"


def teste_callback_com_dados_str():

    callback = TesteCallback(2)
    assert callback.get_callback_str() == f"TesteCallback {2}"

def teste_callback_com_dados_lida_callback():
    callback = TesteCallback(2)
    assert TesteCallback.k == "a"

    callback.lida_callback(Update(12),ContextTypes.DEFAULT_TYPE)

    assert TesteCallback.k == "b"




