import sqlite3

class StatRecord:
    def __init__(self, user_id, question_id, answer_time, user_answer, is_correct_ans, date) -> None:
        self.user_id = user_id
        self.question_id = question_id
        self.answer_time = answer_time
        self.user_answer = user_answer
        self.is_correct_ans = is_correct_ans
        self.date = date

query = '''INSERT INTO stats (user_id, question_id, answer_time, user_answer, is_correct_ans, date) VALUES(?,?,?,?,?,?);'''

def save_stats_to_db(stat_record):
    values = [stat_record.user_id, stat_record.question_id, stat_record.answer_time, stat_record.user_answer, stat_record.is_correct_ans, stat_record.date]
    with (sqlite3.connect('math_challenge.db')) as con:
        cur = con.cursor()
        cur.execute(query, values)
        con.commit()