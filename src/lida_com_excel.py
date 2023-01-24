

import pandas as pd
import os
from geral import *
import time


def lida_com_arquivo_excel(path):

    file = pd.read_excel(path)
    expected = ["TITULO","DESCRICAO","LINK"]
    test_expected = lambda x: [x[:len(i)] in expected for i in expected]

    dictionary = {}
    for column in file:
        titulo = column.title().upper().strip()
        if not any(test_expected(titulo)):
            if not any(test_expected(file[column][0])):   
                return None,False
            titulo = file[column][0]
        dictionary[titulo] = []
        for row in file[column]:
            if row == titulo:
                continue
            dictionary[titulo].append(row)
    
    rows = []
    for i in range(len(dictionary['TITULO'])):
        v = {}
        for key in dictionary.keys():
            v[key] = dictionary[key][i]
        rows.append(v)

    return rows,True
    