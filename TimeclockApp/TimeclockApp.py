import tkinter as tk
import mysql.connector
from tkinter import ttk
from UserPage import UserWindow
from AdminPage import AdminWindow

class TimeclockApp():
    def __init__(self):
        self.dbConnection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Password123",
            database="timeclockdb"
        )

        self.root = tk.Tk()

        self.root.geometry('700x600')
        self.root.title('Time Clock')
        
        
        label1 = tk.Label(self.root, text="Time Clock", font=("Cooper Black", 48), justify="center")
        label1.pack(padx=20, pady=100)

        self.txtbox1 = ttk.Entry(self.root, font=("Cooper Black", 16), justify="center", width=6)
        self.txtbox1.pack(padx=20, pady=20)

        btnframe = tk.Frame(self.root, width=500, height=550)
        btnframe.columnconfigure(0, weight=1)
        btnframe.columnconfigure(1, weight=1)
        btnframe.columnconfigure(2, weight=1)
        btnframe.rowconfigure(0, weight=1)
        btnframe.rowconfigure(1, weight=1)
        btnframe.rowconfigure(2, weight=1)
        btnframe.rowconfigure(3, weight=1)
        btnframe.pack(padx=20, pady=50, ipadx=150, ipady=250)
        
        #for later styling possibilities
        
        sty = ttk.Style()
        sty.configure("TButton", font=("Cooper Black", 15), padding=(0,-2))


        btn1 = ttk.Button(btnframe, text="1", command=lambda: self.add_input(btn1))
        btn1.grid(row=0, column=0, sticky=tk.NSEW)

        btn2 = ttk.Button(btnframe, text="2", command=lambda: self.add_input(btn2))
        btn2.grid(row=0, column=1, sticky=tk.NSEW)

        btn3 = ttk.Button(btnframe, text="3", command=lambda: self.add_input(btn3))
        btn3.grid(row=0, column=2, sticky=tk.NSEW)

        btn4 = ttk.Button(btnframe, text="4", command=lambda: self.add_input(btn4))
        btn4.grid(row=1, column=0, sticky=tk.NSEW)

        btn5 = ttk.Button(btnframe, text="5", command=lambda: self.add_input(btn5))
        btn5.grid(row=1, column=1, sticky=tk.NSEW)

        btn6 = ttk.Button(btnframe, text="6", command=lambda: self.add_input(btn6))
        btn6.grid(row=1, column=2, sticky=tk.NSEW)

        btn7 = ttk.Button(btnframe, text="7", command=lambda: self.add_input(btn7))
        btn7.grid(row=2, column=0, sticky=tk.NSEW)
        
        btn8 = ttk.Button(btnframe, text="8", command=lambda: self.add_input(btn8))
        btn8.grid(row=2, column=1, sticky=tk.NSEW)

        btn9 = ttk.Button(btnframe, text="9", command=lambda: self.add_input(btn9))
        btn9.grid(row=2, column=2, sticky=tk.NSEW)

        btn0 = ttk.Button(btnframe, text="0", command=lambda: self.add_input(btn0))
        btn0.grid(row=3, column=0, columnspan=2, sticky=tk.NSEW)

        backBtn = ttk.Button(btnframe, text="\u2190", command=self.backspace_int)
        backBtn.grid(row=3, column=2, sticky=tk.NSEW)

        enterBtn = ttk.Button(btnframe, text="Submit", command=self.submit_btn)
        enterBtn.grid(row=4, column=0, columnspan=3, sticky=tk.NSEW)

        self.root.mainloop()
        return

    def add_input(self, btn):
        oldText = self.txtbox1.get()
        passedText = btn.cget("text")
        newText = oldText + passedText

        if len(newText) > 4:
            return

        self.txtbox1.delete(0,tk.END)
        self.txtbox1.insert(0,newText)
    
    def backspace_int(self):
        oldText = self.txtbox1.get()
        newText = oldText[:-1]

        self.txtbox1.delete(0, tk.END)
        self.txtbox1.insert(0, newText)
        
    def submit_btn(self):
        pin = self.txtbox1.get()

        self.cursor = self.dbConnection.cursor()
        self.cursor.execute("SELECT employee_pin FROM employees")
        result = self.cursor.fetchall()

        if len(pin) == 4:
            i = 0


            for x in result:
                if int(pin) == x[-1]:
                    self.cursor.execute("SELECT admin FROM employees WHERE employee_pin = " + str(x[-1]))
                    pinResult = self.cursor.fetchall()

                    for y in pinResult:
                        if y[-1] == 1:
                            adminClass = AdminWindow(self.root)
                            adminClass.admin_page()
                        elif y[-1] == 0:
                            userClass = UserWindow(self.root)
                            userClass.user_page()
                        else:
                            print("invalid")
                            return
            #if newText == admin's pin
                #go to admin's page
            return
start = TimeclockApp()