import tkinter as tk
import mysql.connector
from tkinter import ttk

class UserWindow:
    def __init__(self, master):
        self.master = master
        self.user_page()

    def user_page(self):
        self.dbConnection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Password123",
            database="timeclockdb"
        )

        for widget in self.master.winfo_children():
            widget.destroy()

        label1 = tk.Label(self.master, text="Employee Punch Clock", font=("Cooper Black", 36), justify="center")
        label1.pack(padx=20, pady=100)

        btnframe = tk.Frame(self.master, width=150, height=150)
        btnframe.columnconfigure(0, weight=1)
        btnframe.columnconfigure(1, weight=1)
        btnframe.pack(padx=20, pady=100, ipadx=150, ipady=250)

        clockIn = ttk.Button(btnframe, text="Clock In", command=self.clock_in)
        clockIn.grid(row=0, column=0, sticky=tk.NSEW, padx=50)

        clockOut = ttk.Button(btnframe, text="Clock Out", command=self.clock_out)
        clockOut.grid(row=0, column=1, sticky=tk.NSEW, padx=50)
    
    def clock_in(self):
        print("clock in")

    def clock_out(self):
        print("clock out")