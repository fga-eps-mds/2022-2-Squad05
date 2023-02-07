from geral import *
from app import inicia_bot
from bot_cursos import start as bot_cursos_start
import pytest
import asyncio as a
from cursos import *
import time
from datetime import datetime

import pytest

from telegram import (
    CallbackQuery,
    Chat,
    ChatJoinRequest,
    ChatMemberOwner,
    ChatMemberUpdated,
    ChosenInlineResult,
    InlineQuery,
    Message,
    Poll,
    PollAnswer,
    PollOption,
    PreCheckoutQuery,
    ShippingQuery,
    Update,
    User,
)

BOTE_TESTS_TOKEN = "5666314930:AAENO8ook7pmT3u9dP_x8wPE03_wWMhdnFM"

BOTEZINHO_TESTS_TOKEN = "5768246642:AAGNaoBYQcR7O0p7aNCyA_tBX0sUw5ps2pE"

TESTES_CHAT_ID = -605298131

from telegram._utils.datetime import from_timestamp

#todos os testes desse arquivo devem primeiro chamar inicia bot
def test_cria_processo():
    processo_cursos,processo_alunos = inicia_bot(BOTEZINHO_TESTS_TOKEN,BOTE_TESTS_TOKEN)

    assert processo_cursos.is_alive()
    assert processo_alunos.is_alive()

    processo_alunos.terminate()
    processo_cursos.terminate()
