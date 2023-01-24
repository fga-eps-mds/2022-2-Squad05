

from geral import *
from lida_com_excel import lida_com_arquivo_excel


def test_arquivo_excel_bom():

    arquivo_teste = "teste.xlsx"

    rows,conseguiu = lida_com_arquivo_excel(arquivo_teste)
    
    assert conseguiu
    assert rows[0]["TITULO"] == "Aula 1"
    assert rows[0]["LINK"] == 'https://pt.wikipedia.org/wiki/Banana'

    
