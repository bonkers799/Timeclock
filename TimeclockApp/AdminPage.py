import tkinter as tk
import mysql.connector
from tkinter import ttk

class AdminWindow:
    def __init__(self, master):
        self.master = master
        self.admin_page()

    def admin_page(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        label1 = tk.Label(self.master, text="Admin Portal", font=("Cooper Black", 36), justify="center")
        label1.pack(padx=20, pady=5)

        summaryBtn = ttk.Button(self.master, text="Summary Report", command=self.summary_report)
        summaryBtn.pack(padx=20, pady=80, ipadx=20, ipady=20)

        label2 = tk.Label(self.master, text="Enter Employee then Select an Action", font=("Cooper Black", 16), justify="center")
        label2.pack(padx=20, pady=2)

        txtbox = ttk.Entry(self.master, font=("Cooper Black", 16), justify="center", width=50)
        txtbox.pack(padx=20, pady=1)

        btnframe = tk.Frame(self.master, width=150, height=150)
        btnframe.columnconfigure(0, weight=1)
        btnframe.columnconfigure(1, weight=1)
        btnframe.columnconfigure(2, weight=1)
        btnframe.columnconfigure(3, weight=1)
        btnframe.columnconfigure(4, weight=1)
        btnframe.columnconfigure(5, weight=1)
        btnframe.rowconfigure(0, weight=1)
        btnframe.rowconfigure(1, weight=1)
        btnframe.pack(padx=20, pady=5, ipadx=50, ipady=50)

        weeklybtn = ttk.Button(btnframe, text="Get Weekly Hours", command=self.weekly_hours)
        weeklybtn.grid(row=0, column=2, columnspan=2, sticky=tk.NSEW, padx=15)

        createUser = ttk.Button(btnframe, text="Create User", command=self.create_user)
        createUser.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW, padx=15, ipadx=5)

        deleteUser = ttk.Button(btnframe, text="Delete User", command=self.delete_user)
        deleteUser.grid(row=1, column=4, columnspan=2, sticky=tk.NSEW, padx=15, ipadx=5)
    
    def summary_report(self):
        print("Get Summary Report")

    def weekly_hours(self):
        print("Get Employee Weekly Hours")

    def create_user(self):
        print("Create User")
    
    def delete_user(self):
        print("Delete User")