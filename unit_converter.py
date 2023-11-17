# unit_converter.py
from tkinter import *
from tkinter import messagebox
from utils import BackEnd

class UnitConverter(BackEnd):
    """
    A class implementing unit conversion via a graphical user interface (GUI).

    Inherits from BackEnd class to utilize conversion methods.

    Attributes:
    - root (Tk): The root Tkinter instance for the GUI.
    - colors (dict): Dictionary containing color codes for GUI elements.
    - unitDict (dict): Dictionary of conversion factors for different units.
    - length_units (list): List of length-related unit types.
    - temperature_units (list): List of temperature-related unit types.
    - area_units (list): List of area-related unit types.
    - volume_units (list): List of volume-related unit types.
    - weight_units (list): List of weight-related unit types.
    - SELECTIONS (list): List of unit selections for the GUI dropdown menu.
    - buttons (list): List containing buttons layout for the GUI.

    Methods:
    - __init__(self, root): Constructor method initializing the GUI and variables.
    - create_gui(self): Creates the graphical user interface.
    - create_buttons(self): Generates buttons for the GUI layout for user input.
    - display_about(self): Displays information about the Unit Converter.
    - reset(self): Resets the input and output fields and clears the history.
    - convert(self): Performs unit conversion based on user input and selected units.
    - add_digit(self, digit): Appends a digit to the input field.
    - delete_character(self): Deletes the last character from the input field.
    - update_history(self): Updates the conversion history displayed in the GUI.
    - load_conversion_history(self): Loads conversion history from a file.
    - save_conversion_history(self): Saves conversion history to a file.
    - show_history(self): Displays conversion history in a new window.
    """
    def __init__(self, root):
        BackEnd.__init__(self)
        self.root = root

        self.colors = {
            "light_grey": "#B8B8B8",
            "dark_grey": "#535353",
        }

        # dictionary of conversion factors  
        self.unitDict = {  
            "millimeter" : 0.001,  
            "centimeter" : 0.01,  
            "meter" : 1.0,  
            "kilometer" : 1000.0,  
            "foot" : 0.3048,  
            "mile" : 1609.344,  
            "yard" : 0.9144,  
            "inch" : 0.0254,  
            "square meter" : 1.0,  
            "square kilometer" : 1000000.0,  
            "square centimeter" : 0.0001,  
            "square millimeter" : 0.000001,  
            "are" : 100.0,  
            "hectare" : 10000.0,  
            "acre" : 4046.856,  
            "square mile" : 2590000.0,  
            "square foot" : 0.0929,  
            "cubic meter" : 1000.0,  
            "cubic centimeter" : 0.001,  
            "litre" :  1.0,  
            "millilitre" : 0.001,  
            "gallon" : 3.785,  
            "gram" : 1.0,  
            "kilogram" : 1000.0,  
            "milligram" : 0.001,  
            "quintal" : 100000.0,  
            "ton" : 1000000.0,  
            "pound" : 453.592,  
            "ounce" : 28.3495  
        }  

        # charts for units conversion  
        self.length_units = [  
            "millimeter", "centimeter", "meter", "kilometer", "foot", "mile", "yard", "inch"  
            ]  
        self.temperature_units = [  
            "celsius", "fahrenheit"  
        ]  
        self.area_units = [  
            "square meter", "square kilometer", "square centimeter", "square millimeter",  
            "are", "hectare", "acre", "square mile", "square foot"  
            ]  
        self.volume_units = [  
            "cubic meter", "cubic centimeter", "litre", "millilitre", "gallon"     
        ]  
        self.weight_units = [  
            "gram", "kilogram", "milligram", "quintal", "ton", "pound", "ounce"  
        ]  

        # creating the list of options for selection menu  
        self.SELECTIONS = [  
            "Select Unit",  
            "millimeter",  
            "centimeter",  
            "meter",  
            "kilometer",  
            "foot",  
            "mile",  
            "yard",  
            "inch",  
            "celsius",  
            "fahrenheit", 
            "square meter",  
            "square kilometer",  
            "square centimeter",  
            "square millimeter",  
            "are",  
            "hectare",  
            "acre",  
            "square mile",  
            "square foot",  
            "cubic meter",  
            "cubic centimeter",  
            "litre",  
            "millilitre",  
            "gallon"     
            "gram",  
            "kilogram",  
            "milligram",  
            "quintal",  
            "ton",  
            "pound",  
            "ounce"  
        ] 

        self.buttons = [
            ['7', '8', '9'],
            ['4', '5', '6'],
            ['1', '2', '3'],
            ['OK', '0', '←']
        ]

        self.create_gui()

        self.conversion_history = []
        self.load_conversion_history()

        self.history_text = Text(self.root, wrap=WORD)
        self.history_text.grid(row=2, column=0, padx=10, pady=10, columnspan=4)
        self.history_text.config(state=DISABLED)

    def create_gui(self):
        self.root.title("Unit Converter")
        self.root.geometry("450x320")
        self.root.resizable(False, False)
        self.root.configure(bg=self.colors["light_grey"])

        self.top_frame = Frame(self.root, bg=self.colors["light_grey"])
        self.top_frame.grid(row=0, column=0, sticky=NSEW)
        
        self.about = Button(self.top_frame, text="ABOUT", bg=self.colors["light_grey"], fg=self.colors["dark_grey"], font=("Segoe UI", 14, 'bold'), borderwidth=3, padx=4, command=self.display_about)
        self.reset_button = Button(self.top_frame, text="RESET", bg=self.colors["light_grey"], fg=self.colors["dark_grey"], font=("Segoe UI", 14, 'bold'), borderwidth=3, padx=4, command=self.reset)
        self.about.grid(row=1, column=1)
        self.reset_button.grid(row=1, column=3)

        self.history_button = Button(
            self.top_frame,
            text="Show History",
            bg=self.colors["light_grey"],
            fg=self.colors["dark_grey"],
            font=("Segoe UI", 14, 'bold'),
            borderwidth=3,
            padx=4,
            command=self.show_history
        )
        self.history_button.grid(row=1, column=2)
        
        self.bottom_frame = Frame(self.root, bg=self.colors["light_grey"])
        self.bottom_frame.grid(row=1, column=0, sticky=NSEW)
        
        self.input_value = StringVar()
        self.output_value = StringVar()
        self.input_value.set(self.SELECTIONS[0])
        self.output_value.set(self.SELECTIONS[0])

        # creating the labels for the body of the main window  
        self.input_label = Label(  
            self.bottom_frame,  
            text = "From:",  
            bg = self.colors["light_grey"],  
            fg = self.colors["dark_grey"],
            font=("Segoe UI", 14, 'bold')
        )  
        self.output_label = Label(  
            self.bottom_frame,  
            text = "To:",  
            bg = self.colors["light_grey"],  
            fg = self.colors["dark_grey"],
            font=("Segoe UI", 14, 'bold')  
        )  

        # using the grid() method to set the position of the above labels   
        self.input_label.grid(row = 0, column = 0, padx = 20, pady = 20, sticky = NSEW)  
        self.output_label.grid(row = 1, column = 0, padx = 20, pady = 20, sticky = NSEW)  

        self.input_field = Entry(self.bottom_frame, bg="#e8f8f5")
        self.output_field = Entry(self.bottom_frame, bg="#e8f8f5")
        self.input_field.grid(row=0, column=1)
        self.output_field.grid(row=1, column=1)

        self.input_menu = OptionMenu(self.bottom_frame, self.input_value, *self.SELECTIONS)
        self.output_menu = OptionMenu(self.bottom_frame, self.output_value, *self.SELECTIONS)
        self.input_menu.grid(row=0, column=2, padx=20)
        self.output_menu.grid(row=1, column=2, padx=20)

        self.create_buttons()

    def create_buttons(self):
        self.buttons_frame = Frame(self.bottom_frame, bg=self.colors["dark_grey"])
        for i, row_buttons in enumerate(self.buttons):
            for j, button_text in enumerate(row_buttons):
                button = Button(
                    self.buttons_frame,
                    text=button_text,
                    bg=self.colors["light_grey"],
                    borderwidth=3,
                    font=('Segoe UI', 16, 'bold')
                )
                if button_text.isdigit():
                    button.config(command=lambda x=button_text: self.add_digit(x))
                elif button_text == "OK":
                    button.config(command=lambda x=button_text: self.convert())
                elif button_text == "←":
                    button.config(command=lambda x=button_text: self.delete_character(x))

                button.grid(row=i, column=j, sticky=NSEW, padx=4, pady=4)
        
                
        self.buttons_frame.grid(row=2, column=1, sticky=NSEW)

    def display_about(self):
        about_text = "Unit Converter\nVersion 1.0\nCreated by Thura Aung <66011606@kmitl.ac.th>"
        messagebox.showinfo("ABOUT", about_text)

    def reset(self):
        self.input_field.delete(0, END)
        self.output_field.delete(0, END)
        self.input_value.set(self.SELECTIONS[0])
        self.output_value.set(self.SELECTIONS[0])
        self.input_field.focus_set()

        # Clear conversion history when resetting
        self.conversion_history = []
        self.update_history()
        self.save_conversion_history()

    def convert(self):
        # getting the string from entry field and converting it into float  
        inputVal = float(self.input_field.get())  
        # getting the values from selection menus  
        input_unit = self.input_value.get()  
        output_unit = self.output_value.get()  
    
        # list of the required combination of the conversion factors  
        conversion_factors = [input_unit in self.length_units and output_unit in self.length_units,  
        input_unit in self.weight_units and output_unit in self.weight_units,  
        input_unit in self.temperature_units and output_unit in self.temperature_units,  
        input_unit in self.area_units and output_unit in self.area_units,  
        input_unit in self.volume_units and output_unit in self.volume_units]  
    
        if any(conversion_factors): # If both the units are of same type, perform the conversion  
            if input_unit == "celsius" and output_unit == "fahrenheit":  
                self.output_field.delete(0, END)  
                self.output_field.insert(0, (inputVal * 1.8) + 32)  
            elif input_unit == "fahrenheit" and output_unit == "celsius":  
                self.output_field.delete(0, END)  
                self.output_field.insert(0, (inputVal - 32) * (5/9))  
            else:  
                self.output_field.delete(0, END)  
                self.output_field.insert(0, round(inputVal * self.unitDict[input_unit] / self.unitDict[output_unit], 5))  
    
        else:  
            # displaying error if units are of different types  
            self.output_field.delete(0, END)  
            self.output_field.insert(0, "Error: Units are different types.")  
        
        # Append conversion details to the history list
        history_entry = f"{inputVal} {input_unit} = {self.output_field.get()} {output_unit}\n"
        self.conversion_history.append(history_entry)

        # Update the conversion history displayed in the Text widget
        self.update_history()
        self.save_conversion_history()

    def add_digit(self, digit):
        current_value = self.input_field.get()
        self.input_field.insert(END, digit)

    def delete_character(self):
        current_value = self.input_field.get()
        self.input_field.delete(len(current_value) - 1, END)

    def update_history(self):
        # Clear the history text widget and update it with the latest conversion history
        self.history_text.delete(1.0, END)
        for entry in self.conversion_history:
            self.history_text.insert(END, entry)

    def load_conversion_history(self):
        try:
            with open("conversion_history.txt", "r") as file:
                self.conversion_history = file.readlines()
        except FileNotFoundError:
            self.conversion_history = []

    def save_conversion_history(self):
        with open("conversion_history.txt", "w") as file:
            file.writelines(self.conversion_history)
    
    def show_history(self):
            # Create a new window for history
            history_window = Toplevel(self.root)
            history_window.title("Conversion History")
            history_window.geometry("400x300")
            
            # Read history from the file
            try:
                with open('conversion_history.txt', 'r') as history_file:
                    history_data = history_file.readlines()
            except FileNotFoundError:
                history_data = []
            except Exception as e:
                # Handle other exceptions with a generic error message
                messagebox.showerror("Error", f"An error occurred: {e}")

            # Display history in a Text widget
            history_text = Text(history_window, wrap=WORD)
            history_text.pack(expand=YES, fill=BOTH)

            for entry in history_data:
                history_text.insert(END, entry)

            # Disable text editing in the history window
            history_text.config(state=DISABLED)

if __name__ == "__main__":
    root = Tk()
    app = UnitConverter(root)
    root.mainloop()
