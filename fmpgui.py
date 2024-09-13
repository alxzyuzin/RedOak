import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from functools import partial


class App(tk.Tk):
   
    def __init__(self):
        super().__init__()
        
        # Create a custom font
        custom_font = tkFont.Font(family="Calibry", size=13)
        self.title("Redwood project")
        
        self.style = ttk.Style(self)
        self.style.configure('TButton', font = custom_font)
        #-------------------------------------------------------
        # Set root window size and position in the screen center
        #-------------------------------------------------------
        window_width = 800
        window_height = 1000

        # get the screen dimension
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # find the center point
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)

        # set the position of the window to the center of the screen
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        
        # Configure the grid
        # Split main window on three parts
        #   - top row from side to side
        #   - left column for list of simbols
        #   -right column for indicators
     
        self.rowconfigure(0, weight=1)
        self.rowconfigure(10, weight= 10)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=10)

        menu_frame = self.create_menu_frame(self).grid(column=0, row=0, sticky=tk.NW)
        simbol_frame = self.create_simbol_frame(self).grid(column=0, row=1)
        plot_frame = self.create_plot_frame(self).grid(column=1, row=1)
    

    def create_menu_frame(self, container):
        frame = ttk.Frame(container)
        ttk.Button(frame, text='Analyze', command = partial(self.menu_action, 'analize')).grid(column = 0, row = 0)
        ttk.Button(frame, text='Review candidates', command = partial(self.menu_action, "candidates")).grid(column = 1, row = 0)
        ttk.Button(frame, text='Portfolio', command = partial(self.menu_action, 'portfolio')).grid(column = 2, row = 0)
        return frame
    
    def create_simbol_frame(self,container):
        frame = ttk.Frame(container)
        #ttk.Label(frame, text = "Portfolio").grid(column = 0, row = 0)
        #ttk.Button(frame, text='FSPTX').grid(column = 0, row = 1)
        #ttk.Button(frame, text='FSSEL', command = partial(self.menu_action, "OOOO")).grid(column = 0, row = 2)
        return frame
    
    def create_plot_frame(self,container):      
        frame = ttk.Frame(container)
        #ttk.Label(frame, text = "Simbols").grid(column = 0, row = 0)
        #ttk.Button(frame, text='FSPTX').grid(column = 0, row = 1)
        #ttk.Button(frame, text='FSSEL', command = partial(self.menu_action, "OOOO")).grid(column = 0, row = 2)
        return frame
    
    def menu_action(self, action):
        print(action)
    #def create_list_of_simbols(self):
    #    frame = ttk.Frame(self, bg='blue')
    #    #if type_of_list == 'portfolio':


if __name__ == "__main__":
    app = App()
    app.mainloop()