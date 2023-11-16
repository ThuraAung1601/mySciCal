from tkinter import *
from tkinter import messagebox
from utils import BackEnd

light_grey = "#B8B8B8"
dark_grey = "#535353"

class UnitConverter(BackEnd):
    def __init__(self, root):
        BackEnd.__init__(self)
        self.root = root
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

    def create_gui(self):
        self.root.title("Unit Converter")
        self.root.geometry("450x320")
        self.root.resizable(False, False)
        self.root.configure(bg=light_grey)

        self.top_frame = Frame(self.root, bg=light_grey)
        self.top_frame.grid(row=0, column=0, sticky=NSEW)
        
        self.about = Button(self.top_frame, text="ABOUT", bg=light_grey, fg=dark_grey, font=("Segoe UI", 14, 'bold'), borderwidth=3, padx=4, command=self.display_about)
        self.reset_button = Button(self.top_frame, text="RESET", bg=light_grey, fg=dark_grey, font=("Segoe UI", 14, 'bold'), borderwidth=3, padx=4, command=self.reset)
        self.about.grid(row=1, column=1)
        self.reset_button.grid(row=1, column=3)
        
        self.bottom_frame = Frame(self.root, bg=light_grey)
        self.bottom_frame.grid(row=1, column=0, sticky=NSEW)
        
        self.input_value = StringVar()
        self.output_value = StringVar()
        self.input_value.set(self.SELECTIONS[0])
        self.output_value.set(self.SELECTIONS[0])

        # creating the labels for the body of the main window  
        self.input_label = Label(  
            self.bottom_frame,  
            text = "From:",  
            bg = light_grey,  
            fg = dark_grey,
            font=("Segoe UI", 14, 'bold')
        )  
        self.output_label = Label(  
            self.bottom_frame,  
            text = "To:",  
            bg = light_grey,  
            fg = dark_grey,
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
        self.buttons_frame = Frame(self.bottom_frame, bg=dark_grey)
        for i, row_buttons in enumerate(self.buttons):
            for j, button_text in enumerate(row_buttons):
                button = Button(
                    self.buttons_frame,
                    text=button_text,
                    bg=light_grey,
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
            self.output_field.insert(0, "ERROR")  

    def add_digit(self, digit):
        current_value = self.input_field.get()
        self.input_field.insert(END, digit)

    def delete_character(self):
        current_value = self.input_field.get()
        self.input_field.delete(len(current_value) - 1, END)

if __name__ == "__main__":
    root = Tk()
    app = UnitConverter(root)
    root.mainloop()