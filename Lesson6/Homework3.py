import datasource2

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
        ttk.Label(topFrame,text='空氣品質指標(AQI)(歷史資料)',style='TopFrame.TLabel').pack()
        topFrame.pack(padx=20,pady=20)
        
        #==============end topFrame===============

        #==============bottomFrame===============
        bottomFrame = ttk.Frame(self)

        val = tk.StringVar(value='old_data')
        radio_btn1 = tk.Radiobutton(bottomFrame, text='既有資料',variable=val, value='old_data')
        radio_btn1.pack(side='left',expand=True,anchor='n')
        radio_btn2 = tk.Radiobutton(bottomFrame, text='最新資料',variable=val, value='new_data')
        radio_btn2.pack(side='left',expand=True,anchor='n')

        # 監聽 Radiobutton 變化
        def on_radio_change(*args):
            if val.get() == 'old_data':
                self.data, self.sitenames = datasource2.fetch_old_data()
            elif val.get() == 'new_data':
                self.data, self.sitenames = datasource2.get_new_data()
            sitenames_cb['values'] = self.sitenames  # 更新 Combobox 的值

        val.trace('w', on_radio_change)

        # 預設加載舊資料
        self.data, self.sitenames = datasource2.fetch_old_data()

        self.selected_site = tk.StringVar()
        sitenames_cb = ttk.Combobox(bottomFrame, textvariable=self.selected_site,values=self.sitenames,state='readonly')
        self.selected_site.set('請選擇站點')
        sitenames_cb.bind('<<ComboboxSelected>>', self.sitename_selected)
        sitenames_cb.pack(side='left',expand=True,anchor='n')        

        # define columns and tree
        columns = ('date', 'county', 'aqi', 'pm25','status','lat','lon')
        self.tree = ttk.Treeview(bottomFrame, columns=columns, show='headings')

        # define headings
        self.tree.heading('date', text='日期')
        self.tree.heading('county', text='縣市')
        self.tree.heading('aqi', text='AQI')
        self.tree.heading('pm25', text='PM25')
        self.tree.heading('status',text='狀態')
        self.tree.heading('lat', text='緯度')
        self.tree.heading('lon', text='經度')

        self.tree.column('date', width=150,anchor="center")
        self.tree.column('county', width=80,anchor="center")
        self.tree.column('aqi', width=50,anchor="center")
        self.tree.column('pm25', width=50,anchor="center")
        self.tree.column('status', width=50,anchor="center")
        self.tree.column('lat', width=100,anchor="center")
        self.tree.column('lon', width=100,anchor="center")
        self.tree.pack(side='right')
        bottomFrame.pack(expand=True,fill='x',padx=20,pady=(0,20),ipadx=10,ipady=10)

            #==============end bottomFrame===============

    def sitename_selected(self,event):
        selected = self.selected_site.get()
        selected_data = datasource2.get_selected_data(selected, self.data)
        self.tree.delete(*self.tree.get_children())  # 清空 Treeview
        for record in selected_data:
            self.tree.insert("", "end", values=record)

def main():
    window = Window(theme="arc")
    window.mainloop()

if __name__ == '__main__':
    main()