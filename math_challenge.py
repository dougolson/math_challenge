import random
import argparse
import sys
import time
import re
import math


def get_random_number(smallest, largest):
    return random.randint(smallest, largest)

def print_banner(name):
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

choice_confirmation = {1: "Addition", 2:"Subtraction", 3:"Multiplication", 4:"Division"}

def get_praise():
    praise = ["Nice!", "Noice!", "Well Done!", "Amazing!", "Fabulous", "Fantastic", "Splendimonious", "Que Bueno!", "You're the Goat!", "Sweet!", "Tasty!"]
    return praise[get_random_number(0, len(praise) - 1)]
def get_condolence():
    condolence = ["Regrettably", "Sadly", "My condolences", "Such a shame", "Oh what a pity", "Not quite", "Doh"]
    return condolence[get_random_number(0, len(condolence) - 1)]

float_pattern = r'\d*\.\d*'

def validate_and_convert_string_int(string_int):
    result = None
    if re.match(float_pattern, string_int):
        print(f"{get_condolence()}, that is not an integer!")
        return result
    try:
        result = int(string_int)
        return result
    except:
        print("That's not a number!")
        return result

def addition_problem(smallest, largest):
    n1 = get_random_number(smallest, largest)
    n2 = get_random_number(smallest, largest)
    response = input(f"{n1} + {n2} = ?\n")
    response = validate_and_convert_string_int(response)
    if response is not None:
        if response == n1 + n2:
            print(f"{get_praise()}")
        else:
            print(f"{get_condolence()}, {n1} + {n2} = {n1 + n2}!")    
    if input("Would you like to try again? y/n\n") == 'y':
        addition_problem(smallest, largest)
    else:
        print("Goodbye!\n")
        return

def subtraction_problem(smallest, largest):
    n1 = get_random_number(smallest, largest)
    n2 = get_random_number(smallest, largest)
    if n1 < n2:
        n1, n2 = n2, n1
    response = input(f"{n1} - {n2} = ?\n")
    response = validate_and_convert_string_int(response)
    if response is not None:
        if response == n1 - n2:
            print(f"{get_praise()}")
        else:
            print(f"{get_condolence()}, {n1} - {n2} = {n1 - n2}!")
    if input("Would you like to try again? y/n\n") == 'y':
        subtraction_problem(smallest, largest)
    else:
        print("Goodbye!\n")
        return

def multiplication_problem(smallest, largest):
    n1 = get_random_number(smallest, largest)
    n2 = get_random_number(smallest, largest)
    response = input(f"{n1} x {n2} = ?\n")
    response = validate_and_convert_string_int(response)
    if response is not None:
        if response == n1 * n2:
            print(f"{get_praise()}")
        else:
            print(f"{get_condolence()}, {n1} * {n2} = {n1 * n2}!")
    if input("Would you like to try again? y/n\n") == 'y':
        multiplication_problem(smallest, largest)
    else:
        print("Goodbye!\n")
        return

def division_problem(smallest, largest):
    max_divisor = int(math.sqrt(largest)) + 1
    candidate_numbers = range(smallest, max_divisor)
    divisor = random.choice(candidate_numbers)
    quotient = random.choice(candidate_numbers)
    print(f"smallest {smallest}")
    print(f"largest {largest}")
    print(f"largest // smallest {largest // smallest}")
    dividend = divisor * quotient
    print(f"divisor = {divisor}")
    print(f"quotient  = {quotient}")
    print(f"dividend  = {dividend}")

    # max_divisor = dividend // quotient
    # if max_divisor < smallest:
    #     max_divisor, smallest = smallest, max_divisor
    # # divisor = n2
    # divisor = random.choice([x for x in range(smallest, max_divisor + 1)])
    # print(f"quotient = {quotient}")
    # dividend = divisor * quotient
    # print(f"dividend = {dividend}")
    response = input(f"{dividend} / {divisor} = ?\n")
    response = validate_and_convert_string_int(response)
    if response is not None:
        if response == quotient:
            print(f"{get_praise()}")
        else:
            print(f"{get_condolence()}, {dividend} / {divisor} = {quotient}!")
    if input("Would you like to try again? y/n\n") == 'y':
        division_problem(smallest, largest)
    else:
        setup('')
        return   

def quit_program(dummy_1, dummy_2):
    print("Goodbye!\n")
    sys.exit()

function_choice = {1: addition_problem, 2: subtraction_problem, 3: multiplication_problem, 4: division_problem, 5:quit_program}

def setup(name):
    if first_run:
        print_banner(name)
        first_run = False  
    print("What do you want to practice?")
    # print()
    choice = input('''
    1 - Addition
    2 - Subtraction
    3 - Multiplication
    4 - Division
    5 - Quit
    ''')
    try: 
        choice = int(choice)
        print(f"{choice_confirmation[choice]} - great choice!")
    except:
        print("Sorry - I didn't understand that")
    smallest_number = input("What's the smallest number you want to use?\n")
    try:
        smallest_number =int(smallest_number)
    except:
        print("that doesn't seem to be a number!")
    largest_number = input("What's the largest number you want to use?\n")
    try:
        largest_number =int(largest_number)
    except:
        print("that doesn't seem to be a number!")

    print(f"Great! Let's do some {choice_confirmation[choice]} problems with numbers between {smallest_number} and {largest_number}...")
    answer = function_choice[choice](smallest_number, largest_number)


    
    

# def main():



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("name", type=str, default="Mr. Doo-Doo Head")
    args = parser.parse_args()
    player_name = args.name
    first_run = True
    setup(player_name)
