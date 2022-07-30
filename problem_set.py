import sqlite3
from question import Question

def get_problem_set(operation, mn, mx) -> list[Question]:
    func_choice = {
        'addition':get_by_operation_and_operand_range,
        'subtraction':get_by_operation_and_operand_answer_range,
        'multiplication':get_by_operation_and_operand_range,
        'division':get_by_operation_and_operand_answer_range
        }
    return func_choice[operation](operation, mn, mx)  
       
def get_by_operation_and_operand_range(operation, mn, mx) -> list[Question]:
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
    
def get_by_operation_and_operand_answer_range(operation, mn, mx) -> list[Question]:
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
    smallest, largest = 3, 25
    data = get_problem_set('addition', 5, 7)
    for item in data:
        item.print_question()