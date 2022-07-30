import sqlite3

class Question:
    def __init__(self, id:int, operation:str, operand1:int, operand2:int, answer:int) -> None:
        self.id = id
        self.operation = operation
        self.operand1 = operand1
        self.operand2 = operand2
        self.answer = answer
    
    def print_question(self):
        question_string = f"Question:\n\tid: {self.id}\n\toperation: {self.operation}\n\toperand1: {self.operand1}\n\toperand2: {self.operand2}\n\answer: {self.answer}"
        print(question_string)

class QuestionData:
    @classmethod    
    def get_by_id(self, id) -> Question:
        query = '''SELECT id, operation, operand1, operand2, answer FROM arithmetic_problems WHERE id = ?'''
        with (sqlite3.connect('math_challenge.db')) as con:
            cur = con.cursor()
            cur.execute(query, (id,))
            data = cur.fetchone()
            result = Question(*data)
            return result
    
    @classmethod    
    def get_by_operation(self, operation) -> list[Question]:
        query = '''SELECT id, operation, operand1, operand2, answer FROM arithmetic_problems WHERE operation = ?'''
        with (sqlite3.connect('math_challenge.db')) as con:
            cur = con.cursor()
            cur.execute(query, (operation,))
            data = cur.fetchall()
            result = [Question(*x) for x in data]
            return result

    @classmethod    
    def get_by_operation_and_operand_range(self, operation, mn, mx) -> list[Question]:
        query = '''SELECT id, operation, operand1, operand2, answer 
                   FROM arithmetic_problems WHERE operation = ?
                   AND operand1 >= ? 
                   AND operand2 <= ?'''
        with (sqlite3.connect('math_challenge.db')) as con:
            cur = con.cursor()
            cur.execute(query, (operation, mn, mx))
            data = cur.fetchall()
            result = [Question(*x) for x in data]
            return result

    @classmethod    
    def get_by_operation_and_operand_answer_range(self, operation, mn, mx) -> list[Question]:
        query = '''SELECT id, operation, operand1, operand2, answer 
                   FROM arithmetic_problems WHERE operation = ?
                   AND operand1 BETWEEN ?  AND ?
                   AND operand2 BETWEEN ?  AND ?
                   AND answer <= ?'''
        with (sqlite3.connect('math_challenge.db')) as con:
            cur = con.cursor()
            cur.execute(query, (operation, mn, mx, mn, mx, mx))
            data = cur.fetchall()
            result = [Question(*x) for x in data]
            return result

if __name__ == '__main__':
    # question = QuestionData.get_by_id(10006)
    # question.print_question()
    # questions = QuestionData.get_by_operation('multiplication')
    # for item in questions:
    #     item.print_question()
    questions = QuestionData.get_by_operation_and_operand_answer_range('subtraction', 3, 12)
    for item in questions:
        item.print_question()
