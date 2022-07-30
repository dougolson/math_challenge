import sqlite3
from turtle import st
from user import User

class StatReportRecord:

    def __init__(self, data: list) -> None:
        self.user_name = data[0]
        self.question_id = data[1]
        self.answer_time = data[2]
        self.user_answer = data[3]
        self.is_correct_ans = [True, False][data[4]=='false']
        self.date = data[5]
        self.count = data[6]
        self.operation = data[7]
        self.operand1 = data[8]
        self.operand2 = data[9]
        self.answer = data[10]

    def display_record(self):
        print(f"user_name: {self.user_name};\
  question_id: {self.question_id};\
  answer_time: {self.answer_time:.2f};\
  user_answer: {self.user_answer};\
  is_correct_ans: {self.is_correct_ans};\
  count: {self.count};\
  date: {self.date};\
  operation: {self.operation};\
  operand1: {self.operand1};\
  operand2: {self.operand2};\
  answer: {self.answer}")

class StatsReportData:
    query_start = '''SELECT 
            users.user_name,
            s.question_id,
            s.answer_time,
            s.user_answer,
            s.is_correct_ans,
            s.date,
            0 count,
            ap.operation,
            ap.operand1,
            ap.operand2,
            ap.answer
            FROM stats s 
            INNER JOIN arithmetic_problems ap ON s.question_id = ap.id 
            INNER JOIN users on users.id = s.user_id '''

    @classmethod
    def get_by_user_name(self, user) -> list[StatReportRecord]:
        query =  self.query_start + '''WHERE users.user_name = ?'''
        with (sqlite3.connect('math_challenge.db')) as con:
            cur = con.cursor()
            cur.execute(query, (user,))
            data = cur.fetchall()
            result = [StatReportRecord(record) for record in data]
            return result

    @classmethod
    def get_by_user_id(self, id:int) -> list[StatReportRecord]:
        query =  self.query_start + '''WHERE users.id = ?'''
        with (sqlite3.connect('math_challenge.db')) as con:
            cur = con.cursor()
            cur.execute(query, (id,))
            data = cur.fetchall()
            result = [StatReportRecord(record) for record in data]
            return result

    @classmethod
    def get_all(self) -> list[StatReportRecord]:
        query = self.query_start
        with (sqlite3.connect('math_challenge.db')) as con:
            cur = con.cursor()
            cur.execute(query)
            data = cur.fetchall()
            result = [StatReportRecord(x) for x in data]
            return result

    @classmethod
    def get_by_question_id(self, question_id) -> list[StatReportRecord]:
        query = self.query_start + '''WHERE s.question_id = ?'''
        with (sqlite3.connect('math_challenge.db')) as con:
            cur = con.cursor()
            cur.execute(query, (question_id,))
            data = cur.fetchall()
            result = [StatReportRecord(x) for x in data]
            return result

    @classmethod
    def get_by_answer_date(self, answer_date)-> list[StatReportRecord]:
        query = self.query_start + ''' WHERE s.date = ?'''
        with (sqlite3.connect('math_challenge.db')) as con:
            cur = con.cursor()
            cur.execute(query, (answer_date,))
            data = cur.fetchall()
            result = [StatReportRecord(x) for x in data]
            return result

    @classmethod
    def get_by_answer_date_range(self, start_date, end_date)-> list[StatReportRecord]:
        query = self.query_start + ''' WHERE s.date BETWEEN ? AND ?'''
        with (sqlite3.connect('math_challenge.db')) as con:
            cur = con.cursor()
            cur.execute(query, (start_date, end_date))
            data = cur.fetchall()
            result = [StatReportRecord(x) for x in data]
            return result
    
    @classmethod
    def get_summary_by_user_name(self, user:str) -> list[StatReportRecord]:
        query = '''SELECT 
                    usr.user_name,
                    s.question_id,
                    ROUND(AVG(s.answer_time),2) answer_time,
                    0 user_answer,
                    s.is_correct_ans,
                    '' date,    
                    COUNT(1) count,
                    ap.operation,
                    ap.operand1,
                    ap.operand2,
                    ap.answer
                    FROM stats s 
                    INNER JOIN arithmetic_problems ap ON s.question_id = ap.id 
                    INNER JOIN users usr on usr.id = s.user_id
                    WHERE usr.user_name = ?
                    GROUP BY usr.user_name,
                    s.question_id,
                    s.is_correct_ans,
                    ap.operation,
                    ap.operand1,
                    ap.operand2,
                    ap.answer
                    '''
        with (sqlite3.connect('math_challenge.db')) as con:
            cur = con.cursor()
            cur.execute(query, (user,))
            data = cur.fetchall()
            result = [StatReportRecord(x) for x in data]
            return result   

