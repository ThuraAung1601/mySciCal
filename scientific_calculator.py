# scientific_calculator.py
from tkinter import Tk, Toplevel, Button, Frame, Label, NE, NSEW, Radiobutton, RAISED, RIGHT, SOLID, DISABLED, SUNKEN, END, Text, YES, W, BOTH, WORD, messagebox
import numpy as np
import matplotlib.pyplot as plt
from utils import BackEnd
from unit_converter import UnitConverter

class App(BackEnd):
    
    # colors
    light_grey = "#B8B8B8"
    dark_grey = "#535353"
    light_green = "#A3CDA8"
    dark_green = "#729177"
    orange = "#FFA662"
    dark_orange = "#C48542"

    def __init__(self, w):
        BackEnd.__init__(self)

        self.buttons = [
            ['INV', 'π', 'e', '()', '←', 'C', '/', '//'],
            ['sin', 'cos', 'tan', '7', '8', '9', '*', '**'],
            ['log', 'ln', 'fact', '4', '5', '6', '+', '%'],
            ['pow', 'sqrt', 'abs', '1', '2', '3', False, '-'],
            ['ceil', 'floor', 'exp', '0', '00', '.', '=', False]
        ]

        self.inv_buttons = {
            'sin': 'asin', 'cos': 'acos', 'tan': 'atan',
            'log': '10^x', 'ln': 'e^x', 'fact': 'x',
            'pow': 'root', 'sqrt': 'x^2', 'abs': 'abs'
        }

        # inverse key will be active from row 1 (2nd row) to row 4
        self.inv_rows = (1, 4)
        # inverse key will be active from column 0 (1st column) to column 3
        self.inv_cols = (0, 3)

        self.w = w
        self.meta_window()

        self.top_frame = Frame(self.w, bg=App.light_grey)
        self.bottom_frame = Frame(self.w, bg=App.dark_grey)
        self.place_mainframes()

        # top frame widgets
        self.tf_buttons = Frame(self.top_frame)
        self.tf_copy_button = Button(self.top_frame)
        self.tf_about_button = Button(self.tf_buttons)
        self.tf_graph_button = Button(self.tf_buttons)
        self.tf_history_button = Button(self.tf_buttons)
        self.tf_menu_button = Button(self.tf_buttons)
        self.tf_confirm_text = Label(self.tf_buttons)

        self.tf_textbox = Label(self.top_frame)

        self.tf_angle_selection_frame = Frame(self.top_frame)
        self.tf_asf_text = Label(self.tf_angle_selection_frame)
        self.tf_asf_rad_choice = Radiobutton(self.tf_angle_selection_frame)
        self.tf_asf_deg_choice = Radiobutton(self.tf_angle_selection_frame)

        self.place_tf_widgets()
        self.config_tf_widgets()

        # bottom frame widgets
        self.bf_buttons = []
        self.inverse_State = False
        self.place_bf_widgets()

    def meta_window(self):
        self.w.geometry("640x440")
        self.w.title("Scientific Calculator")
        self.w.config(bg=App.dark_grey)
        self.w.resizable(False, False)
        # column 0 and row 1 will resize with window
        self.w.columnconfigure(0, weight=1)
        self.w.rowconfigure(1, weight=1)

    def place_mainframes(self):
        self.top_frame.grid(row=0, column=0, sticky=NSEW)
        self.top_frame.columnconfigure(0, weight=1)

        self.bottom_frame.grid(row=1, column=0, sticky=NSEW, padx=8, pady=8)
        self.bottom_frame.grid_propagate(False)
        for i in range(5):
            self.bottom_frame.rowconfigure(i, weight=1, uniform="xyz")
        for i in range(8):
            self.bottom_frame.columnconfigure(i, weight=1, uniform="xyz")

    def place_tf_widgets(self):
        self.tf_buttons.grid(row=0, column=0, pady=4, sticky=NSEW)
        self.tf_buttons.rowconfigure(0, weight=1)
        self.tf_buttons.grid_propagate(False)
        self.tf_copy_button.grid(row=1, column=1, padx=4, sticky=NSEW)
        self.tf_about_button.grid(row=0, column=1, padx=4, sticky=NSEW)
        self.tf_graph_button.grid(row=0, column=2, padx=4, sticky=NSEW)
        self.tf_history_button.grid(row=0, column=3, padx=4, sticky=NSEW)
        self.tf_menu_button.grid(row=0, column=4, padx=4, sticky=NSEW)
        self.tf_textbox.grid(row=1, column=0, sticky=NSEW, padx=4, pady=4)

        self.tf_angle_selection_frame.grid(row=2, column=0, sticky=W, pady=8, padx=4)
        self.tf_asf_text.grid(row=0, column=0, padx=4)
        self.tf_asf_rad_choice.grid(row=0, column=1, padx=16)
        self.tf_asf_deg_choice.grid(row=0, column=2, padx=4)

    def copy_result(self):
        text = self.textvar.get()
        self.w.clipboard_clear()
        self.w.clipboard_append(text)
        self.w.update()

        self.tf_confirm_text.grid(row=0, column=4, padx=4, sticky=NSEW)
        self.tf_confirm_text.after(2000, lambda: self.tf_confirm_text.grid_remove())

    def toggle_angle(self):
        curr_ang = self.angle_unit.get()
        print(f"You selected {curr_ang}")
        if curr_ang == "degree":
            self.tf_asf_deg_choice.config(selectcolor="lime")
            self.tf_asf_rad_choice.config(selectcolor=App.light_grey)
        else:
            self.tf_asf_deg_choice.config(selectcolor=App.light_grey)
            self.tf_asf_rad_choice.config(selectcolor="lime")

    def display_about(self):
        about_text = "Scientific Calculator\nVersion 1.0\nCreated by Thura Aung <66011606@kmitl.ac.th>"
        messagebox.showinfo("About", about_text)

    def graphing(self):
        if self.display_text:
            try:
                # Extract the expression from the display text
                expression = self.textvar.get()

                # Generate x values
                x_values = np.linspace(-10, 10, 400)

                # Evaluate the expression for each x value
                y_values = [self.equation_solver(expression.replace('x', str(x))) for x in x_values]

                # Plot the graph
                plt.plot(x_values, y_values)
                plt.title("Graph of " + expression)
                plt.xlabel("x")
                plt.ylabel("y")
                plt.grid(True)
                plt.show()
            except Exception as e:
                print(f"Error during graphing: {e}")

    def show_history(self):
            # Create a new window for history
            history_window = Toplevel(self.w)
            history_window.title("Calculation History")
            history_window.geometry("400x300")
            
            # Read history from the file
            try:
                with open('history.txt', 'r') as history_file:
                    history_data = history_file.readlines()
            except FileNotFoundError:
                history_data = []

            # Display history in a Text widget
            history_text = Text(history_window, wrap=WORD)
            history_text.pack(expand=YES, fill=BOTH)

            for entry in history_data:
                history_text.insert(END, entry)

            # Disable text editing in the history window
            history_text.config(state=DISABLED)

    def to_unit_converter(self):
        self.custom_root = Toplevel(self.w)
        unit_converter = UnitConverter(self.custom_root)

    def config_tf_widgets(self):
        self.tf_buttons.config(bg=App.light_grey, height=32)
        self.tf_copy_button.config(
            text="COPY",
            bg=App.dark_grey,
            activebackground=App.light_grey,
            fg=App.dark_grey,
            font=("Segoe UI", 14, 'bold'),
            borderwidth=3,
            command=lambda: self.copy_result())
        self.tf_about_button.config(
            text="ABOUT",
            bg=App.dark_grey,
            activebackground=App.light_grey,
            fg=App.dark_grey,
            font=("Segoe UI", 14, 'bold'),
            borderwidth=3,
            command=lambda: self.display_about())
        self.tf_graph_button.config(
            text="GRAPHING",
            bg=App.dark_grey,
            activebackground=App.light_grey,
            fg=App.dark_grey,
            font=("Segoe UI", 14, 'bold'),
            borderwidth=3,
            command=lambda: self.graphing())
        self.tf_history_button.config(
            text="HISTORY",
            bg=App.dark_grey,
            activebackground=App.light_grey,
            fg=App.dark_grey,
            font=("Segoe UI", 14, 'bold'),
            borderwidth=3,
            command=lambda: self.show_history())
        self.tf_menu_button.config(
            text="UNIT CONVERTER",
            bg=App.dark_grey,
            activebackground=App.light_grey,
            fg=App.dark_grey,
            font=("Segoe UI", 14, 'bold'),
            borderwidth=3,
            command=lambda: self.to_unit_converter())
        self.tf_confirm_text.config(
            text="Copied to Clipboard",
            bg="white",
            fg=App.dark_grey,
            font=('Segoe UI', 10))
        self.tf_textbox.update()
        self.tf_textbox.config(
            height=2,
            font=("Courier New", 16, "bold"),
            textvariable=self.textvar,
            fg=App.dark_grey,
            bg="white",
            borderwidth=2,
            relief=SOLID,
            wraplength=self.tf_textbox.winfo_width() - 6,
            justify=RIGHT,
            anchor=NE
        )

        self.tf_angle_selection_frame.config(bg=App.light_grey)
        self.tf_asf_text.config(
            text="Angle: ",
            bg=App.light_grey,
            font=('Segoe UI', 14, 'normal'))
        self.tf_asf_rad_choice.config(
            text="Radians",
            selectcolor=App.light_grey,
            activebackground=App.light_grey,
            font=('Segoe UI', 14, 'normal'),
            variable=self.angle_unit,
            value="rad",
            command=self.toggle_angle,
            bg=App.light_grey)
        self.tf_asf_deg_choice.config(
            text="Degrees",
            selectcolor="lime",
            activebackground=App.light_grey,
            font=('Segoe UI', 14, 'normal'),
            variable=self.angle_unit,
            value="deg",
            command=self.toggle_angle,
            bg=App.light_grey)
        self.angle_unit.set("deg")

    def inverse(self):
        if not self.inverse_State:
            # for i in range(1,4):
            for i in range(*self.inv_rows):
                if i == 1:
                    self.bf_buttons[i][2].config(
                        text=self.inv_buttons[self.buttons[i][2]],
                        bg=App.light_green,
                        command=lambda x=self.inv_buttons[self.buttons[i][2]]: [self.send_press(x), self.inverse()])
                for j in range(*self.inv_cols):
                    self.bf_buttons[i][j].config(
                        text=self.inv_buttons[self.buttons[i][j]],
                        bg=App.light_green,
                        command=lambda x=self.inv_buttons[self.buttons[i][j]]: [self.send_press(x), self.inverse()])
            self.bf_buttons[0][0].config(bg=App.dark_green, relief=SUNKEN)
            self.inverse_State = True
        else:
            for i in range(*self.inv_rows):
                if i == 1:
                    self.bf_buttons[i][2].config(
                        text=self.buttons[i][2],
                        bg=App.light_grey,
                        command=lambda x=self.buttons[i][2]: self.send_press(x))
                for j in range(*self.inv_cols):
                    self.bf_buttons[i][j].config(
                        text=self.buttons[i][j],
                        bg=App.light_grey,
                        command=lambda x=self.buttons[i][j]: self.send_press(x))
            self.bf_buttons[0][0].config(bg=App.light_green, relief=RAISED)
            self.inverse_State = False

    def place_bf_widgets(self):
        for i in range(len(self.buttons)):
            row = []
            for j in range(len(self.buttons[i])):
                if self.buttons[i][j]:
                    b = Button(
                        self.bottom_frame,
                        text=self.buttons[i][j],
                        bg=App.light_grey,
                        borderwidth=3,
                        font=('Segoe UI', 16, 'bold'),
                        command=lambda x=self.buttons[i][j]: self.send_press(x))
                    if (self.buttons[i][j].isdecimal() and self.buttons[i][j] != '00') or self.buttons[i][j] in ('+', '-', '=', '*', '/', '.', '()'):
                        self.w.bind(f"{self.buttons[i][j]}", lambda event, a=self.buttons[i][j]: self.send_press(a))
                    if j > 2 or (i == 0 and 0 < j < 3):
                        b.config(font=('Segoe UI', 22, 'bold'))
                    row.append(b)
                    b.grid(row=i, column=j, sticky=NSEW, padx=4, pady=4)
        
            self.bf_buttons.append(row)
        # print(self.buttons)
        self.w.bind('<Return>', lambda event, a='=': self.send_press(a))
        self.w.bind('<BackSpace>', lambda event, a='backspace': self.send_press(a))
        self.w.bind('<Delete>', lambda event, a='C': self.send_press(a))

        self.bf_buttons[2][6].grid(row=2, column=6, rowspan=2)
        self.bf_buttons[4][6].grid(row=4, column=6, columnspan=2)
        self.bf_buttons[0][0].config(bg=App.light_green, activebackground=App.dark_green)
        self.bf_buttons[0][5].config(bg=App.orange, activebackground=App.dark_orange)
        self.bf_buttons[0][4].config(bg=App.orange, activebackground=App.dark_orange)
        self.bf_buttons[0][1].config(command=lambda f='pi': self.send_press(f))
        self.bf_buttons[0][4].config(command=lambda f='backspace': self.send_press(f))

        self.bf_buttons[0][0].config(
            command=lambda x=self.buttons[0][0]: [print(f"You pressed {x}"), self.inverse()])

    def start(self):
        self.w.mainloop()


if __name__ == "__main__":
    root = Tk()
    calculator = App(root)
    calculator.start()