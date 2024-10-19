from ttkthemes import ThemedTk
from tkinter import ttk

class Window(ThemedTk):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.title('使用ttk的套件')
        self.geometry('400x300')
        #設定主題，跟老師所提供的做法不同
        self.set_theme("Breeze")  # 使用 set_theme() 方法來套用主題

        #設定樣式
        style = ttk.Style(self)        
        style.configure('Main.TButton',font=('Arial',15))

        #建立按鈕
        btn1 = ttk.Button(self,text="Button Demo",style='Main.TButton')
        btn1.pack(ipadx=10,ipady=10,padx=10,pady=10)

def main():
    window = Window()
    window.mainloop()

if __name__ == '__main__':
    main()