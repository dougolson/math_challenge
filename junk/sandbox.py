import curses
from curses import panel
import re

class Utils():
    @classmethod
    def is_valid_string_int(self, string_int):
        """is a string a valid representation of an integer

        Args:
            string_int (string): a string

        Returns:
            boolean: True if valid, else False
        """        
        result = False
        if re.fullmatch(r'\d+', string_int):
            result = True
        return result

class Addition():
    def __init__(self, stdscreen):
        self.window = stdscreen.subwin(10, 0)
        self.window.keypad(0)
        self.panel = panel.new_panel(self.window)
        self.panel.hide()
        panel.update_panels()
        self.position = 0
        self.smallest = None
        self.largest = None

    def reset(self):
        self.smallest = None
        self.largest = None

    def get_number_range(self, y, x):
        if self.smallest is None:
            self.window.addstr(y , x, "what is the smallest number you would like to use?")
            key = self.window.getkey()
            self.window.clrtoeol()
            while not Utils.is_valid_string_int(key):
                self.get_number_range(y, x)
            self.smallest = int(key)
        if self.largest is None:
            self.window.addstr(y , x, "what is the largest number you would like to use?")
            key = self.window.getkey()
            self.window.clrtoeol()
            while not Utils.is_valid_string_int(key):
                self.get_number_range(y, x)
            self.largest = int(key)
        if self.smallest >= self.largest:
            self.reset()
            self.window.clrtoeol()
            self.window.addstr(y , x, "Sorry, the smallest number has to be smaller than the largest number. Tyy again")
            self.get_number_range(y+1, x)
        return 



    # def problem(self, smallest, largest):
    #     """generate an addition problem with operands between smallest and largest

    #     Args:
    #         smallest (int): smallest operand
    #         largest (int): largest operand
    #     """        
    #     n1 = self.get_random_number(smallest, largest)
    #     n2 = self.get_random_number(smallest, largest)
    #     self.start_timer()
    #     response = input(f"{n1} + {n2} = ?\n")
    #     result = self.convert_string_int(response)
    #     if result is not None:
    #         if result == n1 + n2:
    #             print(f"{self.get_praise()}")
    #             self.problems_solved[1] += 1
    #         else:
    #             print(f"{self.get_condolence()}, {n1} + {n2} = {n1 + n2}!")
    #     else:
    #         print(f"{self.get_confused_response()}, {self.get_error_message(response)}")        
    #     self.problem_time[1] += self.stop_timer()
    #     self.problems_attempted[1] += 1   
    #     if input(self.prompt_new_question).strip().lower() == '':
    #         self.addition_problem(smallest, largest)
    #     else:
    #         self.setup('')
    #         return

    def display(self):
        self.panel.top()
        self.panel.show()
        self.window.clear()
        self.index = 1
        self.window.addstr(1 , 1, "Welcome to Addition")
        self.window.addstr(2 , 1, "press 'm' to return to the menu")
        self.get_number_range(3, 1)
        self.window.addstr(3 , 1, f"Great! Let's do some problems with numbers between {self.smallest} and {self.largest}")
        while True:
        #     self.window.refresh()
        #     curses.doupdate()
        #     for index, item in enumerate(self.items):
        #         if index == self.position:
        #             mode = curses.A_REVERSE
        #         else:
        #             mode = curses.A_NORMAL

        #         msg = "%d. %s" % (index, item[0])
        # self.window.addstr(1 + index, 1, msg, mode)

            

            key = self.window.getch()
            if key == ord('m'): 
                self.reset()
                break
            # if key in [curses.KEY_ENTER, ord("\n")]:
            #     if self.position == len(self.items) - 1:
            #         break
            #     else:
            #         self.items[self.position][1]()

            # elif key == curses.KEY_UP:
            #     self.navigate(-1)

            # elif key == curses.KEY_DOWN:
            #     self.navigate(1)

        self.window.clear()
        self.panel.hide()
        panel.update_panels()
        curses.doupdate()

    

class Menu():
    def __init__(self, items, stdscreen):
        self.window = stdscreen.subwin(0, 0)
        self.window.keypad(1)
        self.panel = panel.new_panel(self.window)
        self.panel.hide()
        panel.update_panels()

        self.position = 0
        self.items = items
        self.items.append(("exit", "exit"))

    def navigate(self, n):
        self.position += n
        if self.position < 0:
            self.position = 0
        elif self.position >= len(self.items):
            self.position = len(self.items) - 1

    def display(self):
        self.panel.top()
        self.panel.show()
        self.window.clear()

        while True:
            self.window.refresh()
            curses.doupdate()
            for index, item in enumerate(self.items):
                if index == self.position:
                    mode = curses.A_REVERSE
                else:
                    mode = curses.A_NORMAL

                msg = "%d. %s" % (index, item[0])
                self.window.addstr(1 + index, 1, msg, mode)

            key = self.window.getch()

            if key in [curses.KEY_ENTER, ord("\n")]:
                if self.position == len(self.items) - 1:
                    break
                else:
                    self.items[self.position][1]()

            elif key == curses.KEY_UP:
                self.navigate(-1)

            elif key == curses.KEY_DOWN:
                self.navigate(1)

        self.window.clear()
        self.panel.hide()
        panel.update_panels()
        curses.doupdate()


class MyApp(object):
    def __init__(self, stdscreen):
        self.screen = stdscreen
        curses.curs_set(0)

        # submenu_items = [("beep", curses.beep), ("flash", curses.flash)]
        # submenu = Menu(submenu_items, self.screen)

        main_menu_items = [
            ("Add", Addition(self.screen).display),
            ("Subtract", curses.flash),
            ("Multiply", curses.flash),
            ("Divide", curses.flash),
        ]
        main_menu = Menu(main_menu_items, self.screen)
        main_menu.display()


if __name__ == "__main__":
    # curses.wrapper(MyApp)
    util = Utils()
    print(util.is_valid_string_int('7'))
    print(util.is_valid_string_int('07'))
    print(util.is_valid_string_int('X'))