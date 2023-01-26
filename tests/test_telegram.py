from geral import *
from all import inicia_bot


BOTE_TESTS_TOKEN = "5666314930:AAENO8ook7pmT3u9dP_x8wPE03_wWMhdnFM"

BOTEZINHO_TESTS_TOKEN = "5768246642:AAGNaoBYQcR7O0p7aNCyA_tBX0sUw5ps2pE"


def test_cria_processo():
    processo_cursos,processo_alunos = inicia_bot(BOTEZINHO_TESTS_TOKEN,BOTE_TESTS_TOKEN)

    assert processo_cursos.is_alive()
    assert processo_alunos.is_alive()

    processo_alunos.terminate()
    processo_cursos.terminate()




