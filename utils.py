from tkinter import StringVar
import math

def is_number(value):
    if value.isdecimal() or (value.count('.') == 1 and value.replace('.', '').isdecimal()):
        return True
    return False

def decimal2Scientific(value):
    if len(str(int(value))) > 1:
        prefix = value / (10 ** (len(str(int(value))) - 1))
        return f"{prefix}E{len(str(int(value)))-1}"
    return value

class Operations(object):
    def __init__(self):
        self.result = 0
        self.deg_or_rad = 'radian'

    def equation_solver(self, equation):
        log = self.log_value
        ln = self.ln_value
        fact = self.factorial_value
        sqrt = self.squareRoot_value
        abs = self.absolute_value
        ceil = self.ceil_value
        floor = self.floor_value

        sin = self.sin_value
        cos = self.cos_value
        tan = self.tan_value
        asin = self.asin_value
        acos = self.acos_value
        atan = self.atan_value
        
        e = math.e
        pi = math.pi
        x = "x"
        equation = equation.replace('π', 'pi')
        equation = equation.replace('^', '**')

        try:
            return eval(equation)
        except:
            if "x" in equation:
                return "Equations: Only for Graph"
            else:
                return "Error: Cannot be calculated."
            
    @staticmethod
    def log_value(value):
        if value == 0:
            return "Undefined"
        base = 10
        result = math.log(value, base)
        return result
    
    @staticmethod
    def ln_value(value):
        if value == 0:
            return "Undefined"
        base = math.e
        result = math.log(value, base)
        return result
    
    @staticmethod
    def factorial_value(value):
        if int(value) < 0:
            return "Invalid Input."
        result = 1
        for i in range(2, value + 1):
            result *= i
        return result
    
    @staticmethod
    def squareRoot_value(value):
        result = value ** (1/2)
        return result
    
    @staticmethod
    def absolute_value(value):
        result = abs(value)
        return result
    
    @staticmethod
    def ceil_value(value):
        result = math.ceil(value)
        return result
    
    @staticmethod
    def floor_value(value):
        result = int(value)
        return result
        
    @staticmethod
    def radian_converter(angle):
        return math.radians(angle)
    
    @staticmethod
    def degree_converter(angle):
        return math.degrees(angle)
    
    def sin_value(self, angle):
        if self.deg_or_rad == 'degree':
            return math.sin(self.radian_converter(angle))
        return math.sin(angle)

    
    def cos_value(self, angle):
        if self.deg_or_rad == 'degree':
            return math.cos(self.radian_converter(angle))
        return math.cos(angle)
    
    def tan_value(self, angle):
        if self.deg_or_rad == 'degree':
            return math.tan(self.radian_converter(angle))
        return math.tan(angle)
    
    def asin_value(self, angle):
        if self.deg_or_rad == 'degree':
            return math.asin(self.radian_converter(angle))
        return math.asin(angle)
    
    def acos_value(self, angle):
        if self.deg_or_rad == 'degree':
            return math.acos(self.radian_converter(angle))
        return math.acos(angle)
    
    def atan_value(self, angle):
        if self.deg_or_rad == 'degree':
            return math.atan(self.radian_converter(angle))
        return math.atan(angle)
    
