import tkinter as tk
import mysql.connector
from tkinter import ttk
from datetime import datetime, timedelta, time

class AdminWindow:
    def __init__(self, root):
        self.root = root
        self.startDate = None
        self.endDate = None
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

        self.sty = ttk.Style()
        self.sty.configure("AdminPage.TButton", font=("Cooper Black", 15), padding=(5,10))
        
        weeklybtn = ttk.Button(btnframe, text="Get Weekly Hours", style="AdminPage.TButton", command=self.weekly_hours)
        weeklybtn.grid(row=0, column=2, columnspan=2, sticky=tk.NSEW, padx=15)

        createUser = ttk.Button(btnframe, text="Create User", style="AdminPage.TButton", command=self.create_user)
        createUser.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW, padx=15, ipadx=5)

        deleteUser = ttk.Button(btnframe, text="Delete User", style="AdminPage.TButton", command=self.delete_user)
        deleteUser.grid(row=1, column=4, columnspan=2, sticky=tk.NSEW, padx=15, ipadx=5)
    
    def summary_report(self):
        #clears screen
        for widget in self.root.winfo_children():
            widget.destroy()

        self.cursor = self.dbConnection.cursor()
        self.cursor.execute("SELECT * FROM time")
        result = self.cursor.fetchall()

        today = datetime.now().date()

        #fills dateArr with dates that will be displayed from the most recent sunday with data to the following saturday
        if self.startDate is None:
            i = 0
            dateArr = []
            for r in result:
                if r[1].weekday()==6 and (today - r[1]) < timedelta(days=8):
                    sunday = today - r[1]
                    while i < 7:
                        dateArr.append(sunday - timedelta(days=i))
                        i += 1
                    break
            self.startDate = (today - dateArr[0])
            self.endDate = (today - dateArr[6])
        
        #calculates hours worked if the record's date is within the start and end date
        totalHrs = {}
        for record in result:
            employee_pin, date, clockIn, clockOut = record
            
            if self.startDate <= date <= self.endDate:
                if clockIn and clockOut:
            
                    totalHrsWorked = clockOut - clockIn
                    totalHrs.setdefault(employee_pin, 0)
                    totalHrs[employee_pin] += totalHrsWorked.total_seconds() / 3600

        #query to get all the names of the employees
        self.cursor.execute("SELECT employee_pin, first_name, last_name FROM employees WHERE first_name IS NOT NULL AND last_name IS NOT NULL AND admin=0")
        result = self.cursor.fetchall()

        #fills a dictionary with every employees name and hours worked
        nameDict = {}
        i = 0
        for key, value in totalHrs.items():
            for name in result:
                if key == name[0]:
                    
                    nameDict[(name[1] + " " + name[2])] = value

        #starts drawing screen
        title = tk.Label(self.root, text="Weekly Summary", font=("Cooper Black", 24), justify="center")
        title.pack(padx=20, pady=5)

        #frame and buttons for navigation
        weekSelectFrame = tk.Frame(self.root, width=200, height=100)
        weekSelectFrame.rowconfigure(0, weight=1)
        weekSelectFrame.columnconfigure(0, weight=1)
        weekSelectFrame.columnconfigure(1, weight=1)
        weekSelectFrame.columnconfigure(2, weight=1)
        weekSelectFrame.pack(padx=20, pady=20)
        
        prevSummary = ttk.Button(weekSelectFrame, text="Previous Summary", style="AdminPage.TButton", command=lambda: self.prev_sum(self.startDate, self.endDate))
        prevSummary.grid(row=0, column=0, sticky=tk.NSEW)

        backBtn = ttk.Button(weekSelectFrame, text="Back to Admin", style="AdminPage.TButton", command=self.admin_page)
        backBtn.grid(row=0, column=1, sticky=tk.NSEW)

        nextSummary = ttk.Button(weekSelectFrame, text="Next Summary", style="AdminPage.TButton", command=lambda: self.next_sum(self.startDate, self.endDate))
        nextSummary.grid(row=0, column=2, sticky=tk.NSEW)

        weekHeader = tk.Label(self.root, text="Week of: {} - {}".format(self.startDate, self.endDate), font=("Cooper Black", 16), justify="center", padx=10)
        weekHeader.pack(padx=20, pady=3)


        #creates a scrollbar, doesnt work well
        scrollbar = ttk.Scrollbar(self.root, orient="vertical")
        scrollbar.pack(side=tk.RIGHT, fill="y", expand=False)
        self.scrollCanvas = tk.Canvas(self.root, width=500, height=300,  yscrollcommand=scrollbar.set)
        self.scrollCanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.scrollCanvas.yview)
        
        
        self.dataFrame = ttk.Frame(self.scrollCanvas)
        #self.dataFrame.bind('<Configure>', self.configure_dataFrame)
        #self.dataFrame.bind('<Configure>', self.configure_scrollCanvas)
        self.dataFrameId = self.scrollCanvas.create_window((155,0), window=self.dataFrame, anchor="nw")


        self.dataFrame.columnconfigure(0, weight=1)
        self.dataFrame.columnconfigure(1, weight=1)
        self.dataFrame.columnconfigure(2, weight=1)
        self.dataFrame.rowconfigure(0, weight=1)
        self.dataFrame.rowconfigure(1, weight=1)

        empHeader = tk.Label(self.dataFrame, text="Weekday", font=("Cooper Black", 16), justify="center", padx=10)
        empHeader.grid(row=0, column=0, sticky=tk.NSEW)

        hrHeader = tk.Label(self.dataFrame, text="Hours Worked", font=("Cooper Black", 16), justify="center", padx=10)
        hrHeader.grid(row=0, column=2, sticky=tk.EW)

        empLine = tk.Frame(self.dataFrame, width=5, bg="black", height=5)
        empLine.grid(row=1, column=0, columnspan=4, sticky=tk.EW)
        
        #loops through all the items in the dictionary and draws its contents on the screen
        i = 2
        for name, value in nameDict.items():
            if value.is_integer():
                value = int(value)
            else:
                value = round(value, 2)

            self.dataFrame.rowconfigure(i, weight=1)

            employeeLabel = tk.Label(self.dataFrame, text=name, font=("Cooper Black", 16), justify="center", padx=10)
            employeeLabel.grid(row=i, column=0, sticky=tk.NSEW)

            lineRight = tk.Frame(self.dataFrame, width=3, bg="black")
            lineRight.grid(row=i, column=1, sticky=tk.NSEW)

            valueLabel = tk.Label(self.dataFrame, text=str(value) + " Hours", font=("Cooper Black", 16), justify="right", padx=10)
            valueLabel.grid(row=i, column=2, sticky=tk.E)

            i += 1


    #allows for changing of the date range
    def next_sum(self, start, end):
        self.startDate = start + timedelta(days=7)
        self.endDate = end + timedelta(days=7)
        self.summary_report()

    #allows for changing of the date range
    def prev_sum(self, start, end):
        self.startDate = start - timedelta(days=7)
        self.endDate = end - timedelta(days=7)
        self.summary_report()
    
    #used for scrolling
    def configure_dataFrame(self):
        size = (self.dataFrame.winfo_reqwidth(), self.dataFrame.winfo_reqheight())
        self.scrollCanvas.config(scrollregion=(0, 0, size[0], size[1]))
        if self.dataFrame.winfo_reqwidth() != self.scrollCanvas.winfo_width():
            self.scrollCanvas.config(width=self.dataFrame.winfo_reqwidth())

    def configure_scrollCanvas(self):
        self.scrollCanvas.config(scrollregion=self.scrollCanvas.bbox("all"))

    #method used when the user clicks get weekly hours
    def weekly_hours(self):
        week = 0
        name = self.txtbox.get()

        #sql query to get first and last name as well as the pin from the textbox
        self.cursor = self.dbConnection.cursor()
        self.cursor.execute("SELECT employee_pin, first_name, last_name FROM employees")
        result = self.cursor.fetchall()

        #checks to see if the user exists in the database
        invalidUser = 0
        for i in result:
            #if true call show_hours()
            if name == i[1] + " " + i[2]:
                pin = i[0]
                self.show_hours(name, pin, week)

            #otherwisee display a window showing invalid name
            if i == result[-1] and invalidUser == 1:
                self.deleteWindow = tk.Tk()
                self.deleteWindow.title("User Could Not Be Found")
                self.deleteWindow.geometry('400x200')

                label = tk.Label(self.deleteWindow, text="User Could Not Be Found", font=("Cooper Black", 18), justify="center")
                label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
                return


    def show_hours(self, name, pin, week):
        #clears screen
        for widget in self.root.winfo_children():
            widget.destroy()

        #sql query to get selected employees hour
        self.cursor = self.dbConnection.cursor()
        selectEmployee = "SELECT * FROM time WHERE employee_pin=%s"
        self.cursor.execute(selectEmployee, (str(pin),))
        result = self.cursor.fetchall()

        #gets the most record with the most recent date and the days of the week associated with it
        today = datetime.now().date()
        weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        diff = 100

        #gives most recent punch out of the results
        for r in result:
            dateTest = r[1] - today
            testDifference = abs(dateTest.days)
            if testDifference < diff:
                mostRecent = r[1]
                diff = testDifference

        #fills date list to fill in screen
        i = 0
        j = 0
        while True:
            dateTest = (mostRecent - timedelta(days=i)).weekday()
            if weekdays[dateTest] == "Sunday":
                dateArr = []

                sunday = mostRecent - timedelta(days=i)

                #these two ifs come into play after either the next or previous week buttons have been pressed
                #if week is negative then advance to the next week
                if week > 0:
                    #makes previous week button load instead
                    sunday = sunday - timedelta(days=(week * 7))
                    while j < 7:
                        dateArr.append(sunday + timedelta(days=j))
                        j += 1
                    break
                    
                #if week is negative then advance to the next week
                if week < 0:
                    sunday = sunday - timedelta(days=(week * 7))
                    while j < 7:
                        dateArr.append(sunday + timedelta(days=j))
                        j += 1
                    break
                
                while j < 7:
                    dateArr.append(sunday + timedelta(days=j))
                    j += 1

                break
            i += 1


        #fills clock_in list to fill in screen by searching for a record with a date that matches date array, formats it, then appends to clock in list
        inArr = []
        for x in dateArr:
            flag = False

            for record in result:
                dateCombine = datetime.combine(x, time(hour=record[2].hour, minute=record[2].minute, second=record[2].second))

                if dateCombine == record[2]:
                    formattedTime = "{}:{:02d}:{:02d}".format(record[2].hour, record[2].minute, record[2].second)
                    inArr.append(formattedTime)
                    flag = True
                    break

            #if a datetime doesnt match with a record, N/A
            if not flag:
                inArr.append("N/A")
                
        #fills clock_out list to fill in screen by searching for a record with a date that matches date array, formats it, then appends to clock out list
        outArr = []
        for x in dateArr:
            flag = False
            for record in result:
                dateCombine = datetime.combine(x, time(hour=record[3].hour, minute=record[3].minute, second=record[3].second))

                if dateCombine == record[3]:
                    formattedTime = "{}:{:02d}:{:02d}".format(record[3].hour, record[3].minute, record[3].second)
                    outArr.append(formattedTime)
                    flag = True
                    break

            #if a datetime doesnt match with a record, N/A
            if not flag:
                outArr.append("N/A")
        
        #calculates total hours worked
        i = 0
        totalArr = []
        totalHrs = 0
        while i < len(inArr) and i < len(outArr):
            if inArr[i] == "N/A" or outArr[i] == "N/A":
                totalArr.append("N/A")
                i += 1
                continue
            
            clockIn = inArr[i] 
            clockOut = outArr[i]

            hoursWorked = datetime.strptime(clockOut, "%H:%M:%S") - datetime.strptime(clockIn, "%H:%M:%S")
            
            hr = hoursWorked.seconds // 3600
            min = (hoursWorked.seconds // 60) % 60
            sec = hoursWorked.seconds % 60

            intHrs = hr + (min/60) + (sec/3600)
            calculatedHours = "{}:{:02d}:{:02d}".format(hr, min, sec)

            totalArr.append(calculatedHours)

            #variable used for totals row
            totalHrs = float(totalHrs) + intHrs
            totalHrs = "{:.2f}".format(totalHrs)
            i += 1

        #formats date list
        i = 0
        for date in dateArr:
            formattedDate = "{}/{}/{}".format(date.month, date.day, date.year)
            dateArr[i] = formattedDate
            i += 1

        #draws screen
        title = tk.Label(self.root, text="Weekly Report - " + name, font=("Cooper Black", 24), justify="center")
        title.pack(padx=20, pady=5)

        weekSelectFrame = tk.Frame(self.root, width=200, height=100)
        weekSelectFrame.rowconfigure(0, weight=1)
        weekSelectFrame.columnconfigure(0, weight=1)
        weekSelectFrame.columnconfigure(1, weight=1)
        weekSelectFrame.columnconfigure(2, weight=1)
        weekSelectFrame.pack(padx=20, pady=20)
        
        prevBtn = ttk.Button(weekSelectFrame, text="Previous Week", command=lambda: self.prev_week(name, pin, week))
        prevBtn.grid(row=0, column=0, sticky=tk.NSEW)

        backBtn = ttk.Button(weekSelectFrame, text="Back to Admin", command=self.admin_page)
        backBtn.grid(row=0, column=1, sticky=tk.NSEW)

        nextBtn = ttk.Button(weekSelectFrame, text="Next Week", command=lambda: self.next_week(name, pin, week))
        nextBtn.grid(row=0, column=2, sticky=tk.NSEW)
    
        #creates the frame the data goes in
        hourFrame = tk.Frame(self.root, width=200, height=500)
        hourFrame.columnconfigure(0, weight=1)
        hourFrame.columnconfigure(1, weight=1)
        hourFrame.columnconfigure(2, weight=1)
        hourFrame.columnconfigure(3, weight=1)
        hourFrame.columnconfigure(4, weight=1)
        hourFrame.columnconfigure(5, weight=1)
        hourFrame.columnconfigure(6, weight=1)
        hourFrame.columnconfigure(7, weight=1)
        hourFrame.rowconfigure(0, weight=1)
        hourFrame.rowconfigure(1, weight=1)
        hourFrame.rowconfigure(2, weight=1)
        hourFrame.rowconfigure(3, weight=1)
        hourFrame.rowconfigure(4, weight=1)
        hourFrame.rowconfigure(5, weight=1)
        hourFrame.rowconfigure(6, weight=1)
        hourFrame.rowconfigure(7, weight=1)
        hourFrame.rowconfigure(8, weight=1)
        hourFrame.rowconfigure(9, weight=1)
        hourFrame.pack(padx=20, pady=30)

        #draws column headers
        dayHeader = tk.Label(hourFrame, text="Weekday", font=("Cooper Black", 16), justify="center", padx=10)
        dayHeader.grid(row=0, column=0, sticky=tk.NSEW)

        line1 = tk.Frame(hourFrame, width=5, bg="black")
        line1.grid(row=0, column=1, sticky=tk.NS)

        dateHeader = tk.Label(hourFrame, text="Date", font=("Cooper Black", 16), justify="center", padx=10)
        dateHeader.grid(row=0, column=2, sticky=tk.NSEW)

        line2 = tk.Frame(hourFrame, width=5, bg="black")
        line2.grid(row=0, column=3, sticky=tk.NS)
        
        inHeader = tk.Label(hourFrame, text="Clock In", font=("Cooper Black", 16), justify="center", padx=10)
        inHeader.grid(row=0, column=4, sticky=tk.NSEW)

        line3 = tk.Frame(hourFrame, width=5, bg="black")
        line3.grid(row=0, column=5, sticky=tk.NS)

        outHeader = tk.Label(hourFrame, text="Clock Out", font=("Cooper Black", 16), justify="center", padx=10)
        outHeader.grid(row=0, column=6, sticky=tk.NSEW)

        line4 = tk.Frame(hourFrame, width=5, bg="black")
        line4.grid(row=0, column=7, sticky=tk.NS)

        totalHeader = tk.Label(hourFrame, text="Total", font=("Cooper Black", 16), justify="center", padx=10)
        totalHeader.grid(row=0, column=8, sticky=tk.NSEW)

        #draws line between headers and data
        k = 0
        while k < 9:
            separatorLine = tk.Frame(hourFrame, height=5, bg="black")
            separatorLine.grid(row=1, column=k, sticky=tk.EW)
            k += 1
        

        #draws sunday row
        dayLabel = tk.Label(hourFrame, text="Sunday", font=("Cooper Black", 14), justify="center", padx=10, pady=6)
        dayLabel.grid(row=2, column=0, sticky=tk.NSEW)

        line5 = tk.Frame(hourFrame, width=5, bg="black")
        line5.grid(row=2, column=1, sticky=tk.NS)

        dateLabel = tk.Label(hourFrame, text=dateArr[0], font=("Cooper Black", 14), justify="center", padx=10, pady=6)
        dateLabel.grid(row=2, column=2, sticky=tk.NSEW)

        line6 = tk.Frame(hourFrame, width=5, bg="black")
        line6.grid(row=2, column=3, sticky=tk.NS)
        

        inLabel = tk.Label(hourFrame, text=inArr[0], font=("Cooper Black", 14), justify="center", padx=10, pady=6)
        inLabel.grid(row=2, column=4, sticky=tk.NSEW)

        line7 = tk.Frame(hourFrame, width=5, bg="black")
        line7.grid(row=2, column=5, sticky=tk.NS)

        outLabel = tk.Label(hourFrame, text=outArr[0], font=("Cooper Black", 14), justify="center", padx=10, pady=6)
        outLabel.grid(row=2, column=6, sticky=tk.NSEW)

        line8 = tk.Frame(hourFrame, width=5, bg="black")
        line8.grid(row=2, column=7, sticky=tk.NS)

        totalLabel = tk.Label(hourFrame, text=totalArr[0], font=("Cooper Black", 14), justify="center", padx=10, pady=6)
        totalLabel.grid(row=2, column=8, sticky=tk.NSEW)

        #sets the data in the various columns
        i = 3
        for day in weekdays:
            if day == "Sunday":
                break

            dayLabel = tk.Label(hourFrame, text=day, font=("Cooper Black", 14), justify="center", padx=10, pady=6)
            dayLabel.grid(row=i, column=0, sticky=tk.NSEW)

            line1 = tk.Frame(hourFrame, width=5, bg="black")
            line1.grid(row=i, column=1, sticky=tk.NS)

            dateLabel = tk.Label(hourFrame, text=dateArr[i-2], font=("Cooper Black", 14), justify="center", padx=10, pady=6)
            dateLabel.grid(row=i, column=2, sticky=tk.NSEW)

            line2 = tk.Frame(hourFrame, width=5, bg="black")
            line2.grid(row=i, column=3, sticky=tk.NS)

            inLabel = tk.Label(hourFrame, text=inArr[i-2], font=("Cooper Black", 14), justify="center", padx=10, pady=6)
            inLabel.grid(row=i, column=4, sticky=tk.NSEW)

            line3 = tk.Frame(hourFrame, width=5, bg="black")
            line3.grid(row=i, column=5, sticky=tk.NS)

            outLabel = tk.Label(hourFrame, text=outArr[i-2], font=("Cooper Black", 14), justify="center", padx=10, pady=6)
            outLabel.grid(row=i, column=6, sticky=tk.NSEW)

            line4 = tk.Frame(hourFrame, width=5, bg="black")
            line4.grid(row=i, column=7, sticky=tk.NS)

            totalLabel = tk.Label(hourFrame, text=totalArr[i-2], font=("Cooper Black", 14), justify="center", padx=10, pady=6)
            totalLabel.grid(row=i, column=8, sticky=tk.NSEW)

            i += 1

        #draws total row
        hoursLabel = tk.Label(hourFrame, text="Total Hours: " + str(totalHrs), font=("Cooper Black", 24), justify="center", padx=10, pady=30)
        hoursLabel.grid(row=9, column=0, columnspan=9, sticky=tk.NSEW)
        
    #sets week variable so date array knows what dates to use
    def prev_week(self, name, pin, week):
        name = name
        pin = pin
        week += 1
        self.show_hours(name, pin, week)

    #sets week variable so date array knows what dates to use
    def next_week(self, name, pin, week):
        name = name
        pin = pin
        week -= 1
        self.show_hours(name, pin, week)


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