import tkinter as tk
from tkinter import ttk

class Window(tk.Tk):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.title('使用ttk的套件')
        self.geometry('400x300')
        style = ttk.Style(self)
        style.configure('TLabel',font=('Helvetica', 11)) #修改現有的
        style.configure('Title.TLabel',font=('Helvetica', 15),background="lightblue",foreground='red') #自訂的style
        message = ttk.Label(self,text='使用ttk的Label',style='Title.TLabel') #使用自訂的
        print(message.winfo_class())
        message.pack()
        style.configure('Main.TButton', font= ('Arial',15))
        btn1 = ttk.Button(self, text = "Button Demo")
        btn1.pack(ipadx= 10, ipady= 50, padx= 110, pady= 50) 
        #ipadx 盒內距, i= internal, x為水平, y為垂直
        #padx 盒外距, x為水平, y為垂直

def main():
    window = Window()
    window.mainloop()

if __name__ == '__main__':
    main()