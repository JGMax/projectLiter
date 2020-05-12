from tkinter import *
import tkinter.ttk as ttk
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from time import sleep
#from WordAnalyser.main import main
from requests import author, namebooks
languages = ["Пуш", "До", "Лерм", "Куп", "Бл", "Толс","Бу", "Салт", "Пр", "Нек", "Ес", "Кап", "Мо", "Пре", "Со", "Фе"]
datalst = [31, 41, 59, 26, 53, 58, 97, 96, 36]
poems = ["Мастер и Маргарита", "Война и мир", "Преступление и наказание"]
text_wap = 'Так говорила в июле 1805 года известная\n Анна Павловна Шерер, фрейлина и приближенная императрицы\n ' \
         'Марии Феодоровны, встречая важного и чиновного\n князя Василия, первого приехавшего на ее вечер. '
help_text = 'Выберите автора в первом окне, затем его произведение во втором!!!'
message = ''
biography = 'Lev Nikolaevich Tolstoy\nBorn: 9 September 1828\nDied: 20 November 1910 (aged 82)\nLanguage: Russian\n' \
            'Resting place: Yasnaya Polyana'


def tabs(name):
    nb = ttk.Notebook(width=490,height=430)
    nb.grid(row=2, column=4, columnspan=4, rowspan=4, ipadx=3, ipady=2, sticky=N, padx=2,pady=2)

    f1 = Canvas(nb)
    name.append(f1)
    f2 = ttk.Frame(nb)
    name.append(f2)
    f3 = ttk.Frame(nb)
    name.append(f3)
    #text(f1, help_text)

    nb.add(f1, text='Текст')
    nb.add(f2, text='Гистограмма')
    nb.add(f3, text='График')


def graph(f3):
    f = Figure(figsize=(5, 5))
    a = f.add_subplot(111)
    a.plot(["Пуш", "До", "Лерм", "Куп", "Бл", "Толс", "Бу", "Салт"], [5, 6, 4, 2, 8, 6, 4, 1], color='#228B22')
    canvas = FigureCanvasTkAgg(f, f3)
    canvas.draw()
    canvas.get_tk_widget().pack()


def hist(f2, data):
    ff = Figure(figsize=(5, 5), dpi=100)
    xx = ff.add_subplot(111)
    ind = np.arange(len(data))
    xx.bar(ind, data, 0.8, color="#DC143C")
    canvas = FigureCanvasTkAgg(ff, master=f2)
    canvas.draw()
    canvas.get_tk_widget().pack()


def text(f1, text_message):
    global message
    f1.delete(message)
    message = f1.create_text(10, 10, anchor=NW, text=text_message, fill="#000000")


def cur_select_authors(evn):
    w = evn.widget
    i, value = 0, ''
    if w.curselection() != ():
        i = int(w.curselection()[0])
        value = w.get(i)
    if value and value in author:
        text(tabs_name[0], biography)
    print_poems(listbox_poems())


def cur_select_poems(evn):
    global tabs_name
    wid = evn.widget
    i, value = 0, ''
    if wid.curselection() != ():
        i = int(wid.curselection()[0])
        value = wid.get(i)
    if value and value not in languages:
        text(tabs_name[0], text_wap)


def listbox_author():
    authors_listbox = Listbox(width=40, height=15, selectmode=SINGLE, exportselection=0)
    vsb = Scrollbar(orient="vertical", command=authors_listbox.yview)
    vsb.grid(row=2, column=2, sticky='ns')
    authors_listbox.configure(yscrollcommand=vsb.set)
    authors_listbox.bind('<<ListboxSelect>>', cur_select_authors)
    for writer in author:
        authors_listbox.insert(END, writer)
    authors_listbox.grid(row=2, column=0, columnspan=2, ipadx=3, ipady=2, sticky=N, padx=2, pady=2)


def listbox_poems():
    poems_listbox = Listbox(width=40, height=10)
    vsb1 = Scrollbar(orient="vertical", command=poems_listbox.yview)
    vsb2 = Scrollbar(orient="horizontal", command=poems_listbox.xview)
    vsb1.grid(row=4, column=2, sticky='ns')
    vsb2.grid(row=5, column=0, columnspan=2, sticky='ew')
    poems_listbox.configure(yscrollcommand=vsb1.set)
    poems_listbox.configure(xscrollcommand=vsb2.set)
    poems_listbox.bind('<<ListboxSelect>>', cur_select_poems)
    poems_listbox.grid(row=4, column=0, columnspan=2, ipadx=3, ipady=2, sticky=N, padx=2, pady=2)
    return poems_listbox


def print_poems(poems_listbox):
    for row in namebooks:
        poems_listbox.insert(END, row)


def labels():
    label1 = Label(text="Авторы", fg="#eee", bg="#333")
    label1.grid(row=1, column=0, columnspan=2, ipadx=3, ipady=2, sticky=W, padx=2, pady=2)
    label2 = Label(text="Произведения", fg="#eee", bg="#333")
    label2.grid(row=3, column=0, columnspan=2, ipadx=3, ipady=2, sticky=W, padx=2, pady=2)
    label3 = Label(text="Результат исследования", fg="#eee", bg="#333")
    label3.grid(row=1, column=4, columnspan=4, ipadx=3, ipady=2, sticky=W, padx=2, pady=2)


def bottoms(r):
    but = Button(r, text='Существ')
    but1 = Button(r, text='Глагол')
    but2 = Button(r, text='Прилагат')
    but3 = Button(r, text='Очистить')
    but.grid(row=6, column=4, ipadx=3, ipady=2, padx=1, pady=2)
    but1.grid(row=6, column=5, ipadx=10, ipady=2, padx=1, pady=2)
    but2.grid(row=6, column=6, ipadx=10, ipady=2,  padx=1, pady=2)
    but3.grid(row=6, column=7, ipadx=10, ipady=2, padx=1, pady=2)


def loading(r):
    p = ttk.Progressbar(r, orient=HORIZONTAL, length=200, mode="determinate", takefocus=True, maximum=100)
    label = Label(text="Loading...", fg="#000000")
    label.pack(expand=1, anchor=S)
    p.pack(expand=1, anchor=N)
    for i in range(100):
        sleep(0.05)
        p.step()
        r.update()
    for ele in r.winfo_children():
        ele.destroy()

if __name__ == '__main__':
    root = Tk()
    root.title("Анализ литературных произведений")
    root.geometry("780x600+270+20")
    loading(root)
    tabs_name = []
    labels()
    listbox_author()
    listbox_poems()
    tabs(tabs_name)
    bottoms(root)
    graph(tabs_name[2])
    hist(tabs_name[1], datalst)
    #main()
    root.mainloop()
