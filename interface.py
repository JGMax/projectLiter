from tkinter import *
import tkinter.ttk as ttk
import numpy as np
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from time import sleep
import codecs
from projectLiter.WordAnalyser.results_keys import morph_statistic_key, morph_posts_key, \
    characters_key, frequency_key, dict_of_words_key
import threading
import queue
from projectLiter.WordAnalyser.word_analyser import text_analysis
from projectLiter.requests import SearchAboutAuthor, SearchBook
matplotlib.use("TkAgg")
author = ['Антон Чехов', 'Лев Толстой', 'Иван Тургенев', 'Николай Гоголь', 'Александр Куприн',
          'Михаил Булгаков', 'Максим Горький', 'Виктор Астафьев', 'Александр Солженицын', 'Федор Достоевский']
characters = ["Пуш", "До", "Лерм", "Куп", "Бл", "Толс","Бу", "Салт", "Пр", "Нек", "Ес", "Кап", "Мо", "Пре", "Со", "Фе"]
datalst = [31, 41, 59, 26, 53, 58, 97, 96, 36]
help_text = "Welcome to the literary analysis application.\n" \
            "Here you can see the writer's biography, find his poems, and also analyze:\n" \
            "find characters, top of the most popular words, and also a dictionary of vocabulary.\n" \
            "First, you must select the author’s name from the top list and select a work \n" \
            "from the second list."
help_text1 = 'Here you can find out the main characters of the work, as well as see the frequency\n' \
             'of their occurrence in each chapter.'
help_text2 = 'Here you can see the amount of each part of speech in a work, and also see the top of\n' \
             'the most popular words in a work'
message = ''
find = ()
book=''
result = {frequency_key: [],
          characters_key: [],
          morph_posts_key: [],
          morph_statistic_key: [],
          dict_of_words_key: []}


def tabs(name):
    nb = ttk.Notebook(width=470,height=430)
    nb.grid(row=2, column=4, columnspan=4, rowspan=4, ipadx=3, ipady=2, sticky=N, padx=2,pady=2)

    f1 = Canvas(nb)
    name.append(f1)
    f2 = Canvas(nb)
    name.append(f2)
    #create_combobox(f2)
    #f3 = ttk.Frame(nb)
    f3 = Canvas(nb)
    name.append(f3)
    vsb1 = Scrollbar(orient="vertical", command=f1.yview)
    vsb2 = Scrollbar(orient="horizontal", command=f1.xview)
    vsb1.grid(row=2, column=9, rowspan=6, sticky='ns')
    vsb2.grid(row=6, column=4, columnspan=4, sticky='ew')

    print_text(f1, help_text, 10, 'help')
    print_text(f2, help_text1, 40, 'help1')
    print_text(f3, help_text2, 40, 'help2')

    nb.add(f1, text='Text')
    nb.add(f2, text='Characters')
    nb.add(f3, text='Vocabulary')


def get_active_text(env):
    w = env.widget
    model = w.current()
    active = w.get()
    if model < 0:
        return None
    print(active)
    return active


def create_combobox(f2):
    combobox = ttk.Combobox(f2, values=result[characters_key],  exportselection=0)
    label1 = Label(f2, text="Выберите персонажа:", fg="#000000")
    label1.grid(row=0, column=2, columnspan=2, ipadx=3, ipady=2, sticky=W, padx=2, pady=2)
    combobox.grid(row=0, column=4, columnspan=2, ipadx=3, ipady=2, sticky=N, padx=2, pady=2)
    combobox.bind('<<ComboboxSelected>>', get_active_text)
    combobox.current(1)
    return combobox


def graph(f3, array1, array2):
    f = Figure(figsize=(3, 3))
    a = f.add_subplot(111)
    a.plot(array1, array2, color='#228B22')
    canvas = FigureCanvasTkAgg(f, f3)
    canvas.draw()
    canvas.get_tk_widget().grid(row=3, column=0, ipadx=3, ipady=2, padx=1, pady=2)


def hist(f2,  array1, array2, x, y):
    ff = Figure(figsize=(3, 3), dpi=100)
    xx = ff.add_subplot(111)
    ind = np.arange(len(array2))
    xx.bar(ind, array2, 0.8, color="#DC143C")
    canvas = FigureCanvasTkAgg(ff, master=f2)
    canvas.draw()
    canvas.get_tk_widget().grid(row=x+1, column=y, columnspan=7, ipadx=3, ipady=2, padx=1, pady=2)


def print_text(f, text_message, y, tag):
    global message
    print(message)
    f.delete(message)
    message = f.create_text(10, y, anchor=NW, text=text_message, fill="#000000", tag=tag)


def cur_select_authors(evn):
    global find
    w = evn.widget
    i, value = 0, ''
    if w.curselection() != ():
        i = int(w.curselection()[0])
        value = w.get(i)
    if value and value in author:
        '''que = queue.Queue()
        print(value)
        t = threading.Thread(target=lambda q, arg1: q.put(SearchAboutAuthor(arg1)), args=(que, value))
        t.start()
        t.join()
        find = que.get()'''
        find = SearchAboutAuthor(value)
        label1 = Label(tabs_name[0], text="Biography", fg="#000000")
        label1.grid(row=0, column=0, columnspan=5, ipadx=3, ipady=2, sticky=W, padx=2, pady=2)
        tabs_name[0].delete('help')
        print_text(tabs_name[0], find[0], 30, 'biogr')
        print_poems(listbox_poems(), find[1])


