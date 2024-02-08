import tkinter as tk
import mysql.connector
from tkinter import ttk

class AdminWindow:
    def __init__(self, root):
        self.root = root
        self.admin_page()

    def admin_page(self):
        self.dbConnection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Password123",
            database="timeclockdb"
        )
        self.cursor = self.dbConnection.cursor()

        for widget in self.root.winfo_children():
            widget.destroy()

        label1 = tk.Label(self.root, text="Admin Portal", font=("Cooper Black", 36), justify="center")
        label1.pack(padx=20, pady=5)

        summaryBtn = ttk.Button(self.root, text="Summary Report", command=self.summary_report)
        summaryBtn.pack(padx=20, pady=50, ipadx=20, ipady=20)

        label2 = tk.Label(self.root, text="Enter Employee then Select an Action", font=("Cooper Black", 16), justify="center")
        label2.pack(padx=20, pady=2)

        self.txtbox = ttk.Entry(self.root, font=("Cooper Black", 16), justify="center", width=50)
        self.txtbox.pack(padx=20, pady=1)

        btnframe = tk.Frame(self.root, width=150, height=150)
        btnframe.columnconfigure(0, weight=1)
        btnframe.columnconfigure(1, weight=1)
        btnframe.columnconfigure(2, weight=1)
        btnframe.columnconfigure(3, weight=1)
        btnframe.columnconfigure(4, weight=1)
        btnframe.columnconfigure(5, weight=1)
        btnframe.rowconfigure(0, weight=1)
        btnframe.rowconfigure(1, weight=1)
        btnframe.pack(padx=20, pady=10, ipadx=50, ipady=50)


        #fix formatting
        weeklybtn = ttk.Button(btnframe, text="Get Weekly Hours", command=self.weekly_hours)
        weeklybtn.grid(row=0, column=2, columnspan=2, sticky=tk.NSEW, padx=15)

        createUser = ttk.Button(btnframe, text="Create User", command=self.create_user)
        createUser.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW, padx=15, ipadx=5)

        deleteUser = ttk.Button(btnframe, text="Delete User", command=self.delete_user)
        deleteUser.grid(row=1, column=4, columnspan=2, sticky=tk.NSEW, padx=15, ipadx=5)
    
    def summary_report(self):
        print("Get Summary Report")

    def weekly_hours(self):
        name = self.txtbox.get()

        self.cursor = self.dbConnection.cursor()
        self.cursor.execute("SELECT employee_pin, first_name, last_name FROM employees")
        
        result = self.cursor.fetchall()

        invalidUser = 0
        for i in result:
            if name == i[1] + " " + i[2]:
                pin = i[0]
                self.show_hours(name, pin)

            if i == result[-1] and invalidUser == 1:
                self.deleteWindow = tk.Tk()
                self.deleteWindow.title("User Could Not Be Found")
                self.deleteWindow.geometry('400x200')

                label = tk.Label(self.deleteWindow, text="User Could Not Be Found", font=("Cooper Black", 18), justify="center")
                label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
                return


    #will add onto this, incomplete
    def show_hours(self, name, pin):

        for widget in self.root.winfo_children():
            widget.destroy()

        self.cursor = self.dbConnection.cursor()
        self.cursor.execute("SELECT date, clock_in, clock_out FROM time WHERE employee_pin=" + str(pin))
        
        result = self.cursor.fetchall()

        label = tk.Label(self.root, text="Weekly Report - " + name, font=("Cooper Black", 18), justify="center")
        label.pack(padx=20, pady=5)

        print(result)     


    def create_user(self):
        self.pinWindow = tk.Tk()
        self.pinWindow.title("Enter User's Pin")
        self.pinWindow.geometry('375x175')

        label = tk.Label(self.pinWindow, text="Enter User's Pin", font=("Cooper Black", 18), justify="center")
        label.pack(padx=20, pady=5)

        self.pinEntry = ttk.Entry(self.pinWindow, width=6)
        self.pinEntry.pack(pady=5)

        self.chkboxValue = tk.BooleanVar(value=False)
        self.chkbox = ttk.Checkbutton(self.pinWindow, text="Admin?", variable=self.chkboxValue)
        self.chkbox.pack(pady=1)

        self.createBtn = ttk.Button(self.pinWindow, text="Submit Pin", command=self.create_user_window)
        self.createBtn.pack(pady=5)

    def create_user_window(self):
        name = self.txtbox.get()
        if self.chkboxValue == 1:
            admin = 1
        else:
            admin = 0
        nameArr = name.split(" ")
        print(nameArr)
        firstName = nameArr[0]
        lastName = nameArr[1]
        pin = self.pinEntry.get()
        query = "INSERT INTO employees (employee_pin, admin, first_name, last_name) VALUES (" + pin + ", " + str(admin) + ", " + firstName + ", " + lastName + ")"
        print(query)

        for widget in self.pinWindow.winfo_children():
            widget.destroy()
        
        label = tk.Label(self.pinWindow, text="User Created", font=("Cooper Black", 18), justify="center")
        label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.txtbox.delete(0, "end")

    def delete_user(self):
        name = self.txtbox.get()

        self.cursor = self.dbConnection.cursor()
        self.cursor.execute("SELECT employee_pin, first_name, last_name FROM employees")
        
        result = self.cursor.fetchall()

        for i in result:
            if name == (i[1] + " " + i[2]):                
                print("SQL Query: DELETE FROM employees WHERE employee_pin=" + str(i[0]) + " AND first_name=" + i[1] + " AND last_name=" + i[2])

                #employee_pin is the foreign key of the employees table
                print("SQL QUERY: DELETE FROM time WHERE employee_pin=" + str(i[0]))
                return

            if i == result[-1]:                
                self.deleteWindow = tk.Tk()
                self.deleteWindow.title("user Could Not Be Found")
                self.deleteWindow.geometry('400x200')

                label = tk.Label(self.deleteWindow, text="User Could Not Be Found", font=("Cooper Black", 18), justify="center")
                label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
                self.txtbox.delete(0, "end")     
        return