import tkinter as tk
import mysql.connector
from tkinter import ttk
from datetime import datetime


class UserWindow:
    def __init__(self, root):
        self.root = root
        self.user_page

    #method used when the user enters a employees pin in the home screen
    def user_page(self, pin):
        #connects to the database
        self.dbConnection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Password123",
            database="timeclockdb"
        )
        self.cursor = self.dbConnection.cursor()
        
        #clears screen
        for widget in self.root.winfo_children():
            widget.destroy()
        
        #draws new screen
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
    
    #method used when the user clicks clock in
    def clock_in(self, pin):
        d = datetime.today()
        hr = datetime.now().time()
        min = datetime.now().time()
        sec = datetime.now().time()

        #gets rid of the single quotes around the pin and converts it to a string
        pinTemp = str(pin)
        pinFinal = pinTemp[1:5]

        #creates strings to be used for datetime entires in the sql query
        date = d.strftime("%Y-%m-%d")
        clockIn = date + " " + hr.strftime("%H") + ":" + min.strftime("%M") + ":" + sec.strftime("%S")
        clockOutNull = None

        #makes sure the pin has an employee associated with it
        fetchPin = "SELECT * FROM employees WHERE employee_pin=%s"
        self.cursor.execute(fetchPin, (int(pinFinal),))
        invalidPin = self.cursor.fetchone()

        if invalidPin:
            #sql query to insert pin, date, and clock in time to "time" database"
            query = "INSERT INTO time (employee_pin, date, clock_in, clock_out) VALUES (%s, %s, %s, %s);"
            self.cursor.execute(query, (int(pinFinal), date, clockIn, clockOutNull))
            self.dbConnection.commit()


    #method used when the user clicks clock out
    def clock_out(self, pin):
        d = datetime.today()
        hr = datetime.now().time()
        min = datetime.now().time()
        sec = datetime.now().time()

        #gets rid of the single quotes around the pin and converts it to a string
        pinTemp = str(pin)
        pinFinal = pinTemp[1:5]

        #creates strings to be used for datetime entires in the sql query
        date = d.strftime("%Y-%m-%d")
        clockOut = date + " " + hr.strftime("%H") + ":" + min.strftime("%M") + ":" + sec.strftime("%S")

        #makes sure the pin has an employee associated with it
        fetchPin = "SELECT * FROM employees WHERE employee_pin=%s"
        self.cursor.execute(fetchPin, (int(pinFinal),))
        invalidPin = self.cursor.fetchone()

        #ensures there is an existing pin as well as whether or not there is a record that has been started already (clocked in but not out yet)
        checkExistingRecordQuery = "SELECT * FROM time WHERE employee_pin IS NOT NULL AND date IS NOT NULL;"
        if invalidPin:
            self.cursor.execute(checkExistingRecordQuery)
            recordExists = self.cursor.fetchone()

            if recordExists:
                query = "UPDATE time SET clock_out=%s WHERE employee_pin IS NOT NULL AND date IS NOT NULL AND clock_in IS NOT NULL AND clock_out IS NULL;"
                print(query)
                self.cursor.execute(query, (clockOut,))
                self.dbConnection.commit()
            else:
                print("Record does not exist")
            
        else:
            print("Failed to clock out")