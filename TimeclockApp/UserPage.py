import tkinter as tk
import mysql.connector
from tkinter import ttk
from datetime import datetime

class UserWindow:
    def __init__(self, root):
        self.root = root
        self.user_page

    def user_page(self, pin):
        self.dbConnection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Password123",
            database="timeclockdb"
        )

        self.cursor = self.dbConnection.cursor()
        

        for widget in self.root.winfo_children():
            widget.destroy()

        label1 = tk.Label(self.root, text="Employee Punch Clock", font=("Cooper Black", 36), justify="center")
        label1.pack(padx=20, pady=100)

        btnframe = tk.Frame(self.root, width=150, height=150)
        btnframe.columnconfigure(0, weight=1)
        btnframe.columnconfigure(1, weight=1)
        btnframe.pack(padx=20, pady=100, ipadx=150, ipady=250)

        clockIn = ttk.Button(btnframe, text="Clock In", command=lambda: self.clock_in(pin))
        clockIn.grid(row=0, column=0, sticky=tk.NSEW, padx=50)

        clockOut = ttk.Button(btnframe, text="Clock Out", command=lambda: self.clock_out(pin))
        clockOut.grid(row=0, column=1, sticky=tk.NSEW, padx=50)
    
    def clock_in(self, pin):
        d = datetime.today()
        hr = datetime.now().time()
        min = datetime.now().time()
        sec = datetime.now().time()

        pinTemp = str(pin)
        pinFinal = pinTemp[1:5]

        date = d.strftime("%m/%d/%y")
        clockIn = hr.strftime("%H") + ":" + min.strftime("%M") + ":" + sec.strftime("%S")
        query = "INSERT INTO time (date, clock_in) VALUES (" + date + ", " + clockIn + ") WHERE employee_pin=" + pinFinal

        print("SQL Query: " + query)
        #self.cursor.execute(query)

    def clock_out(self, pin):
        d = datetime.today()
        hr = datetime.now().time()
        min = datetime.now().time()
        sec = datetime.now().time()

        pinTemp = str(pin)
        pinFinal = pinTemp[1:5]

        date = d.strftime("%m/%d/%y")
        clockOut = hr.strftime("%H") + ":" + min.strftime("%M") + ":" + sec.strftime("%S")
        query = "INSERT INTO time (date, clock_out) VALUES (" + date + ", " + clockOut + ") WHERE employee_pin=" + pinFinal

        print("SQL Query: " + query)
        #self.cursor.execute(query)