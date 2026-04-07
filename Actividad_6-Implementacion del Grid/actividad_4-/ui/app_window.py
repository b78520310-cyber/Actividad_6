import tkinter as tk
from tkinter import ttk
from service.task_service import TaskService

class AppWindow(tk.Tk):

    def __init__(self, task_service: TaskService) -> None:
        super().__init__()

        self._task_service = task_service

        self.title("Formulario de Registro")
        self.geometry("500x500")
        self.resizable(False, False)

        self.users = [
            {"fname": "Juan", "lname": "Santana", "age": "18"},
            {"fname": "Carlos", "lname": "Rodríguez", "age": "37"},
            {"fname": "María", "lname": "Rosario", "age": "28"},
        ]

        self.create_widgets()
        self.show_table()

    def create_widgets(self):

        tk.Label(self, text="Nombre").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.fname = tk.Entry(self)
        self.fname.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self, text="Apellido").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.lname = tk.Entry(self)
        self.lname.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self, text="Edad").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.age = tk.Entry(self)
        self.age.grid(row=2, column=1, padx=10, pady=5)

        tk.Button(self, text="Guardar", width=15, command=self.get_user)\
            .grid(row=3, column=0, pady=10)

        tk.Button(self, text="Actualizar", width=15, command=self.update_user)\
            .grid(row=3, column=1, pady=10)

        tk.Button(self, text="Eliminar", width=15, command=self.delete_user)\
            .grid(row=4, column=0, columnspan=2, pady=10)

        self.tree = ttk.Treeview(self, columns=("lname", "age"))

        self.tree.column("#0", width=150)
        self.tree.column("lname", width=150, anchor="center")
        self.tree.column("age", width=100, anchor="center")

        self.tree.heading("#0", text="Nombre")
        self.tree.heading("lname", text="Apellido")
        self.tree.heading("age", text="Edad")

        self.tree.grid(row=5, column=0, columnspan=2, padx=20, pady=20)

        self.tree.bind("<<TreeviewSelect>>", self.select_user)

    def get_user(self):
        fname = self.fname.get()
        lname = self.lname.get()
        age = self.age.get()

        self.users.append({"fname": fname, "lname": lname, "age": age})

        self.show_table()
        self.clear_inputs()

    def select_user(self, event):
        selected = self.tree.focus()

        if selected:
            values = self.tree.item(selected)

            fname = values["text"]
            lname, age = values["values"]

            self.clear_inputs()

            self.fname.insert(0, fname)
            self.lname.insert(0, lname)
            self.age.insert(0, age)

    def update_user(self):
        selected = self.tree.focus()

        if selected:
            index = self.tree.index(selected)

            fname = self.fname.get()
            lname = self.lname.get()
            age = self.age.get()

            self.users[index] = {"fname": fname, "lname": lname, "age": age}

            self.show_table()
            self.clear_inputs()

    def delete_user(self):
        selected = self.tree.focus()

        if selected:
            index = self.tree.index(selected)

            del self.users[index]

            self.show_table()
            self.clear_inputs()

    def show_table(self):
        self.clear_table()

        for user in self.users:
            self.tree.insert("", "end", text=user["fname"], values=(user["lname"], user["age"]))

    def clear_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def clear_inputs(self):
        self.fname.delete(0, "end")
        self.lname.delete(0, "end")
        self.age.delete(0, "end")