class StatsAnalysis:
    def __init__(self, data:list[StatReportRecord]) -> None:
        self.data = data
        self.operations = {'addition':'+', 'subtraction':'-', 'multiplication':'x', 'division':'/'}
        self.summary_per_question = self.get_summary_per_question()
        self.sorted_by_incorrect_attempts: list[dict] = None
        self.sorted_correct_by_time_spent: list[dict] = None
        self.sorted_incorrect_by_time_spent: list[dict] = None
        self.sorted_by_total_time_spent: list[dict] = None
        self.get_various_stats()

    def get_summary_per_question(self) -> dict[dict]:
        result = {}
        for data_record in self.data:
            q_id = data_record.question_id
            p_time = data_record.answer_time
            is_correct_ans = data_record.is_correct_ans
            if q_id not in result.keys():
                if is_correct_ans:
                    result[q_id] = {'total_time':p_time, 'p_time_correct': p_time,'p_time_incorrect':0, 'correct_attempts': 1, 'incorrect_attempts':0, 'total_attempts':1}
                else:
                    result[q_id] = {'total_time':p_time, 'p_time_correct': 0,'p_time_incorrect':p_time,'correct_attempts': 0, 'incorrect_attempts':1,'total_attempts':1}
                result[q_id]['operation'] = data_record.operation
                result[q_id]['operand1'] = data_record.operand1
                result[q_id]['operand2'] = data_record.operand2
            else:
                if is_correct_ans:
                    result[q_id]['p_time_correct'] += p_time
                    result[q_id]['correct_attempts'] += 1
                else:
                    result[q_id]['p_time_incorrect'] += p_time
                    result[q_id]['incorrect_attempts'] += 1
                result[q_id]['total_time'] += p_time
                result[q_id]['total_attempts'] += 1
        for k, _ in result.items():
            if result[k]['p_time_correct'] == 0 or result[k]['correct_attempts'] == 0: 
                result[k]['avg_time_correct'] = 0
            else:
                result[k]['avg_time_correct'] = result[k]['p_time_correct'] / result[k]['correct_attempts']
            if result[k]['p_time_incorrect'] == 0 or result[k]['incorrect_attempts'] == 0:
                result[k]['avg_time_incorrect'] = 0
            else:
                result[k]['avg_time_incorrect'] = result[k]['p_time_incorrect'] / result[k]['incorrect_attempts']
            if result[k]['total_time'] == 0 or result[k]['total_attempts'] == 0:
                result[k]['avg_time_total'] = 0
            else:
                result[k]['avg_time_total'] = result[k]['total_time'] / result[k]['total_attempts']
        return result
    
    def print_summary_per_question(self):
        if self.summary_per_question is not None:
            for key, inner_dict in self.summary_per_question.items():
                print(f"{key}:")
                for key, val in inner_dict.items():
                    print(f"  {key}: {val:.2f}")
    
    def print_top_3_incorrect_by_time(self):
        if self.sorted_incorrect_by_time_spent is not None:
            print("Here are the questions you spent the longest time trying to answer:")
            count = 0
            while count < 3:
                try:
                    top_question = self.sorted_incorrect_by_time_spent.pop(-1)
                    q_data = top_question[1]
                    print(f"  Question: {q_data['operand1']} {self.operations[q_data['operation']]} {q_data['operand2']} = ?")
                    print(f"    time spent: {q_data['avg_time_incorrect']:.2f}")
                    count += 1
                except:
                    break
        return

    def print_top_3_incorrect_by_attempts(self):
        if self.sorted_by_incorrect_attempts is not None:
            print("Here are the questions you answered incorrectly most often:")
            count = 0
            while count < 3:
                try:
                    top_3 = self.sorted_by_incorrect_attempts.pop(-1)
                    q_data = top_3[1]
                    print(f"  Question: {q_data['operand1']} {self.operations[q_data['operation']]} {q_data['operand2']} = ?")
                    print(f"    Answered incorrectly: {q_data['incorrect_attempts']} times.")
                    count += 1
                except:
                    break
        return

    # def print_top_3_incorrect_by_time_spent_XXX(self):
    #     if self.summary_per_question is not None:
    #         for key, inner_dict in self.summary_per_question.items():
    #             print(f"  {key}:")
    #             for key, val in inner_dict.items():
    #                 print(f"    {key}: {val:.2f}")

    # def print_top_3_total_time_spent(self):
    #     if self.summary_per_question is not None:
    #         for key, inner_dict in self.summary_per_question.items():
    #             print(f"{key}:")
    #             for key, val in inner_dict.items():
    #                 print(f"  {key}: {val:.2f}")

    
    def get_various_stats(self):
        self.sorted_by_incorrect_attempts = sorted(self.summary_per_question.items(), key=lambda x:x[1]['incorrect_attempts'])
        self.sorted_correct_by_time_spent = sorted(self.summary_per_question.items(), key=lambda x:x[1]['avg_time_correct'])
        self.sorted_by_total_time_spent = sorted(self.summary_per_question.items(), key=lambda x:x[1]['avg_time_total'])
        self.sorted_incorrect_by_time_spent = sorted(self.summary_per_question.items(), key=lambda x:x[1]['avg_time_incorrect'])

    
    