def cur_select_poems(evn):
    global tabs_name, book
    wid = evn.widget
    i, value = 0, ''
    if wid.curselection() != ():
        i = int(wid.curselection()[0])
        value = wid.get(i)
    if value and value not in author:
        '''que1 = queue.Queue()
        t = threading.Thread(target=lambda q, arg1, arg2, arg3: q.put(SearchBook(arg1, arg2, arg3)),
                             args=(que1, value, find[1], find[2]))
        t.start()
        t.join()
        book = que1.get()'''
        book = SearchBook(value, find[1], find[2])
        analyser(book, 'ru')
        but = Button(tabs_name[0], text='Book', command=print_book)
        but.grid(row=0, column=6, ipadx=3, ipady=2, padx=1, pady=2)


def print_book():
    label1 = Label(tabs_name[0], text="   Text    ", fg="#000000")
    label1.grid(row=0, column=0, columnspan=5, ipadx=3, ipady=2, sticky=S, padx=2, pady=2)
    with codecs.open(book, encoding='utf-8') as file:
        text = file.read()
    tabs_name[0].delete('biogr')
    print_text(tabs_name[0], text, 50, 'text')


def listbox_author():
    authors_listbox = Listbox(width=40, height=15, selectmode=SINGLE, exportselection=0)
    vsb = Scrollbar(orient="vertical", command=authors_listbox.yview)
    vsb.grid(row=2, column=2, sticky='ns')
    authors_listbox.configure(yscrollcommand=vsb.set)
    authors_listbox.bind('<<ListboxSelect>>', cur_select_authors)
    for writer in author:
        authors_listbox.insert(END, writer)
    authors_listbox.grid(row=2, column=0, columnspan=2, ipadx=3, ipady=2, sticky=N, padx=2, pady=2)


def analyser(book, language):
    global result
    result = text_analysis(book, language)


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


def print_poems(poems_listbox, books):
    for row in books:
        poems_listbox.insert(END, row)


def print_characters():
    answer = ''
    label1 = Label(tabs_name[1], text="Найденные персонажи:", fg="#000000")
    label1.grid(row=1, column=0, columnspan=5, ipadx=3, ipady=2, sticky=W, padx=2, pady=2)
    tabs_name[1].delete('help1')
    if result[characters_key]:
        for character in result[characters_key]:
            answer += str(character)
            answer += '\n'
        print_text(tabs_name[1], answer, 70, 'charact')
        create_combobox(tabs_name[1])
    else:
        print_text(tabs_name[1], 'Not found!', 70, 'not1')


def print_vocab():
    array1, array2 = [], []
    answer = ''
    label1 = Label(tabs_name[2], text="Найденные части речи:", fg="#000000")
    label1.grid(row=1, column=0, ipadx=3, ipady=2, sticky=W, padx=2, pady=2)
    tabs_name[2].delete('help2')
    if result[morph_posts_key]:
        for post in result[morph_posts_key]:
            array1.append(post)
            array2.append(int(result[morph_statistic_key][post]))
            answer += str(post + ' - ' + str(result[morph_statistic_key][post]))
            answer += '\n'
        print_text(tabs_name[2], answer, 70, 'vocab')
        hist(tabs_name[2], array1, array2, 1, 1)
    else:
        print_text(tabs_name[2], 'Not found!', 70, 'not2')


def labels():
    label1 = Label(text="Авторы", fg="#eee", bg="#333")
    label1.grid(row=1, column=0, columnspan=2, ipadx=3, ipady=2, sticky=W, padx=2, pady=2)
    label2 = Label(text="Произведения", fg="#eee", bg="#333")
    label2.grid(row=3, column=0, columnspan=2, ipadx=3, ipady=2, sticky=W, padx=2, pady=2)
    label3 = Label(text="Результат исследования", fg="#eee", bg="#333")
    label3.grid(row=1, column=4, columnspan=4, ipadx=3, ipady=2, sticky=W, padx=2, pady=2)


def bottoms(r):
    but = Button(r[1], text='Characters', command=print_characters)
    but1 = Button(r[2], text='Vocabulary', command=print_vocab)
    but2 = Button(r[2], text='Прилагат')
    but3 = Button(r[2], text='Очистить')
    but.grid(row=0, column=0, ipadx=3, ipady=2, padx=1, pady=2)
    but1.grid(row=0, column=0, ipadx=10, ipady=2, padx=1, pady=2)
    but2.grid(row=0, column=1, ipadx=10, ipady=2,  padx=1, pady=2)
    but3.grid(row=0, column=2, ipadx=10, ipady=2, padx=1, pady=2)


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
    #loading(root)
    tabs_name = []
    labels()
    listbox_author()
    listbox_poems()
    tabs(tabs_name)
    bottoms(tabs_name)
    #create_combobox(tabs_name[1])
    #main()
    root.mainloop()
