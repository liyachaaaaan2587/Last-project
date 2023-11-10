import tkinter as tk
import sqlite3
from tkinter import ttk

class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()
        
    def init_main(self):
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        
        self.add_image = tk.PhotoImage(file='./img/add.png')
        btn_open_dialog = tk.Button(toolbar, image=self.add_image,
                                    bg='#d7d8e0', bd=0, command=self.open_dialog)
        btn_open_dialog.pack(side=tk.LEFT)
        
        self.update_image = tk.PhotoImage(file='./img/update.png')
        btn_update = tk.Button(toolbar, image=self.update_image,
                                    bg='#d7d8e0', bd=0, command=self.update_dialog)
        btn_update.pack(side=tk.LEFT)

        self.delete_image = tk.PhotoImage(file='./img/delete.png')
        btn_delete = tk.Button(toolbar, image=self.delete_image,
                                    bg='#d7d8e0', bd=0, command=self.delete_records)
        btn_delete.pack(side=tk.LEFT)
        
        self.search_image = tk.PhotoImage(file='./img/search.png')
        btn_search = tk.Button(toolbar, image=self.search_image,
                               bg='#d7d8e0', bd=0, command=self.search_dialog)
        btn_search.pack(side=tk.LEFT)
        
        self.refresh_image = tk.PhotoImage(file='./img/refresh.png')
        btn_refresh = tk.Button(toolbar, image=self.refresh_image,
                                    bg='#d7d8e0', bd=0, command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

        
        self.tree = ttk.Treeview(self, columns=['ID', 'name', 'tel', 'email', 'salary'],
                                 height=45, show='headings')
        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('name', width=200, anchor=tk.CENTER)
        self.tree.column('tel', width=150, anchor=tk.CENTER)
        self.tree.column('email', width=100, anchor=tk.CENTER)
        self.tree.column('salary', width=70, anchor=tk.CENTER)
        
        self.tree.heading('ID', text='ID')
        self.tree.heading('name', text='ФИО')
        self.tree.heading('tel', text='Номер телефона')
        self.tree.heading('email', text='E-mail')
        self.tree.heading('salary', text='Зарплата')

        self.tree.pack(side=tk.LEFT)
        
    def open_dialog(self):
        Child()
        
    def update_dialog(self):
        Update()
    
    def search_dialog(self):
        Search()
        
    def records(self, name, tel, email, salary):
        self.db.insert_data(name, tel, email, salary)
        self.view_records()
        
    def view_records(self):
        self.db.c.execute("""SELECT * FROM db""")
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]
        
    def update_record(self, name, tel, email, salary):
        self.db.c.execute("""
        UPDATE db SET name=?, tel=?, email=?, salary=? WHERE ID=?""",
        (name, tel, email, salary, 
        self.tree.set(self.tree.selection()[0], '#1')))
        self.view_records()
        
    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.c.execute("DELETE FROM db WHERE id=?",
                              (self.tree.set(selection_item, '#1')))
        self.db.conn.commit()
        self.view_records()
        
    def search_records(self, name):
        name = ('%' + name + '%')
        self.db.c.execute("""
        SELECT * FROM db WHERE name LIKE ? """, (name,))
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]


class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app
        
    def init_child(self):
        self.title('Добавить')
        self.geometry('400x220')
        self.resizable(False, False)
        
        self.grab_set()
        self.focus_set()
        
        label_name = tk.Label(self, text='ФИО')
        label_name.place(x=50, y=50)
        label_tel = tk.Label(self, text='Телефон')
        label_tel.place(x=50, y=80)
        label_email = tk.Label(self, text='E-mail')
        label_email.place(x=50, y=110)
        label_salary = tk.Label(self, text='Зарплата')
        label_salary.place(x=50, y=140)
        
        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=180, y=50)
        self.entry_tel = tk.Entry(self)
        self.entry_tel.place(x=180, y=80)
        self.entry_email = tk.Entry(self)
        self.entry_email.place(x=180, y=110)
        self.entry_salary = tk.Entry(self)
        self.entry_salary.place(x=180, y=140)
        
        self.btn_cancel = tk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=250, y=180)
        
        self.btn_ok = tk.Button(self, text='Добавить')
        self.btn_ok.place(x=170, y=180)
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_name.get(),
                                                                       self.entry_tel.get(),
                                                                       self.entry_email.get(),
                                                                       self.entry_salary.get()))


class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.deffault_data()
        
    def init_edit(self):
        self.title('Редактировать')
        btn_edit = tk.Button(self, text='Редактировать')
        btn_edit.place(x=140, y=180)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_record(self.entry_name.get(),
                                                                          self.entry_email.get(),
                                                                          self.entry_email.get(),
                                                                          self.entry_salary.get()))
        btn_edit.bind('<Button-1>', lambda event: self.destroy, add='+')
        self.btn_ok.destroy()
        
    def deffault_data(self):
        self.db.c.execute("""
        SELECT * FROM db WHERE ID=?""",
        (self.view.tree.set(self.view.tree.selection()[0], '#1'),))
        row = self.db.c.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_tel.insert(0, row[2])
        self.entry_email.insert(0, row[3])
        self.entry_salary.insert(0, row[4])


class Search(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Поиск')
        self.geometry('300x100')
        self.resizable(False, False)
        
        label_search = tk.Label(self, text='Поиск')
        label_search.place(x=50, y=20)
        
        self.search_entry = ttk.Entry(self)
        self.search_entry.place(x=105, y=20, width=150)
        
        self.btn_cancel = tk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=185, y=50)
        
        btn_search = ttk.Button(self, text='Поиск')
        btn_search.place(x=100, y=50)
        btn_search.bind('<Button-1>', lambda event: 
            self.view.search_records(self.search_entry.get()))
        btn_search.bind('<Button-1>', lambda event:
            self.destroy, add='+')

        

class DB:
    def __init__(self):
        self.conn = sqlite3.connect('db.db')
        self.c = self.conn.cursor()
        self.c.execute("""
        CREATE TABLE IF NOT EXISTS db(
            id INTEGER PRIMARY KEY,
            name TEXT,
            tel TEXT,
            email TEXT,
            salary TEXT)""")
        self.conn.commit()

    def insert_data(self, name, tel, email, salary):
        self.c.execute("""
        INSERT INTO db(name, tel, email, salary) VALUES (?, ?, ?, ?)""",
                                            (name, tel, email, salary,))
        self.conn.commit()


if __name__ == '__main__':
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title('Список сотрудников компании')
    root.geometry('700x500')
    root.resizable(False, False)
    root.mainloop()
