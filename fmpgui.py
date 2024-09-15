import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from functools import partial


class App(tk.Tk):
   
    def __init__(self):
        super().__init__()
        
        self.set_style()
        self.set_layout(width = 800, height = 1000, title="Redwood project")
        
        self.create_menu()
        self.create_work_frame()

        
        
    def set_style(self):
        # Create a custom font
        custom_font = tkFont.Font(family="Calibry", size=13)
        self.style = ttk.Style(self)
        self.style.configure('TButton', font = custom_font, background = 'lightsteelblue')
        self.style.configure('TLabel', font = custom_font)
        self.style.configure('WorkFrame.TFrame', font = custom_font, background = 'steelblue' )
       

    def set_layout(self, width, height, title):
        #-------------------------------------------------------
        # Set root window size and position in the screen center
        #-------------------------------------------------------
        
        window_width = width
        window_height = height
        self.title(title)
        self['bg'] = 'lightsteelblue'

        # get the screen dimension
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # find the center point
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)

        # set the position of the window to the center of the screen
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        # set layout
        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 0)
        self.rowconfigure(1, weight = 1)
        
        
    def create_menu(self):
        def menu_action(action):
            print(action)
            if action == 'exit':
                self.destroy()
            if action == 'portfolio':
                self.create_portfolio_frame()
        
        menu_frame = tk.Frame(master = self, borderwidth=1, background = 'lightsteelblue')
        menu_frame.grid(row = 0, sticky=tk.W)
        ttk.Button(menu_frame, text='Analyze',
                   command = partial(menu_action, 'analize'),
                   ).grid(column = 0, row = 0, sticky=tk.W, padx=5, pady=5)
        ttk.Button(menu_frame, text='Review candidates',
                   command = partial(menu_action, "watchlist"),
                  ).grid(column = 1, row = 0, sticky=tk.W)
        ttk.Button(menu_frame, text='Portfolio', 
                   command = partial(menu_action, 'portfolio')).grid(column = 2, row = 0, sticky=tk.W)
        ttk.Button(menu_frame, text='Exit', command = partial(menu_action, 'exit')
                   ).grid(column = 3, row = 0, sticky=tk.E)
    
    def create_work_frame(self):
        
        self.work_frame = ttk.Frame(master = self, borderwidth=0, 
                                    relief='solid', style = 'WorkFrame.TFrame')
        self.work_frame.grid(row = 1, sticky=tk.NSEW)
    
    def create_portfolio_frame(self):
        #simbol_frame = tk.Frame(master = self.work_frame, borderwidth=1, background = 'gray67', height = 80, relief='solid'
        #                        ).grid(row = 1, sticky=tk.NSEW)
    
        pass
    
    #def menu_action(self, action):
    #    print(action)
    #    lbl = ttk.Label(self.simbol_frame, text = "Portfolio", background='yellow').grid(column = 0, row = 0, sticky=tk.EW)
    #    
    #    if action == "candidates":
    #        self.simbol_frame.destroy()
    #    #ttk.Button(frame, text='FSPTX').grid(column = 0, row = 1)
    #    #ttk.Button(frame, text='FSSEL', command = partial(self.menu_action, "OOOO")).grid(column = 0, row = 2)
    
    #def create_menu_frame(self):
    #    frame = ttk.Frame(master = self,width = 40, heigh = 200,borderwidth=1, relief='solid')
    #    ttk.Button(frame, text='Analyze', command = partial(self.menu_action, 'analize')).grid(column = 0, row = 0)
    #    ttk.Button(frame, text='Review candidates', command = partial(self.menu_action, "candidates")).grid(column = 1, row = 0)
    #    ttk.Button(frame, text='Portfolio', command = partial(self.menu_action, 'portfolio')).grid(column = 2, row = 0)
    #    return frame
    
    #def create_simbol_frame(self):
    #    frame = ttk.Frame(self)
    #    #ttk.Label(frame, text = "Portfolio").grid(column = 0, row = 0)
    #    #ttk.Button(frame, text='FSPTX').grid(column = 0, row = 1)
    #    #ttk.Button(frame, text='FSSEL', command = partial(self.menu_action, "OOOO")).grid(column = 0, row = 2)
    #    return frame
    
    #def create_plot_frame(self):      
    #    frame = ttk.Frame(self)
    #    #ttk.Label(frame, text = "Simbols").grid(column = 0, row = 0)
    #    #ttk.Button(frame, text='FSPTX').grid(column = 0, row = 1)
    #    #ttk.Button(frame, text='FSSEL', command = partial(self.menu_action, "OOOO")).grid(column = 0, row = 2)
    #    return frame
    
    
    #def create_list_of_simbols(self):
    #    frame = ttk.Frame(self, bg='blue')
    #    #if type_of_list == 'portfolio':


if __name__ == "__main__":
    app = App()
    app.mainloop()