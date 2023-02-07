import multiprocessing
import os
import subprocess


from src.geral import call_database_and_execute




def inicia_bot(bot_token_alunos = None,bot_token_cursos=None):


    cursos_process = multiprocessing.Process(
        target=subprocess.run,
        kwargs={
            'args': f'python src/bot_cursos.py {f"--bot-token {bot_token_cursos}" if bot_token_cursos != None else ""}',
            'shell': True

        })


    alunos_process= multiprocessing.Process(
        target=subprocess.run,
        kwargs={
            'args': f'python src/bot_alunos.py {f"--bot-token {bot_token_alunos}" if bot_token_alunos != None else ""}',
            'shell': True
        })

    if not os.path.exists("database.db"):
        #criando o banco de dados caso não exista ainda
        call_database_and_execute("""
        CREATE TABLE IF NOT EXISTS users (
            id_user INTEGER PRIMARY KEY
        )""")

        call_database_and_execute("""
        CREATE TABLE IF NOT EXISTS cursos (
            nome TEXT,
            descricao TEXT,
            id_dono INTEGER,
            hash_senha TEXT,
            id TEXT
        )""")

        call_database_and_execute("""
        CREATE TABLE IF NOT EXISTS aulas_por_curso (
            id_aula TEXT,
            id_curso TEXT,
            titulo TEXT,
            descricao TEXT,
            links TEXT
        )""")

        call_database_and_execute("""
        CREATE TABLE IF NOT EXISTS aulas_por_aluno (
            id_aula TEXT,
            id_aluno INTEGER,
            id_curso TEXT
        )""")

        call_database_and_execute("""
        CREATE TABLE IF NOT EXISTS alunos_por_curso (
            id_aluno INTEGER,
            id_curso TEXT
        )""")

    cursos_process.start()
    alunos_process.start()

    return cursos_process,alunos_process
    
if __name__ == "__main__":

    inicia_bot()