import tkinter
from tkinter import *
from PIL import Image, ImageTk
import cv2
import numpy as np
import face_recognition as fc
import os
from datetime import datetime,date
import mysql.connector as sql

mydb = sql.connect(
    host="localhost",
    user="root",
    password="dk19",
    database="face_recognition"
)


path = 'Images'
images = []
classNames = []
myList = os.listdir(path)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

def findEncodings(images):
    encodeList = []
    for img in images:
        if img is None:  # Check if image is loaded properly
            print("Error: Image not loaded correctly.")
            continue

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodings = fc.face_encodings(img)

        if encodings:  # Ensure encodings list is not empty
            encodeList.append(encodings[0])
        else:
            print("Warning: No face detected in an image. Skipping...")

    return encodeList

def markAttendance(name):

    cursor=mydb.cursor()
    cursor.execute("SELECT * FROM ATTENDANCE")
    namelist=[]
    datelist=[]
    myDataList=cursor.fetchall()
    dat=date.today()
    for i in myDataList:
        entry=i[0]
        datry=i[2]
        namelist.append(entry)
        datelist.append(datry)
    try:
        t=namelist.index(name)
    except ValueError:
        t=-1
    if name not in namelist :
        cmd="INSERT INTO ATTENDANCE(name,time,date) VALUES(%s,%s,%s)"
        now = datetime.now()
        dtString = now.strftime('%Y-%m-%d %H:%M:%S')  
        dat=date.today()
        val=name,dtString,dat
        cursor.execute(cmd,val)
        mydb.commit()

encKnown = findEncodings(images)
print('Encoding Complete')


import cv2
import time
import tkinter.messagebox as messagebox

def ch1():
    cap = cv2.VideoCapture(0)  # Open webcam
    start_time = time.time()  # Start timer
    recognized = False  # Track if attendance is marked

    while time.time() - start_time < 10:  # Keep webcam open for 10 seconds
        success, img = cap.read()
        if not success:
            messagebox.showerror("Error", "Failed to capture image from webcam.")
            cap.release()
            return

        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        CurLoc = fc.face_locations(imgS)
        CurEnc = fc.face_encodings(imgS, CurLoc)

        for encodeFace, faceLoc in zip(CurEnc, CurLoc):
            matches = fc.compare_faces(encKnown, encodeFace)
            faceDis = fc.face_distance(encKnown, encodeFace)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex] and not recognized:  # Mark attendance only once
                name = classNames[matchIndex]
                markAttendance(name)
                recognized = True

        cv2.imshow("Webcam", img)

        if cv2.waitKey(1) & 0xFF == ord("q"):  # Allow user to exit early
            break

    cap.release()  # Close webcam
    cv2.destroyAllWindows()

    if recognized:
        messagebox.showinfo("Success", "Attendance Marked Successfully!")
    else:
        messagebox.showwarning("No Face Detected", "No recognized face found. Try again.")


def ch2():
    cursor=mydb.cursor()
    cursor.execute('select * from attendance')
    Attnd=cursor.fetchall()
    for i in Attnd:
        print(i)

import pandas as pd
from tkinter import ttk, filedialog, messagebox  # Import required modules

def download_to_excel():
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM ATTENDANCE")
    records = cursor.fetchall()

    if not records:
        messagebox.showwarning("No Data", "No attendance data available to export.")
        return

    df = pd.DataFrame(records, columns=['ID', 'Name', 'Time', 'Date'])  # Ensure correct column names
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                             filetypes=[("Excel Files", "*.xlsx")],
                                             title="Save Attendance Data")
    if file_path:
        df.to_excel(file_path, index=False)
        messagebox.showinfo("Success", "Attendance data saved successfully!")



def clear_attendance():
    cursor = mydb.cursor()
    cursor.execute("DELETE FROM ATTENDANCE")  # Clears all data
    mydb.commit()
    print("Attendance records cleared successfully!")


from tkinter import ttk  # Importing ttk for table formatting

def ch2a():
    root = Tk()
    root.title("Attendance Sheet")
    root.geometry("600x400")  # Increased window size for better view

    # Define Columns
    columns = ("ID", "Name", "Time", "Date")
    tree = ttk.Treeview(root, columns=columns, show="headings")

    # Define Headings
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Time", text="Time")
    tree.heading("Date", text="Date")

    tree.column("ID", width=50)
    tree.column("Name", width=150)
    tree.column("Time", width=150)
    tree.column("Date", width=100)

    tree.pack(expand=True, fill="both")

    # Fetch Attendance Data
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM ATTENDANCE")
    records = cursor.fetchall()

    for row in records:
        tree.insert("", "end", values=row)

    # Download Button
    download_btn = Button(root, text="Download as Excel", command=download_to_excel)
    download_btn.pack(pady=10)

    root.mainloop()






#gui
box = Tk(className="FACE RECOGNITION")
box.geometry("950x600")
image1 = Image.open("face.jpg")
image2= image1.resize((950,600))
test = ImageTk.PhotoImage(image2)
label1 = tkinter.Label(image=test)
label1.place(x=0, y=0)
w  =Text(box,height=2,width=30)
w.place()
w.insert(END, '\t\t\tFACE RECOGNITION')
button4 = Button(box, text='SHOW ATTENDANCE', width=20,command=ch2a)
button4.place(x=150 , y=250)
button5 = Button(box, text='MARK ATTENDANCE', width=20,command=ch1)
button5.place(x=150 , y=350)
button6 = Button(box, text='CLEAR ATTENDANCE', width=20, command=clear_attendance)
button6.place(x=150, y=450)
box.mainloop()
def showattend():
    box = Tk(className="FACE RECOGNITION")
    box.geometry("350x100")
    image1 = Image.open("face.jpg")
    image2= image1.resize((950,600))
    test = ImageTk.PhotoImage(image2)
    label1 = tkinter.Label(image=test)
    label1.place(x=0, y=0)
    w  =Text(box,height=2,width=30)
    w.place()
    w.insert(END, '\t\t\tFACE RECOGNITION')
button4 = Button(box, text='SHOW ATTENDANCE', width=20,command=ch2a)
button4.place(x=150 , y=250)
button5 = Button(box, text='MARK ATTENDANCE', width=20,command=ch1)
button5.place(x=150 , y=350)
box.mainloop()

