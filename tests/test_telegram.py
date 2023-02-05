from geral import *
from all import inicia_bot
import pytest
import asyncio as a

BOTE_TESTS_TOKEN = "5666314930:AAENO8ook7pmT3u9dP_x8wPE03_wWMhdnFM"

BOTEZINHO_TESTS_TOKEN = "5768246642:AAGNaoBYQcR7O0p7aNCyA_tBX0sUw5ps2pE"

TESTES_CHAT_ID = -605298131

#todos os testes desse arquivo devem primeiro chamar inicia bot
def test_cria_processo():
    processo_cursos,processo_alunos = inicia_bot(BOTEZINHO_TESTS_TOKEN,BOTE_TESTS_TOKEN)

    assert processo_cursos.is_alive()
    assert processo_alunos.is_alive()

    processo_alunos.terminate()
    processo_cursos.terminate()

@pytest.mark.asyncio
async def test_manda_start_bote():
    processo_cursos,processo_alunos = inicia_bot(BOTEZINHO_TESTS_TOKEN,BOTE_TESTS_TOKEN)
    
    
    botezinho = telegram.Bot(BOTEZINHO_TESTS_TOKEN)
    bote = telegram.Bot(BOTE_TESTS_TOKEN)
    await botezinho.initialize()
    await bote.initialize()
    message = await botezinho.send_message(TESTES_CHAT_ID,"@bote_tests_bot /start")

    chat = await bote.get_chat(message.chat_id)

    await a.sleep(5)

