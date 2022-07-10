import random
import argparse
import sys
import time
import re
import math

class MathChallenge():
    
    def __init__(self):
        self.first_run = True
        self.choice_confirmation = {1: "Addition", 2:"Subtraction", 3:"Multiplication", 4:"Division", 5:"Quit"}
        self.int_pattern = r'\s*\d+\s*'
        self.negative_int_pattern = r'-\d+'
        self.less_than_two_pattern = r'(-[0-9]+|[0-1])'
        self.float_pattern = r'(-|\+)?\d*\.\d*'
        self.negative_integer_message = "number must be at least 1!"
        self.invalid_choice_message = "Sorry, that isn't a valid choice"
        self.less_than_two_message = "number must be an integer grater than 1"
        self.float_message = "number can't be a decimal"
        self.not_a_number_message = "I don't even know what that is!"
        self.prompt_new_question = "Try another? y/n\n"
        self.function_choice = {1: self.addition_problem, 2: self.subtraction_problem, 3: self.multiplication_problem, 4: self.division_problem, 5:self.quit_program}

    def get_random_number(self, smallest, largest):
        """get a random intger between smallest and largest
        
        Args:
            smallest (int): 
            largest (int): 

        Returns:
            int
        """        
        return random.randint(smallest, largest)

    def print_banner(self, name):
        """print out a banner

        Args:
            name (string): name of the user
        """        
        banner_string = f"- {name}\'s Math Challenge! -"
        print("\nWelcome to")
        spinner = ['+ ','- ','x ','/ ',]
        for i in range(20):
            sys.stdout.write(spinner[i%4])
            sys.stdout.flush()
            time.sleep(0.05)
        print("\n")
        print("-" * len(banner_string))
        print(f"{banner_string}")
        print("-" * len(banner_string))

    def get_praise(self):
        """get a randomly selected praise statement

        Returns:
            string: praise statement
        """        
        praise = ["Nice!", "Noice!", "Well Done!", "Amazing!", "Fabulous", "Fantastic", "Splendimonious", "Que Bueno!", "You're the Goat!", "Sweet!", "Tasty!"]
        return praise[self.get_random_number(0, len(praise) - 1)]
    
    def get_condolence(self):
        """get a randomly selected condolence statement

        Returns:
            string: condolence statement
        """ 
        condolence = ["Regrettably", "Sadly", "My condolences", "Such a shame", "Oh what a pity", "Not quite", "Doh!"]
        return condolence[self.get_random_number(0, len(condolence) - 1)]

    def get_confused_response(self):
        """get a randomly selected statement of confusion

        Returns:
            string: statement of confusion
        """ 
        confusion = ["uh, wut?", "I don't understand...", "That didn't make sense...", "It is a tale told by an idiot, full of sound and fury, signifying nothing...", "Fascinating, yet incomprehensible", "Captain... I'm confused", "Sorry, I didn't catch that", "Are you messing with me?", "Doh"]
        return confusion[self.get_random_number(0, len(confusion) - 1)]
    
    def is_valid_string_int(self, string_int):
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

    def convert_string_int(self, string_int):
        """convert a valid string int to an integer

        Args:
            string_int (string): a string int

        Returns:
            int or None: an integer if string can be converted, else None
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
            return f"{self.get_condolence()}, {self.less_than_two_message}"
        elif re.match(self.float_pattern, string_int):
            return f"{self.get_condolence()}, {self.float_message}"
        # elif string_int == '0':
        #     return self.invalid_choice_message
        else:
            return f"{self.get_condolence()}, {self.not_a_number_message}"

    def addition_problem(self, smallest, largest):
        """generate an addition problem with operands between smallest and largest

        Args:
            smallest (int): smallest operand
            largest (int): largest operand
        """        
        n1 = self.get_random_number(smallest, largest)
        n2 = self.get_random_number(smallest, largest)
        response = input(f"{n1} + {n2} = ?\n")
        result = self.convert_string_int(response)
        if result is not None:
            if result == n1 + n2:
                print(f"{self.get_praise()}")
            else:
                print(f"{self.get_condolence()}, {n1} + {n2} = {n1 + n2}!")    
        else:
            print(f"{self.get_confused_response()}")        
        if input(self.prompt_new_question).strip().lower() == 'y':
            self.addition_problem(smallest, largest)
        else:
            self.setup('')
            return 

    def subtraction_problem(self, smallest, largest):
        """generate an subtraction problem with operands between smallest and largest

        Args:
            smallest (int): smallest operand
            largest (int): largest operand
        """ 
        n1 = self.get_random_number(smallest, largest)
        n2 = self.get_random_number(smallest, largest)
        if n1 < n2:
            n1, n2 = n2, n1
        response = input(f"{n1} - {n2} = ?\n")
        result = self.convert_string_int(response)
        if result is not None:
            if result == n1 - n2:
                print(f"{self.get_praise()}")
            else:
                print(f"{self.get_condolence()}, {n1} - {n2} = {n1 - n2}!")
        else:
            print(f"{self.get_confused_response()}")
        if input(self.prompt_new_question).strip().lower() == 'y':
            self.subtraction_problem(smallest, largest)
        else:
            self.setup('')
            return 

    def multiplication_problem(self, smallest, largest):
        """generate an multiplication problem with operands between smallest and largest

        Args:
            smallest (int): smallest operand
            largest (int): largest operand
        """ 
        n1 = self.get_random_number(smallest, largest)
        n2 = self.get_random_number(smallest, largest)
        response = input(f"{n1} x {n2} = ?\n")
        result = self.convert_string_int(response)
        if result is not None:
            if result == n1 * n2:
                print(f"{self.get_praise()}")
            else:
                print(f"{self.get_condolence()}, {n1} * {n2} = {n1 * n2}!")
        else:
            print(f"{self.get_confused_response()}")
        if input(self.prompt_new_question).strip().lower() == 'y':
            self.multiplication_problem(smallest, largest)
        else:
            self.setup('')
            return 

    def generate_divisor_list(self, smallest, largest):
        """generate a list of numbers >= smallest such that the product of any number
        in the list and at least one other number in the list is less than largest

        Args:
            smallest (int): smallest divisor
            largest (int): upper limit divisor

        Returns:
            list: list of integers
        """        
        result = []
        for i in range(smallest, largest + 1 // 2):
            if largest // i < smallest: break
            result.append(largest // i)
        return sorted(list(set(result)))

    def generate_quotient_divisor_pairs(self, lst):
        """generate a list of 2-tuples where the product of the tuple elements
        is less than or equal to min(lst) * max(lst) + 1

        Args:
            lst (list): list of integers

        Returns:
            list: list of tuple(int, int)
        """        
        result = []
        for i in range(len(lst)):
            j = i
            while j < len(lst) - i:
                result.append((lst[i], lst[j]))
                j += 1
        return result

    def division_problem(self, smallest, largest):
        """generate an division problem with divisor and quotient >= smallest
        such that the dividend <= largest. In other words: 
        divisor * quptient = dividend | dividend <= largest

        Args:
            smallest (int): smallest divisor | quotient
            largest (int): largest dividend
        """ 
        divisor_list = self.generate_divisor_list(smallest, largest)
        quotient_divisor_pairs = self.generate_quotient_divisor_pairs(divisor_list)
        quotient, divisor = random.choice(quotient_divisor_pairs)
        dividend = quotient * divisor
        response = input(f"{dividend} / {divisor} = ?\n")
        result = self.convert_string_int(response)
        if result is not None:
            if result == quotient:
                print(f"{self.get_praise()}")
            else:
                print(f"{self.get_condolence()}, {dividend} / {divisor} = {quotient}!")
        else:
            print(f"{self.get_confused_response()}")
        if input(self.prompt_new_question).strip().lower() == 'y':
            self.division_problem(smallest, largest)
        else:
            self.setup('')
            return   

    def quit_program(self):
        sys.exit("Goodbye!")

    def get_number(self, designation):
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

    def setup(self, name):
        """set up application

        Args:
            name (string): player name
        """        
        if self.first_run:
            self.print_banner(name)
            self.first_run = False  
        print("What do you want to practice?")
        choice = input('''
        1 - Addition
        2 - Subtraction
        3 - Multiplication
        4 - Division
        5 - Quit
        ''')
        selected = self.convert_string_int(choice)
        if selected is None or selected < 1 or selected > 5:
            print("Please choose an integer between 1 and 5.")
            self.setup('')
        elif selected < 5 and selected >= 1:
            print(f"{self.choice_confirmation[selected]} - great choice!")
        elif selected == 5:
            self.quit_program()
        else:
            print("Please choose an integer between 1 and 5.")
            self.setup('')
        smallest_number = 0
        while smallest_number < 2:
            smallest_number = self.get_number("smallest")
        largest_number = 0
        while (largest_number < 2): 
            largest_number = self.get_number("largest")
        if largest_number <= smallest_number:
            smallest_number, largest_number = largest_number, smallest_number
                # print("Largest number must be larger than the smallest number. Fancy that!")
        print(f"Great! Let's do some {self.choice_confirmation[selected]} problems with numbers between {smallest_number} and {largest_number}...")
        self.function_choice[selected](smallest_number, largest_number)
        return

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("name", type=str, nargs = '?', default="Anonymous Doo-Doo Head")
    args = parser.parse_args()
    player_name = args.name
    game = MathChallenge()
    game.setup(player_name)
