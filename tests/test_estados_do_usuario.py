

import os
import sys
import importlib

from telegram import Update
from callback import Callback,import_all_callbacks
import inspect
from telegram.ext import ContextTypes
from estados_do_usuario import EstadoDoUsuario,set_estado_do_usuario,make_sure_estado_is_init,lida_com_todos_os_estados_do_usuario,get_estados_dos_usuarios,clear_estados_dos_usuarios

import pytest


def test_estados_do_usuario_1():

    assert len(get_estados_dos_usuarios()) == 0

    set_estado_do_usuario(22342,EstadoDoUsuario())

    assert len(get_estados_dos_usuarios()) == 1

    

    
def test_estados_do_usuario_clear():
    get_estados_dos_usuarios().clear()
    assert len(get_estados_dos_usuarios()) == 0

    set_estado_do_usuario(22342,EstadoDoUsuario())

    assert len(get_estados_dos_usuarios()) == 1

    clear_estados_dos_usuarios()

    assert len(get_estados_dos_usuarios()) == 0




class EstadoQualquer(EstadoDoUsuario):
    k = 0

    def lida_com_mensagem(self, update: Update, context: ContextTypes.DEFAULT_TYPE):

        EstadoQualquer.k = 1

        return super().lida_com_mensagem(update, context)

@pytest.mark.asyncio
async def test_estados_do_usuario_2():

    assert len(get_estados_dos_usuarios()) == 0
    assert EstadoQualquer.k == 0

    set_estado_do_usuario("22323",EstadoQualquer())

    assert len(get_estados_dos_usuarios()) == 1
    assert EstadoQualquer.k == 0

    await get_estados_dos_usuarios()["22323"].lida_com_mensagem(Update(2),ContextTypes.DEFAULT_TYPE)


    assert EstadoQualquer.k == 1

    clear_estados_dos_usuarios()
