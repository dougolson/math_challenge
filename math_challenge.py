from ast import Raise
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
        self.float_pattern = r'(-|\+)?\d*\.\d*'
        self.function_choice = {1: self.addition_problem, 2: self.subtraction_problem, 3: self.multiplication_problem, 4: self.division_problem, 5:self.quit_program}

    def get_random_number(self, smallest, largest):
        return random.randint(smallest, largest)

    def print_banner(self, name):
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

    def get_praise(self, ):
        praise = ["Nice!", "Noice!", "Well Done!", "Amazing!", "Fabulous", "Fantastic", "Splendimonious", "Que Bueno!", "You're the Goat!", "Sweet!", "Tasty!"]
        return praise[self.get_random_number(0, len(praise) - 1)]
    
    def get_condolence(self, ):
        condolence = ["Regrettably", "Sadly", "My condolences", "Such a shame", "Oh what a pity", "Not quite", "Doh"]
        return condolence[self.get_random_number(0, len(condolence) - 1)]

    def validate_and_convert_string_int(self, string_int):
        result = None
        if re.match(self.float_pattern, string_int):
            print(f"{self.get_condolence()}, number must be a positive integer!")
            return result
        try:
            result = int(string_int)
            if result < 1:
                print(f"{self.get_condolence()}, number must be a positive integer!")
                return None
            return result
        except:
            print("That's not a number!")
            return result

    def addition_problem(self, smallest, largest):
        n1 = self.get_random_number(smallest, largest)
        n2 = self.get_random_number(smallest, largest)
        response = input(f"{n1} + {n2} = ?\n")
        response = self.validate_and_convert_string_int(response)
        if response is not None:
            if response == n1 + n2:
                print(f"{self.get_praise()}")
            else:
                print(f"{self.get_condolence()}, {n1} + {n2} = {n1 + n2}!")    
        if input("Would you like to try again? y/n\n") == 'y':
            self.addition_problem(smallest, largest)
        else:
            self.setup('')
            return 

    def subtraction_problem(self, smallest, largest):
        n1 = self.get_random_number(smallest, largest)
        n2 = self.get_random_number(smallest, largest)
        if n1 < n2:
            n1, n2 = n2, n1
        response = input(f"{n1} - {n2} = ?\n")
        response = self.validate_and_convert_string_int(response)
        if response is not None:
            if response == n1 - n2:
                print(f"{self.get_praise()}")
            else:
                print(f"{self.get_condolence()}, {n1} - {n2} = {n1 - n2}!")
        if input("Would you like to try again? y/n\n") == 'y':
            self.subtraction_problem(smallest, largest)
        else:
            self.setup('')
            return 

    def multiplication_problem(self, smallest, largest):
        n1 = self.get_random_number(smallest, largest)
        n2 = self.get_random_number(smallest, largest)
        response = input(f"{n1} x {n2} = ?\n")
        response = self.validate_and_convert_string_int(response)
        if response is not None:
            if response == n1 * n2:
                print(f"{self.get_praise()}")
            else:
                print(f"{self.get_condolence()}, {n1} * {n2} = {n1 * n2}!")
        if input("Would you like to try again? y/n\n") == 'y':
            self.multiplication_problem(smallest, largest)
        else:
            self.setup('')
            return 

    def division_problem(self, smallest, largest):
        max_divisor = int(math.sqrt(largest)) + 1
        candidate_numbers = range(smallest, max_divisor)
        divisor = random.choice(candidate_numbers)
        quotient = random.choice(candidate_numbers)
        dividend = divisor * quotient
        response = input(f"{dividend} / {divisor} = ?\n")
        response = self.validate_and_convert_string_int(response)
        if response is not None:
            if response == quotient:
                print(f"{self.get_praise()}")
            else:
                print(f"{self.get_condolence()}, {dividend} / {divisor} = {quotient}!")
        if input("Would you like to try again? y/n\n") == 'y':
            self.division_problem(smallest, largest)
        else:
            self.setup('')
            return   

    def quit_program(self):
        sys.exit("Goodbye!")

    def get_number(self, designation):
        number = input(f"What's the {designation} number you want to use?\n")
        number = self.validate_and_convert_string_int(number)
        return number

    def setup(self, name):
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
        try: 
            choice = self.validate_and_convert_string_int(choice)
            if choice < 5:
                print(f"{self.choice_confirmation[choice]} - great choice!")
            if choice > 5:
                print("Sorry - I didn't understand that")
                self.setup('')
        except:
            print("Sorry - I didn't understand that")
            self.setup('')
        if choice == 5:
            self.quit_program()
            return
        # smallest_number = input("What's the smallest number you want to use?\n")
        smallest_number = 0
        while (smallest_number is None or smallest_number < 1):
            smallest_number = self.get_number("smallest")
            print(f"smallest_number = {smallest_number}")
        largest_number = smallest_number
        while (largest_number is None or largest_number <= smallest_number):
            largest_number = self.get_number("largest")
        # try:
        # except:
        #     print("that doesn't seem to be a number!")
        # largest_number = input("What's the largest number you want to use?\n")
        # try:
        #     largest_number =self.validate_and_convert_string_int(largest_number)
        # except:
        #     print("that doesn't seem to be a number!")

        print(f"Great! Let's do some {self.choice_confirmation[choice]} problems with numbers between {smallest_number} and {largest_number}...")
        self.function_choice[choice](smallest_number, largest_number)
        return

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("name", type=str, nargs = '?', default="Anonymous Doo-Doo Head")
    args = parser.parse_args()
    player_name = args.name
    game = MathChallenge()
    game.setup(player_name)
