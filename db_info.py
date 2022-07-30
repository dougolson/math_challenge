import sqlite3

def get_column_names(table_name):
    query = f"PRAGMA table_info({table_name})"
    with (sqlite3.connect('math_challenge.db')) as con:
                cur = con.cursor()
                cur.execute(query)
                data = cur.fetchall()
                for item in data:
                    print(item[1])

def get_table_info(table_name):
    query = f"PRAGMA table_info({table_name})"
    with (sqlite3.connect('math_challenge.db')) as con:
                cur = con.cursor()
                cur.execute(query)
                data = cur.fetchall()
                lengths = [0] * len(data)
                for item in data:
                    idx = 0
                    for sub in item:
                        if len(str(sub)) > lengths[idx]:
                            lengths[idx] = len(str(sub))
                        idx += 1
                for n, item in enumerate(data):
                    print(f"col_name: {item[1]:{lengths[1]}}  type: {item[2]:{lengths[2]}}   nullable: {item[3]:{lengths[3]}}  pk: {item[5]:{lengths[5]}}")

def word_box(word:str)->None:
    word_len = len(word)
    line = f"{'=' * (len(word) + 4)}"
    word_str = f"= {word} ="
    print('\n' + line)
    print(word_str)
    print(line)


if __name__=='__main__':
    table_names = ['users','arithmetic_problems','stats']
    for table_name in table_names:
        word_box('columns')
        get_column_names(table_name)
        # word_box('table info')
        # get_table_info(table_name)
