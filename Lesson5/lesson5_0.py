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
        self.btn1 = ttk.Button(topFrame,text="按鈕1", command = self.click1)
        self.btn1.pack(side='left',expand=True,fill='x',padx=10)
        btn2 = ttk.Button(topFrame,text="按鈕2", command = self.click2)
        btn2.pack(side='left',expand=True,fill='x')
        btn3 = ttk.Button(topFrame,text="按鈕3", command = self.click3)
        btn3.pack(side='left',expand=True,fill='x',padx=10)
        topFrame.pack(padx=10,pady=(10,0),ipadx=10,ipady=10,expand=True,fill='x')

        bottomFrame = ttk.Frame(self,borderwidth=1,relief='groove')

        bottomFrame1 = ttk.Frame(bottomFrame,borderwidth=1,relief='groove')
        btn4 = ttk.Button(bottomFrame1,text="按鈕4",style='underline.TButton')
        btn4.bind('<ButtonRelease>',self.left_button_click)
        btn4.pack(expand=True,fill='y',pady=(10,0))
        btn5 = ttk.Button(bottomFrame1,text="按鈕5",style='underline.TButton')
        btn5.pack(expand=False,fill='y',pady=(10,0))
        btn6 = ttk.Button(bottomFrame1,text="按鈕6",style='underline.TButton')
        btn6.pack(expand=False,fill='y',pady=10)
        bottomFrame1.pack(side='left',padx=10,pady=(10,0),ipadx=10,ipady=10,expand=True,fill='both')

        bottomFrame2 = ttk.Frame(bottomFrame,borderwidth=1,relief='groove')
        btn7 = ttk.Button(bottomFrame2,text="按鈕7",style='italic.TButton')
        btn7.pack(expand=True,fill='y',pady=(10,0))
        btn8 = ttk.Button(bottomFrame2,text="按鈕8",style='italic.TButton')
        btn8.pack(expand=False,fill='y',pady=(10,0))
        btn9 = ttk.Button(bottomFrame2,text="按鈕9",style='italic.TButton')
        btn9.pack(expand=True,fill='y',pady=10)
        bottomFrame2.pack(side='left',padx=10,pady=(10,0),ipadx=10,ipady=10,expand=True,fill='both')

        bottomFrame3 = ttk.Frame(bottomFrame,borderwidth=1,relief='groove')
        btn10 = ttk.Button(bottomFrame3,text="按鈕10",style='bold.TButton')
        btn10.pack(expand=True,fill='y',pady=(10,0))
        btn11 = ttk.Button(bottomFrame3,text="按鈕11",style='bold.TButton')
        btn11.pack(expand=True,fill='y',pady=(10,0))
        btn12 = ttk.Button(bottomFrame3,text="按鈕12",style='bold.TButton')
        btn12.pack(expand=True,fill='y',pady=10)
        bottomFrame3.pack(side='left',padx=10,pady=(10,0),ipadx=10,ipady=10,expand=True,fill='both')

        bottomFrame.pack(padx=10,pady=(10,0),ipadx=10,ipady=10,expand=True,fill='both')

    def click1(self):
        self.btn1.configure(text="被按了")
        print('Hello body1')

    def click2(self):
        print('Hello dude2')

    def click3(self):
        print('Hello gorgeous3')
    def left_button_click(self,event):
        print(type(event))
        print(event.x)
        print(event.y)
        print(event.width)
        print(event.widget.configure(text="被按了"))


def main():
    window = Window(theme="arc")
    window.mainloop()

if __name__ == '__main__':
    main()