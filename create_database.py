import csv
import sqlite3

# generate csv data
def generate_all_data(mn=2, mx=100):
    add = []
    mult = []
    result = []
    prob_rng = range(mn, mx + 1)

    # generate addition data
    for m in prob_rng:
        for n in prob_rng:
            if n >= m:
                tmp = ('addition', m, n, m+n)
                add.append(tmp)
                result.append(tmp)

    # generate multiplication data
    for m in prob_rng:
        for n in prob_rng:
            if n >= m:
                tmp = ('multiplication', m, n, m * n)
                mult.append(tmp)
                result.append(tmp)

    # generate subtraction data
    for item in add:
        tmp = ('subtraction',item[3], item[2], item[1])
        result.append(tmp)

    # generate division data
    for item in mult:
        tmp = ('division',item[3], item[2], item[1])
        result.append(tmp)
    return result

def reset_database():
    # open connection
    con =sqlite3.connect('math_challenge.db')
    cur = con.cursor()

    # Drop tables if they exist
    cur.execute('''DROP TABLE IF EXISTS users''')
    cur.execute('''DROP TABLE IF EXISTS stats''')
    cur.execute('''DROP TABLE IF EXISTS arithmetic_problems''')

    # create and load users table
    cur.execute('''CREATE TABLE users 
                (
                    id INTEGER PRIMARY KEY NOT NULL,
                    user_name TEXT NOT NULL
                );''') 
    cur.executemany('''INSERT INTO users (user_name) VALUES(?)''', [('lars',), ('lena',),('lucy',),('test_user',)])
    con.commit()

    # create and load arithmetic_problems table
    cur.execute('''CREATE TABLE arithmetic_problems 
                (
                    id INTEGER PRIMARY KEY NOT NULL,
                    operation TEXT NOT NULL,
                    operand1 INTEGER NOT NULL,
                    operand2 INTEGER NOT NULL,
                    answer INTEGER NOT NULL
                );''')
    cur.execute('''CREATE UNIQUE INDEX IDX_Arithmetic_Probems ON arithmetic_problems (operation, operand1, operand2, answer)''') 

    data_to_db = generate_all_data()
    cur.executemany("INSERT INTO arithmetic_problems (operation,operand1,operand2,answer) VALUES (?, ?, ?, ?);", data_to_db)
    con.commit()

    # create stats table
    cur.execute('''CREATE TABLE stats 
                (
                    id INTEGER PRIMARY KEY NOT NULL,
                    user_id INTEGER NOT NULL,
                    question_id INTEGER NOT NULL,
                    answer_time REAL NOT NULL,
                    user_answer INTEGER NOT NULL,
                    is_correct_ans TEXT NOT NULL,
                    date TEXT NOT NULL,
                    FOREIGN KEY(question_id) REFERENCES arithmetic_problems(id)
                );''') 
    con.commit()
    con.close()

