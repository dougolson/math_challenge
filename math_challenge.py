from datetime import datetime
import os
import random
import argparse
import sys
import time
import re
import problem_set as ps
import stat_save as db_save
from stat_save import StatRecord
import user as usr
from user import User
from stats_report import StatsReportData, StatsAnalysis

class TimerError(Exception):

    """A custom exception used to report errors in use of Timer class"""


class MathChallenge():

    def __init__(self):
        self.user:User = None
        self.first_run = True
        self.choice_confirmation = {1: "Addition", 2:"Subtraction", 3:"Multiplication", 4:"Division", 5:"Get Recommendation",6:"Quit"}
        self.operations = ['addition', 'subtraction','multiplication','division']
        self.int_pattern = r'\s*\d+\s*'
        self.negative_int_pattern = r'-\d+'
        self.less_than_two_pattern = r'(-[0-9]+|[0-1])'
        self.float_pattern = r'(-|\+)?\d*\.\d*'
        self.negative_integer_message = "number must be at least 1!"
        self.invalid_choice_message = "Sorry, that isn't a valid choice"
        self.less_than_two_message = "number must be an integer grater than 1"
        self.float_message = "number can't be a decimal"
        self.not_a_number_message = "I don't even know what that is!"
        self.prompt_new_question = "Press Enter for a new question, any other key for the menu\n"
        self.questions_attempted = {'addition':0, 'subtraction':0, 'multiplication':0, 'division':0}
        self.problems_solved = {'addition':0, 'subtraction':0, 'multiplication':0, 'division':0}
        self.answer_time_totals = {'addition':0, 'subtraction':0, 'multiplication':0, 'division':0}
        self.start_time = None
        self.problem_set = None
        self.solved = []
        self.ALL_MIN = 2
        self.ADD_SUB_MAX = 100
        self.MULT_MAX = 100
        self.DIV_MAX = 10000
        self.bounds = {'addition':[self.ALL_MIN, self.ADD_SUB_MAX], 'subtraction':[self.ALL_MIN, self.ADD_SUB_MAX], 'multiplication':[self.ALL_MIN,self.MULT_MAX], 'division':[self.ALL_MIN,self.DIV_MAX]}

    def start_timer(self):
        """Start a new timer"""
        if self.start_time is not None:
            raise TimerError(f"Timer is running. Use .stop() to stop it")
        self.start_time = time.perf_counter()

    def stop_timer(self):
        """Stop the timer, and report the elapsed time"""
        if self.start_time is None:
            raise TimerError(f"Timer is not running. Use .start() to start it")
        elapsed_time = time.perf_counter() - self.start_time
        self.start_time = None
        
        return elapsed_time

    def get_random_number(self, smallest, largest):
        """get a random intger between smallest and largest"""        
        return random.randint(smallest, largest)

    def print_intro_screen(self, user: User):
        """print out a banner"""   
        os.system('clear')
        name = user.user_name.title()     
        banner_string = f"# {name}\'s Math Challenge! #"
        print("\n    Welcome to...   \n")
        spinner = ['+ ','- ','x ','/ ',]
        for i in range(20):
            sys.stdout.write(spinner[i%4])
            sys.stdout.flush()
            time.sleep(0.05)
        print("\n")
        print('  ' + "#" * len(banner_string))
        print('  ' + f"{banner_string}")
        print('  ' + "#" * len(banner_string))

    def print_header(self):
        header_string = f"# {self.user.user_name}\'s Math Challenge! #"
        print('\n\n\n')
        print('\t' + "#" * len(header_string))
        print('\t' + f"{header_string}")
        print('\t' + "#" * len(header_string))
        print('\n\n\n')

    def get_praise(self):
        """get a randomly selected praise statement"""        
        praise = ["Nice!", "Noice!", "Well Done!", "Amazing!", "Fabulous", "Fantastic", "Splendimonious", "Que Bueno!", "You're the Goat!", "Sweet!", "Tasty!"]
        return praise[self.get_random_number(0, len(praise) - 1)]
    
    def get_condolence(self):
        """get a randomly selected condolence statement""" 
        condolence = ["Regrettably", "Sadly", "My condolences", "Such a shame", "Oh what a pity", "Not quite", "Doh!"]
        return condolence[self.get_random_number(0, len(condolence) - 1)]

    def get_confused_response(self):
        """get a randomly selected statement of confusion""" 
        confusion = ["uh, wut?", "I don't understand...", "That didn't make sense...", "It is a tale told by an idiot, full of sound and fury, signifying nothing...", "Fascinating, yet incomprehensible", "Captain... I'm confused", "Sorry, I didn't catch that", "Are you messing with me?", "Doh"]
        return confusion[self.get_random_number(0, len(confusion) - 1)]
    
    def display_recommendations(self):
        data = StatsReportData.get_by_user_id(4)
        summary = StatsAnalysis(data)
        os.system('clear')
        summary.print_top_3_incorrect_by_time()
        summary.print_top_3_incorrect_by_attempts()
        input("Press any key to return to the main menu")
        self.setup()

    def is_valid_string_int(self, string_int:str):
        """is a string a valid representation of an integer
        
        Args:
            string_int (string): a string
        
        Returns:
            boolean: True if valid, else False
        """        
        result = False
        if re.fullmatch(self.int_pattern, string_int):
            result = True
        return result

    def convert_string_int(self, string_int:str):
        """convert a valid string int to an integer
        
        Returns:
            an integer if string can be converted, else None
        """        
        result = None
        if self.is_valid_string_int(string_int):
            result = int(string_int)
        return result
    
    def get_error_message(self, string_int):
        """return various error messages if a string cannot be converted to an integer
        
        Args:
            string_int (string): string representation of an integer
        
        Returns:
            string: an error message
        """        
        if re.match(self.less_than_two_pattern, string_int):
            return f"{self.less_than_two_message}"
        elif re.match(self.float_pattern, string_int):
            return f"{self.float_message}"
        else:
            return f"{self.not_a_number_message}"

    def check_bounds(self, operation:str, smallest:int, largest:int):
        operation = operation.lower()
        if smallest < self.bounds[operation][0]: smallest = self.bounds[operation][0]
        if largest > self.bounds[operation][1]: largest = self.bounds[operation][1]
        return smallest, largest
 
    def get_problem(self, operation:str, smallest:int, largest:int):
        os.system('clear')
        self.print_header()
        operation = operation.lower()
        if self.problem_set is None:
            self.problem_set = ps.get_problem_set(operation, smallest, largest)
            # self.problem_set = self.problem_set_functions[operation](smallest, largest)
            random.shuffle(self.problem_set)
        print(f"{len(self.problem_set)} problems left in set\n")
        if len(self.problem_set) == 0:
            os.system('clear')
            print("You solved them all - nice work!\n")
            self.get_stats()
            self.setup()
        else:
            question = self.problem_set.pop()
        self.start_timer()
        if operation == 'addition':
            response = input(f"{question.operand1} + {question.operand2} = ?\n\n")
            incorrect_msg = f"{self.get_condolence()}, {question.operand1} + {question.operand2} = {question.answer}!"
        elif operation == 'subtraction':
            response = input(f"{question.operand1} - {question.operand2} = ?\n")
            incorrect_msg = f"{self.get_condolence()}, {question.operand1} - {question.operand2} = {question.answer}!"
        elif operation == 'multiplication':
            response = input(f"{question.operand1} x {question.operand2} = ?\n")
            incorrect_msg = f"{self.get_condolence()}, {question.operand1} * {question.operand2} = {question.answer}!"
        elif operation == 'division':
            response = input(f"{question.operand1} / {question.operand2} = ?\n")
            incorrect_msg = f"{self.get_condolence()}, {question.operand1} / {question.operand2} = {question.answer}!"
        else:
            response = ''
        user_answer = self.convert_string_int(response)
        is_correct_ans = 'false'
        if user_answer is not None:
            if user_answer == question.answer:
                is_correct_ans = 'true'
                print(f"\n{self.get_praise()}\n")
                self.problems_solved[operation] += 1
                self.solved.append(question.id)
            else:
                print(incorrect_msg)
                self.problem_set.append(question)
                random.shuffle(self.problem_set)
        else:
            print(f"{self.get_confused_response()}, {self.get_error_message(response)}") 
        answer_time = self.stop_timer()
        print(f"Time spent: {answer_time:.2f}")
        self.answer_time_totals[operation] += answer_time
        self.questions_attempted[operation] += 1 
        stat_record = StatRecord(self.user.id, question.id, answer_time, user_answer, is_correct_ans, datetime.today().strftime('%Y-%m-%d'))
        db_save.save_stats_to_db(stat_record)
        if input(self.prompt_new_question).strip().lower() == '':
            self.get_problem(operation, smallest, largest)
        else:
            self.setup()
            return

    def get_stats(self):
        """print out stats for the user's session""" 
        if sum([self.questions_attempted[x] for x in self.operations]) > 0:
            print("\n=========")
            print("= STATS =")
            print("=========")
        for operation in self.operations:
            if self.questions_attempted[operation] > 0:
                print(f"\n{operation.title()}:")
                print("---------")
                print(f"\tSolved: {self.problems_solved[operation]}")
                print(f"\tAttempted: {self.questions_attempted[operation]}")
                print(f"\tPercent solved: {round(100 * self.problems_solved[operation] / self.questions_attempted[operation])}%")
                print(f"\tAverage time per problem: {round(self.answer_time_totals[operation] / self.questions_attempted[operation], 2)} seconds")
        input("Press any key to continue")

    def quit_program(self):
        stats = [False, True]['y' == input("Show stats? y / n\n")]
        if stats: self.get_stats()
        sys.exit("Goodbye!")

    def get_numbers_for_problem_range(self, designation):
        """get a number from the user
        
        Args:
            designation (string): designation interpolated into user prompt
        
        Returns:
            int: integer if user input is convertible else 0
        """        
        number = input(f"What's the {designation} number you want to use?\n")
        result = self.convert_string_int(number)
        if result is None or result < 2:
            print(self.get_error_message(number))
            return 0
        return result

    def select_user(self, msg = None):
        users = usr.get_users()
        if msg is None:
            print("Please type the number of your user and press 'Enter'\n")
        else:
            print(msg)
        for user in users:
            user.display_user()
        choice = input('\n')
        user_index = self.convert_string_int(choice)
        if user_index is not None:
            try:
                user = users[user_index - 1]
            except:
                self.select_user("Sorry, that doesn't seem to be a valid choice. Please try again")
        else:
            self.select_user("Sorry, that doesn't seem to be a valid choice. Please try again")
        return user

    def setup(self):
        """set up application
        
        Args:
            name (string): player name
        """ 
        os.system('clear') 
        self.solved = []
        self.problem_set = None 
        if self.user is None:
            self.user = self.select_user()
        if self.first_run:
            self.print_intro_screen(self.user)
            self.first_run = False  
        print("\nWhat would you like to practice?")
        choice = input('''
        1 - Addition
        2 - Subtraction
        3 - Multiplication
        4 - Division
        5 - Get Recommendations
        6 - Quit
        ''')
        selected = self.convert_string_int(choice)
        if selected is None or selected < 1 or selected > 6:
            print("Please choose an integer between 1 and 6.")
            self.setup()
        elif selected < 5 and selected >= 1:
            operation = self.choice_confirmation[selected]
            print(f"{operation} - great choice!")
        elif selected == 5:
            operation = self.choice_confirmation[selected]
            self.display_recommendations()
        elif selected == 6:
            self.quit_program()
        else:
            print("Please choose an integer between 1 and 5.")
            self.setup()
        smallest_number = 0
        while smallest_number < 2:
            smallest_number = self.get_numbers_for_problem_range("smallest")
        largest_number = 0
        while (largest_number < 2): 
            largest_number = self.get_numbers_for_problem_range("largest")
        if largest_number <= smallest_number:
            smallest_number, largest_number = largest_number, smallest_number
        smallest_number, largest_number = self.check_bounds(operation, smallest_number, largest_number)
        print(f"Great! Let's do some {self.choice_confirmation[selected]} problems with numbers between {smallest_number} and {largest_number}...")
        self.get_problem(operation, smallest_number, largest_number)
        return

if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument("name", type=str, nargs = '?', default="Anonymous Doo-Doo Head")
    # args = parser.parse_args()
    # player_name = args.name
    game = MathChallenge()
    game.setup()