class BackEnd(Operations):
    def __init__(self):
        Operations.__init__(self)

        self.ops = ['+', '-', '*', '**', '^', '/', '//', '%']
        self.nums = '12345678900'
        self.funcs = ['asin', 'sin', 'acos', 'cos', 'atan', 'tan', 'fact', 'log', 'ln', 'sqrt', 'sqr', 'abs', 'ceil', 'floor']

        # to control the input of mathematical operators (+, -, *, /, etc.)
        self.allow_operator = False
        # to manage the input of specific mathematical constants - 'pi' and 'e'.
        self.allow_constants = True
        # to to control the ability to input any character
        self.allow_any = True

        self.angle_unit = StringVar()
        self.cursor = 0
        self.display_text = []
        self.textvar = StringVar()

    def operator_counter(self, expr):
        count = 0
        for i in expr:
            if i in self.ops + self.funcs:
                count += 1
        return count 
    
    def append_char(self, *char):
        # append each character to display in textbox
        for i in char:
            a = len(self.display_text)
            self.display_text.insert(a + self.cursor, i)

    def clear_text(self):
        # delete the display text
        self.display_text.clear()
        # reset the parameters for display
        self.allow_operator, self.allow_constants, self.allow_any = False, True, True
        self.cursor = 0

    def backspace_text(self):
        # to check where the backspace action should be performed
        index = len(self.display_text) + self.cursor - 1
        if self.display_text[index] == '(':
            # remove '('
            self.display_text.pop(index)
            # increase cursor to check next character
            self.cursor += 1
            # redo
            self.backspace_text()
            # check the ( at the function eg. sqrt() and delete (
            if self.display_text and self.display_text[len(self.display_text) + self.cursor - 1] in self.funcs:
                self.backspace_text()
        else:
            index = len(self.display_text) + self.cursor - 1
            if is_number(self.display_text[index]) and len(self.display_text[index]) > 1:
                self.display_text[index] = self.display_text[index][:-1]
            else:
                self.display_text.pop(len(self.display_text) + self.cursor - 1)
    
    def send_press(self, button):
        # limit - prevent user from entering many operators
        if button in self.ops + self.funcs and (self.operator_counter(self.display_text) > 14):
            return 0
        # to put () for the functions
        if button in self.funcs:
            if not self.allow_operator and self.allow_any:
                self.append_char(button, '(', ')')
                self.cursor -= 1
        # for showing the equation to graph 
        elif button == 'x':
            self.append_char(button)
            self.allow_operator, self.allow_any, self.allow_constants = True, True, True
        # for power function
        elif button == 'pow':
            if self.allow_operator:
                self.append_char('^')
                self.allow_operator, self.allow_any, self.allow_constants = False, True, True
        # for exponential function
        elif button == 'exp':
            if self.allow_operator and self.display_text[len(self.display_text) + self.cursor - 1] != 'e':
                self.append_char('E')
                self.allow_operator, self.allow_any, self.allow_constants = False, True, False
        # for arthmetic operations
        elif button in self.ops:
            if self.allow_operator:
                if button == "**":
                    self.append_char('^')
                else:
                    self.append_char(button)
                self.allow_operator, self.allow_any, self.allow_constants = False, True, True
            else:
                if button == '-' and ((self.display_text and self.display_text[len(self.display_text) + self.cursor - 1] != '-') or (not self.display_text)):
                    self.append_char('-')
                    self.allow_operator, self.allow_any, self.allow_constants = False, True, True
        # for constants
        elif button in ('e', 'pi'):
            if self.allow_constants:
                if button == 'pi':
                    self.append_char('π')
                else:
                    self.append_char(button)
                self.allow_operator, self.allow_any, self.allow_constants = True, False, False
        # for numbers
        elif button in self.nums: 
            if self.allow_any:
                if not self.display_text:
                    self.append_char(button)
                else:
                    if not is_number(self.display_text[len(self.display_text) + self.cursor - 1]):
                        self.append_char(button)
                    else:
                        self.display_text[len(self.display_text) + self.cursor - 1] = self.display_text[len(self.display_text) + self.cursor - 1] + str(button)
                self.allow_constants = False
                self.allow_operator = True
        # for clear expression
        elif button == 'C':
            self.clear_text()
        # for getting the answer
        elif button == '=':
            if self.display_text:
                print(self.display_text)
                self.deg_or_rad = self.angle_unit.get()
                b = self.equation_solver(self.textvar.get())
                self.display_text = [str(b)]
                if type(b) is str:
                    self.allow_operator, self.allow_any, self.allow_constants = False, False, False
                    self.cursor = 0
                else:
                    if b >= 10 ** 10000:
                        self.display_text = ['Overflow']
                        self.allow_any, self.allow_constants, self.allow_constants = False, False, False
                    else:
                        if 10 ** 45 <= b < 10 ** 10000:
                            self.display_text = [str(self.dec_to_e(b))]
                        self.allow_operator, self.allow_any, self.allow_constants = True, False, False
                        self.cursor = 0

                        # append the result to history.txt
                        with open('history.txt', 'a') as history_file:
                                history_file.write(f"{self.textvar.get()} = {b}\n")
        # for float point                
        elif button == '.':
            if self.display_text and self.display_text[len(self.display_text) + self.cursor - 1].isdecimal():
                self.display_text[len(self.display_text) + self.cursor - 1] += '.'
        # for natural number power
        elif button in ['10^x', 'e^x']:
            if not self.allow_operator and self.allow_any:
                self.append_char(button.split('^')[0], '^')
                self.allow_operator, self.allow_any, self.allow_constants = False, True, True
        # for power of 2
        elif button == 'x^2':
            if self.allow_operator:
                self.append_char('^', '2')
                self.allow_operator, self.allow_any, self.allow_constants = True, False, False
        # for ()
        elif button == '()':
            if not self.allow_operator and self.allow_any:
                self.append_char('(', ')')
                self.cursor -= 1
                self.allow_operator, self.allow_any, self.allow_constants = False, True, True
        # backspace - for delete one last character
        elif button == 'backspace':
            if self.display_text:
                self.backspace_text()
            curr = len(self.display_text) + self.cursor - 1
            if not self.display_text:
                self.clear_text()
            elif is_number(self.display_text[curr]):
                self.allow_operator, self.allow_any, self.allow_constants = True, True, False
            elif self.display_text[curr] in self.ops + ['(']:
                self.allow_operator, self.allow_any, self.allow_constants = False, True, True
            elif self.display_text[curr] in 'πe':
                self.allow_operator, self.allow_any, self.allow_constants = True, False, False
        # for root
        elif button == 'root':
            if self.allow_operator:
                self.append_char('^', '(', '1', '/', ')')
                self.cursor -= 1
                self.allow_operator, self.allow_any, self.allow_constants = False, True, True
        # for any character
        else:
            self.append_char(button)
            self.allow_operator = True
        self.textvar.set("".join(self.display_text))