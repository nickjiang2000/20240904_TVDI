from ttkthemes import ThemedTk
from tkinter import ttk

class Window(ThemedTk):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.title('使用ttk的套件')
        style = ttk.Style(self)
        style.configure('underline.TButton',font=("Calibri",15,"underline"),foreground="blue")
        style.configure('italic.TButton',font=("Calibri",15,"italic"),foreground="lightblue")
        style.configure('bold.TButton',font=("Calibri",15,"bold"),foreground="sky blue")
        
        topFrame = ttk.Frame(self,borderwidth=1,relief='groove')
        btn1 = ttk.Button(topFrame,text="按鈕1")
        btn1.pack(side='left',expand=True,fill='x',padx=10)
        btn2 = ttk.Button(topFrame,text="按鈕2")
        btn2.pack(side='left',expand=True,fill='x')
        btn3 = ttk.Button(topFrame,text="按鈕3")
        btn3.pack(side='left',expand=True,fill='x',padx=10)
        topFrame.pack(padx=10,pady=(10,0),ipadx=10,ipady=10,expand=True,fill='x')

        bottomFrame = ttk.Frame(self,borderwidth=1,relief='groove')

        bottomFrame1 = ttk.Frame(bottomFrame,borderwidth=1,relief='groove')
        btn4 = ttk.Button(bottomFrame1,text="按鈕4",style='underline.TButton')
        btn4.pack(expand=True,fill='y',padx=10)
        btn5 = ttk.Button(bottomFrame1,text="按鈕5",style='underline.TButton')
        btn5.pack(expand=False,fill='y',padx=10)
        btn6 = ttk.Button(bottomFrame1,text="按鈕6",style='underline.TButton')
        btn6.pack(expand=False,fill='y',padx=10)
        bottomFrame1.pack(side='left',padx=10,pady=(10,0),ipadx=10,ipady=10,expand=True,fill='y')

        bottomFrame2 = ttk.Frame(bottomFrame,borderwidth=1,relief='groove')
        btn7 = ttk.Button(bottomFrame2,text="按鈕7",style='italic.TButton')
        btn7.pack(expand=True,fill='y',padx=10)
        btn8 = ttk.Button(bottomFrame2,text="按鈕8",style='italic.TButton')
        btn8.pack(expand=False,fill='y',padx=10)
        btn9 = ttk.Button(bottomFrame2,text="按鈕9",style='italic.TButton')
        btn9.pack(expand=True,fill='y',padx=10)
        bottomFrame2.pack(side='left',padx=10,pady=(10,0),ipadx=10,ipady=10,expand=True,fill='y')

        bottomFrame3 = ttk.Frame(bottomFrame,borderwidth=1,relief='groove')
        btn10 = ttk.Button(bottomFrame3,text="按鈕10",style='bold.TButton')
        btn10.pack(expand=True,fill='y',padx=10)
        btn11 = ttk.Button(bottomFrame3,text="按鈕11",style='bold.TButton')
        btn11.pack(expand=True,fill='y',padx=10)
        btn12 = ttk.Button(bottomFrame3,text="按鈕12",style='bold.TButton')
        btn12.pack(expand=True,fill='y',padx=10)
        bottomFrame3.pack(side='left',padx=10,pady=(10,0),ipadx=10,ipady=10,expand=True,fill='y')

        bottomFrame.pack(padx=10,pady=(10,0),ipadx=10,ipady=10,expand=True,fill='y')

def main():
    window = Window(theme="arc")
    window.mainloop()

if __name__ == '__main__':
    main()