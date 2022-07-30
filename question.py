import sqlite3

class Question:
    def __init__(self, id:int, operation:str, operand1:int, operand2:int, answer:int) -> None:
        self.id = id
        self.operation = operation
        self.operand1 = operand1
        self.operand2 = operand2
        self.answer = answer
    
    def print_question(self):
        question_string = f"Question:\n\tid: {self.id}\n\toperation: {self.operation}\n\toperand1: {self.operand1}\n\toperand2: {self.operand2}\n\tanswer: {self.answer}"
        print(question_string)

def get_by_id(id) -> Question:
    query = '''SELECT id, operation, operand1, operand2, answer FROM arithmetic_problems WHERE id = ?'''
    with (sqlite3.connect('math_challenge.db')) as con:
        cur = con.cursor()
        cur.execute(query, (id,))
        data = cur.fetchone()
        result = Question(*data)
        return result

def get_by_operation(operation) -> list[Question]:
    query = '''SELECT id, operation, operand1, operand2, answer FROM arithmetic_problems WHERE operation = ?'''
    with (sqlite3.connect('math_challenge.db')) as con:
        cur = con.cursor()
        cur.execute(query, (operation,))
        data = cur.fetchall()
        result = [Question(*x) for x in data]
        return result

if __name__=='__main__':
    q = get_by_id(5000)
    print("\n=========================")
    q.print_question()
    q_set = get_by_operation('division')
    print(f"\nlen(q_set) = {len(q_set)}\n")
    q_set[0].print_question()
    q_set[-1].print_question()
    print("=========================\n")