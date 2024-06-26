# import mysql.connector
# from creditentials import *
# mydb = mysql.connector.connect(
#     host=f"{host}",
#     user=f"{user}",
#     password=f"{password}",
#     port=f"{port}",
#     database=f"{database}"
# )


def read_query(sql: str, sql_params=()):
    cursor = mydb.cursor()
    cursor.execute(sql, sql_params)
    return cursor.fetchall()


def insert_query(sql: str, sql_params=()):
    cursor = mydb.cursor()
    cursor.execute(sql, sql_params)
    mydb.commit()
    return "success"


def update_query(sql: str, sql_params=()):
    cursor = mydb.cursor()
    cursor.execute(sql, sql_params)
    mydb.commit()
    return "success"


def create_table(sql:str):
    cursor = mydb.cursor()
    cursor.execute(sql)
    mydb.commit()
    return "success"