if __name__=='__main__':
    # print(get_data(query, 'Doug'))
    
    # data = StatsReport.get_by_user_name('test_user')
    # data = StatsReport.get_all()
    # data = StatsReport.get_by_answer_date('2022-07-28')
    # data = StatsReport.get_by_answer_date_range('2022-07-26', '2022-07-28')
    # data = StatsReport.get_by_answer_date_range('2022-07-25', '2022-07-26')
    # data = StatsReport.get_by_question_id(5245)

    # data = StatsReportData.get_by_user_name('test_user')
    data = StatsReportData.get_by_user_id(4)
    summary = StatsAnalysis(data)
    # summary.print_summary_per_question()
    summary.print_top_3_incorrect_by_time()
    summary.print_top_3_incorrect_by_attempts()
    # for stats_report_record in data:
    #     stats_report_record.display_record()
    # stats = StatsAnalysis(data)
    # summary = stats.summary_per_question
    # for outer_key, outer_val in summary.items():
    #     for inner_key, inner_val in outer_val.items():
    #         print(f"{inner_key} : {inner_val}")
    # for item in data:
    #     print(f"{item[0]} {item[1]:5} {item[2]:5} {item[3]:15} {item[4]} {item[5]}")
    # result = stats.summary_per_question
    # stats.get_various_stats()
    # print(stats.sorted_by_incorrect_attempts[-3:])
    # print(stats.sorted_correct_by_time_spent[-3:])
    # print(stats.sorted_incorrect_by_time_spent[-3:])
    # print(result)
    # StatsAnalysis.print_dict_of_dicts(result)
    # stats.print_dict_of_dict()
    # data = DataRecords.get_user_summary('Bob')
    # data = DataRecords.get_all()
    # data = DataRecords.get_by_question_id(100)
    # data = DataRecords.get_by_answer_date('2022-07-23')
    # data = DataRecords.get_by_answer_date('2022-07-24')
    # data = DataRecords.get_by_answer_date_range('2022-07-23', '2022-07-24')
    # print(f"The length of this data is {len(data)}")
    # for data_record in data:
    #     # print(data_record)
    #     data_record.display_record()
    # record = DataRecord(data)
    # record.display_record()
    # display_record(data)
    