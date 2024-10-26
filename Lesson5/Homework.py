from tkinter import ttk
import tkinter as tk
from ttkthemes import ThemedTk
from tkinter.messagebox import showinfo

class Window(ThemedTk):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('登入')
        #==============style===============
        style = ttk.Style(self)
        style.configure('TopFrame.TLabel',font=('Helvetica',20))
        #============end style===============
        
        #==============top Frame===============

        topFrame = ttk.Frame(self)
        ttk.Label(topFrame,text='國破山河在，城春草木深。',style='TopFrame.TLabel').pack()
        topFrame.pack(padx=20,pady=20)
        
        #==============end topFrame===============

        #==============bottomFrame===============
        # https://www.pythontutorial.net/tkinter/tkinter-checkbox/
        bottomFrame = ttk.Frame(self)
        self.agreement = tk.StringVar()
        
        ttk.Checkbutton(bottomFrame,
                text='I agree',
                command=self.agreement_changed,
                variable=self.agreement,
                onvalue='感時花濺淚，恨別鳥驚心。',
                offvalue='峰火連三月，家書抵萬金。').pack()
        
        bottomFrame.pack(expand=True,fill='x',padx=20,pady=(0,20),ipadx=10,ipady=10)
        #==============end bottomFrame===============

    def agreement_changed(self):
        showinfo(
            title='Result',
            message=self.agreement.get())
        

def main():
    window = Window(theme="arc")
    window.mainloop()

if __name__ == '__main__':
    main()