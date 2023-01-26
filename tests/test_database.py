from geral import *



def test_database_usage_function():

    call_database_and_execute("""DROP TABLE IF EXISTS test_db""")

    call_database_and_execute("""CREATE TABLE IF NOT EXISTS test_db (
        teste_dado_1 INTEGER,
        teste_dado_2 TEXT
    )""")

    call_database_and_execute("INSERT INTO test_db (teste_dado_1,teste_dado_2) VALUES (?,?)",[2,"abacate"])

    db_data = call_database_and_execute("SELECT * FROM test_db")

    assert len(db_data) == 1

    db_data_2 = call_database_and_execute("SELECT * FROM test_db WHERE teste_dado_2 = ?",["abacate"])

    assert len(db_data_2) == 1
    assert db_data_2[0]["teste_dado_1"] == 2


