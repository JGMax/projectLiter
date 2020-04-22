from tkinter import *
import tkinter.ttk as ttk
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import pandas as pd
import matplotlib.transforms as mtransforms
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

languages = ["Пуш", "До", "Лерм", "Куп", "Бл", "Толс","Бу", "Салт", "Пр", "Нек", "Ес", "Кап", "Мо","Пре", "Со", "Фе"]
datalst = [31, 41, 59, 26, 53, 58, 97, 96, 36]

#создание вкладок
def tabs(name):
    nb = ttk.Notebook(width=490,height=430)
    nb.grid(row=2,column=4,columnspan=4, rowspan=4,ipadx=3, ipady=2, sticky=N, padx=2,pady=2)

    f1 = ttk.Frame(nb)
    name.append(f1)
    f2 = ttk.Frame(nb)
    name.append(f2)
    f3 = ttk.Frame(nb)
    name.append(f3)

    nb.add(f1, text='Текст')
    nb.add(f2, text='Гистограмма')
    nb.add(f3, text='График')

#посторение графика
def graph(f3):
    f=Figure(figsize=(5,5))
    a=f.add_subplot(111)
    a.plot(["Пуш", "До", "Лерм", "Куп", "Бл", "Толс","Бу", "Салт"],[5,6,4,2,8,6,4,1],color='#228B22')
    canvas=FigureCanvasTkAgg(f,f3)
    canvas.draw()
    canvas.get_tk_widget().pack()
# построение гистограммы
def hist(f2,datalst):
    ff = Figure(figsize=(5,5), dpi=100)
    xx = ff.add_subplot(111)
    ind = np.arange(len(datalst))
    rects1 = xx.bar(ind, datalst, 0.8,color="#DC143C")
    canvas = FigureCanvasTkAgg(ff, master=f2)
    canvas.draw()
    canvas.get_tk_widget().pack()

#listbox с авторами
def listbox_author():
    authors_listbox = Listbox(width=40, height=15)
    vsb = Scrollbar(orient="vertical", command=authors_listbox.yview)
    vsb.grid(row=2, column=2, sticky='ns')
    authors_listbox.configure(yscrollcommand=vsb.set)
    for language in languages:
        authors_listbox.insert(END, language)
    authors_listbox.grid(row=2,column=0,columnspan=2, ipadx=3, ipady=2, sticky=N, padx=2,pady=2)

#listbox с произведениями
def listbox_poems():
    poems_listbox = Listbox(width=40,height=10)
    vsb1 = Scrollbar(orient="vertical", command=poems_listbox.yview)
    vsb1.grid(row=4, column=2, sticky='ns')
    poems_listbox.configure(yscrollcommand=vsb1.set)
    for language in languages:
        poems_listbox.insert(END, language)
    poems_listbox.grid(row=4,column=0,columnspan=2, ipadx=3, ipady=2, sticky=N, padx=2,pady=2)

#названия
def labels():
    label1 = Label(text="Авторы", fg="#eee", bg="#333")
    label1.grid(row=1,column=0,columnspan=2, ipadx=3, ipady=2, sticky=W, padx=2,pady=2)
    label2 = Label(text="Произведения", fg="#eee", bg="#333")
    label2.grid(row=3,column=0,columnspan=2, ipadx=3, ipady=2, sticky=W, padx=2,pady=2)
    label3 = Label(text="Результат исследования", fg="#eee", bg="#333")
    label3.grid(row=1,column=4,columnspan=4, ipadx=3, ipady=2, sticky=W, padx=2,pady=2)

#кнопки
def bottoms(root):
    but=Button(root,text='Существ')
    but1=Button(root,text='Глагол')
    but2=Button(root,text='Прилагат')
    but3=Button(root,text='Очистить')
    but.grid(row=6,column=4, ipadx=3, ipady=2, padx=1,pady=2)
    but1.grid(row=6,column=5,ipadx=10, ipady=2, padx=1,pady=2)
    but2.grid(row=6,column=6, ipadx=10, ipady=2,  padx=1,pady=2)
    but3.grid(row=6,column=7, ipadx=10, ipady=2, padx=1,pady=2)

#главная часть
if __name__=='__main__':
    root = Tk()
    root.title("Анализ литературных произведений")
    root.geometry("780x600+270+20")
    tabs_name=[]
    labels()
    bottoms(root)
    listbox_author()
    listbox_poems()
    tabs(tabs_name)
    graph(tabs_name[2])
    hist(tabs_name[1],datalst)
    root.mainloop()