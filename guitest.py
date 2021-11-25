from ttkbootstrap import Style
import tkinter as tk
from tkinter import ttk

class Application(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.title('Solar System Simulation')
        self.style = Style(theme='darkly')
        self.welcome = WelcomeScreen(self)
        self.welcome.pack(fill='both', expand='yes')
        
class WelcomeScreen(ttk.Frame):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(padding=(20,10))
        self.columnconfigure(2, weight=1)
        ttk.Label(master=self, text='Welcome to Python Solar System Simulation v0.1', width=35).grid(columnspan=4, pady=5)
        for i, label in enumerate(['Please Select Mode']):
            ttk.Label(master=self, text=label.title()).grid(row=i + 1, column=2, sticky='ew', pady=10, padx=(0, 10))
        self.regular = ttk.Button(master=self, text='Regular',command=self.regularmode).grid(row=4, column=1, sticky=tk.EW, pady=10, padx=(0, 10))
        self.sandbox = ttk.Button(master=self, text='Sandbox', command=self.sandboxmode).grid(row=4, column=3, sticky=tk.EW, pady=10, padx=(0, 3))
        
    def regularmode(self):
        print("normal")
        self.quit()
        
        
    def sandboxmode(self):
        print("sandbox")
        self.quit()
            
if __name__ == '__main__':
    Application().mainloop()
    
print("success")