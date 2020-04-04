from tkinter import *
import tkinter.ttk as ttk
languages = ["Пуш", "До", "Лерм", "Куп", "Бл", "Толс",
                 "Бу", "Салт", "Пр", "Нек", "Ес", "Кап", "Мо",
                 "Пре", "Со", "Фе"]
root = Tk()
root.title("Анализ литературных произведений")
root.geometry("780x600+270+20")

nb = ttk.Notebook(width=490,height=430)
nb.grid(row=2,column=4,columnspan=4, rowspan=4,ipadx=3, ipady=2, sticky=N, padx=2,pady=2)

f1 = ttk.Frame(nb)
f2 = ttk.Frame(nb)
f3 = ttk.Frame(nb)
tab1 = ttk.Frame(nb) 
nb.add(f1, text='Текст')
nb.add(f2, text='Гистограмма')
nb.add(f3, text='График')

 
authors_listbox = Listbox(width=40, height=15)
vsb = Scrollbar(orient="vertical", command=authors_listbox.yview)
vsb.grid(row=2, column=2, sticky='ns')
authors_listbox.configure(yscrollcommand=vsb.set)
for language in languages:
    authors_listbox.insert(END, language)
 
authors_listbox.grid(row=2,column=0,columnspan=2, ipadx=3, ipady=2, sticky=N, padx=2,pady=2)
 
poems_listbox = Listbox(width=40,height=10)
vsb1 = Scrollbar(orient="vertical", command=poems_listbox.yview)
vsb1.grid(row=4, column=2, sticky='ns')
poems_listbox.configure(yscrollcommand=vsb1.set) 
for language in languages:
    poems_listbox.insert(END, language)
 
poems_listbox.grid(row=4,column=0,columnspan=2, ipadx=3, ipady=2, sticky=N, padx=2,pady=2)

label1 = Label(text="Авторы", fg="#eee", bg="#333")
label1.grid(row=1,column=0,columnspan=2, ipadx=3, ipady=2, sticky=W, padx=2,pady=2)
label2 = Label(text="Произведения", fg="#eee", bg="#333")
label2.grid(row=3,column=0,columnspan=2, ipadx=3, ipady=2, sticky=W, padx=2,pady=2)
label3 = Label(text="Результат исследования", fg="#eee", bg="#333")
label3.grid(row=1,column=4,columnspan=4, ipadx=3, ipady=2, sticky=W, padx=2,pady=2)
but=Button(root,text='Существ')
but1=Button(root,text='Глагол')
but2=Button(root,text='Прилагат')
but3=Button(root,text='Очистить')
but.grid(row=6,column=4, ipadx=3, ipady=2, padx=1,pady=2)
but1.grid(row=6,column=5,ipadx=10, ipady=2, padx=1,pady=2)
but2.grid(row=6,column=6, ipadx=10, ipady=2,  padx=1,pady=2)
but3.grid(row=6,column=7, ipadx=10, ipady=2, padx=1,pady=2)

root.mainloop()