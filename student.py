from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
import cv2
import os
import numpy as np # Often used for image manipulation with OpenCV

class Student:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1366x768+0+0")
        self.root.title("Student Management System")
        self.root.config(bg="white")
   
        # --- Path Configurations ---
        self.attendance_file_path = r"C:\Users\chintu\OneDrive\Desktop\student\Python_Test_Projects\attendance.csv"
        self.data_img_dir = r"C:\Users\chintu\OneDrive\Desktop\student\Python_Test_Projects\data_img"

        # ADD THESE TWO LINES for face recognition paths and loading
        self.haarcascade_path = r"C:\Users\chintu\OneDrive\Desktop\student\Python_Test_Projects\haarcascade_frontalface_default.xml"
        self.trained_model_path = r"C:\Users\chintu\OneDrive\Desktop\student\Python_Test_Projects\clf.xml"

        # --- Variables ---
        self.var_dep = StringVar()
        self.var_course = StringVar()
        self.var_year = StringVar()
        self.var_semester = StringVar()
        self.var_std_id = StringVar()
        self.var_std_name = StringVar()
        self.var_div = StringVar()
        self.var_roll = StringVar()
        self.var_gender = StringVar()
        self.var_dob = StringVar()
        self.var_email = StringVar()
        self.var_mob = StringVar()
        self.var_address = StringVar()
        self.var_teacher = StringVar()
        self.var_radio1 = StringVar() # For PhotoSampleStatus
        self.var_face_id = StringVar() # Face_ID is now manually set/entered

        # --- Image Paths (Adjust these if your project structure changes) ---
        # Ensure these paths are correct for your system
        self.banner_img_path = r"C:\Users\chintu\OneDrive\Desktop\student\Python_Test_Projects\Images_GUI/banner.jpg"
        self.bg_img_path = r"C:\Users\chintu\OneDrive\Desktop\student\Python_Test_Projects\Images_GUI/bg3.jpg"
        self.haarcascade_path = r"C:\Users\chintu\OneDrive\Desktop\student\Python_Test_Projects\haarcascade_frontalface_default.xml"
        self.data_img_dir = r"C:\Users\chintu\OneDrive\Desktop\student\Python_Test_Projects\data_img"

        # Create data_img directory if it doesn't exist
        if not os.path.exists(self.data_img_dir):
            os.makedirs(self.data_img_dir)

        # --- Load Images ---
        try:
            img = Image.open(self.banner_img_path)
            img = img.resize((1366, 130), Image.Resampling.LANCZOS)
            self.photoimg = ImageTk.PhotoImage(img)
            f_lbl = Label(self.root, image=self.photoimg)
            f_lbl.place(x=0, y=0, width=1366, height=130)
        except FileNotFoundError:
            messagebox.showerror("Image Error", f"Banner image not found at: {self.banner_img_path}", parent=self.root)
            self.photoimg = None

        try:
            bg1 = Image.open(self.bg_img_path)
            bg1 = bg1.resize((1366, 768), Image.Resampling.LANCZOS)
            self.photobg1 = ImageTk.PhotoImage(bg1)
            bg_img = Label(self.root, image=self.photobg1)
            bg_img.place(x=0, y=130, width=1366, height=768)
        except FileNotFoundError:
            messagebox.showerror("Image Error", f"Background image not found at: {self.bg_img_path}", parent=self.root)
            self.photobg1 = None

        # --- Title ---
        title_lbl = Label(bg_img, text="STUDENT MANAGEMENT SYSTEM", font=("times new roman", 35, "bold"), bg="white", fg="darkblue")
        title_lbl.place(x=0, y=0, width=1366, height=45)

        # --- Main Frame ---
        main_frame = Frame(bg_img, bd=2, bg="white")
        main_frame.place(x=20, y=50, width=1320, height=600)

        # --- Left Frame (Student Details) ---
        Left_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE, text="Student Details", font=("times new roman", 12, "bold"))
        Left_frame.place(x=10, y=10, width=660, height=580)

        # --- Current Course Information Frame ---
        current_course_frame = LabelFrame(Left_frame, bd=2, bg="white", relief=RIDGE, text="Current Course Information", font=("times new roman", 12, "bold"))
        current_course_frame.place(x=5, y=15, width=640, height=150)

        # Department
        dep_label = Label(current_course_frame, text="Department", font=("times new roman", 12, "bold"), bg="white")
        dep_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)
        dep_combo = ttk.Combobox(current_course_frame, textvariable=self.var_dep, font=("times new roman", 12, "bold"), state="readonly", width=17)
        dep_combo["values"] = ("Select Department", "Computer Science", "IT", "Civil", "Mechanical", "Electrical", "ECE", "CSE(AIML)", "Data Science", "Computer Networks", "IOT", "Cyber Security", "Aeronautical Engineering", "Robotics")
        dep_combo.current(0)
        dep_combo.grid(row=0, column=1, padx=10, pady=10, sticky=W)

        # Course
        course_label = Label(current_course_frame, text="Course", font=("times new roman", 12, "bold"), bg="white")
        course_label.grid(row=0, column=2, padx=10, pady=10, sticky=W)
        course_combo = ttk.Combobox(current_course_frame, textvariable=self.var_course, font=("times new roman", 12, "bold"), state="readonly", width=17)
        course_combo["values"] = ("Select Course", "Java", "Artificial Intelligence", "Machine Learning", "C", "C++", "Python", "#C")
        course_combo.current(0)
        course_combo.grid(row=0, column=3, padx=10, pady=10, sticky=W)

        # Year
        year_label = Label(current_course_frame, text="Year", font=("times new roman", 12, "bold"), bg="white")
        year_label.grid(row=1, column=0, padx=10, pady=10, sticky=W)
        year_combo = ttk.Combobox(current_course_frame, textvariable=self.var_year, font=("times new roman", 12, "bold"), state="readonly", width=17)
        year_combo["values"] = ("Select Year", "2021-22", "2022-23", "2023-24", "2024-25", "2025-26", "2026-27", "2027-28")
        year_combo.current(0)
        year_combo.grid(row=1, column=1, padx=10, pady=10, sticky=W)

        # Semester
        semester_label = Label(current_course_frame, text="Semester", font=("times new roman", 12, "bold"), bg="white")
        semester_label.grid(row=1, column=2, padx=10, pady=10, sticky=W)
        semester_combo = ttk.Combobox(current_course_frame, textvariable=self.var_semester, font=("times new roman", 12, "bold"), state="readonly", width=17)
        semester_combo["values"] = ("Select Semester", "Semester-1", "Semester-2", "Semester-3", "Semester-4", "Semester-5", "Semester-6", "Semester-7", "Semester-8")
        semester_combo.current(0)
        semester_combo.grid(row=1, column=3, padx=10, pady=10, sticky=W)

        # --- Class Student Information Frame ---
        class_student_frame = LabelFrame(Left_frame, bd=2, bg="white", relief=RIDGE, text="Class Student Information", font=("times new roman", 12, "bold"))
        class_student_frame.place(x=5, y=170, width=640, height=360)

        # Student ID
        studentId_label = Label(class_student_frame, text="Student ID:", font=("times new roman", 12, "bold"), bg="white")
        studentId_label.grid(row=0, column=0, padx=10, pady=5, sticky=W)
        studentId_entry = ttk.Entry(class_student_frame, textvariable=self.var_std_id, width=20, font=("times new roman", 12, "bold"))
        studentId_entry.grid(row=0, column=1, padx=10, pady=5, sticky=W)

        # Student Name
        studentName_label = Label(class_student_frame, text="Student Name:", font=("times new roman", 12, "bold"), bg="white")
        studentName_label.grid(row=0, column=2, padx=10, pady=5, sticky=W)
        studentName_entry = ttk.Entry(class_student_frame, textvariable=self.var_std_name, width=20, font=("times new roman", 12, "bold"))
        studentName_entry.grid(row=0, column=3, padx=10, pady=5, sticky=W)

        # Class Division
        class_div_label = Label(class_student_frame, text="Class Division:", font=("times new roman", 12, "bold"), bg="white")
        class_div_label.grid(row=1, column=0, padx=10, pady=5, sticky=W)
        div_combo = ttk.Combobox(class_student_frame, textvariable=self.var_div, font=("times new roman", 12, "bold"), state="readonly", width=18)
        div_combo["values"] = ("Select Division", "A", "B", "C")
        div_combo.current(0)
        div_combo.grid(row=1, column=1, padx=10, pady=5, sticky=W)

        # Roll No
        roll_no_label = Label(class_student_frame, text="Roll No:", font=("times new roman", 12, "bold"), bg="white")
        roll_no_label.grid(row=1, column=2, padx=10, pady=5, sticky=W)
        roll_no_entry = ttk.Entry(class_student_frame, textvariable=self.var_roll, width=20, font=("times new roman", 12, "bold"))
        roll_no_entry.grid(row=1, column=3, padx=10, pady=5, sticky=W)

        # Gender
        gender_label = Label(class_student_frame, text="Gender:", font=("times new roman", 12, "bold"), bg="white")
        gender_label.grid(row=2, column=0, padx=10, pady=5, sticky=W)
        gender_combo = ttk.Combobox(class_student_frame, textvariable=self.var_gender, font=("times new roman", 12, "bold"), state="readonly", width=18)
        gender_combo["values"] = ("Select Gender", "Male", "Female", "Other")
        gender_combo.current(0)
        gender_combo.grid(row=2, column=1, padx=10, pady=5, sticky=W)

        # Date of Birth
        dob_label = Label(class_student_frame, text="DOB:", font=("times new roman", 12, "bold"), bg="white")
        dob_label.grid(row=2, column=2, padx=10, pady=5, sticky=W)
        dob_entry = ttk.Entry(class_student_frame, textvariable=self.var_dob, width=20, font=("times new roman", 12, "bold"))
        dob_entry.grid(row=2, column=3, padx=10, pady=5, sticky=W)

        # Email
        email_label = Label(class_student_frame, text="Email:", font=("times new roman", 12, "bold"), bg="white")
        email_label.grid(row=3, column=0, padx=10, pady=5, sticky=W)
        email_entry = ttk.Entry(class_student_frame, textvariable=self.var_email, width=20, font=("times new roman", 12, "bold"))
        email_entry.grid(row=3, column=1, padx=10, pady=5, sticky=W)

        # Phone No
        phone_label = Label(class_student_frame, text="Phone No:", font=("times new roman", 12, "bold"), bg="white")
        phone_label.grid(row=3, column=2, padx=10, pady=5, sticky=W)
        phone_entry = ttk.Entry(class_student_frame, textvariable=self.var_mob, width=20, font=("times new roman", 12, "bold"))
        phone_entry.grid(row=3, column=3, padx=10, pady=5, sticky=W)

        # Address
        address_label = Label(class_student_frame, text="Address:", font=("times new roman", 12, "bold"), bg="white")
        address_label.grid(row=4, column=0, padx=10, pady=5, sticky=W)
        address_entry = ttk.Entry(class_student_frame, textvariable=self.var_address, width=20, font=("times new roman", 12, "bold"))
        address_entry.grid(row=4, column=1, padx=10, pady=5, sticky=W)

        # Teacher Name
        teacher_label = Label(class_student_frame, text="Teacher Name:", font=("times new roman", 12, "bold"), bg="white")
        teacher_label.grid(row=4, column=2, padx=10, pady=5, sticky=W)
        teacher_entry = ttk.Entry(class_student_frame, textvariable=self.var_teacher, width=20, font=("times new roman", 12, "bold"))
        teacher_entry.grid(row=4, column=3, padx=10, pady=5, sticky=W)

        # Face_ID (Now Modifiable/Enterable)
        face_id_label = Label(class_student_frame, text="Face ID:", font=("times new roman", 12, "bold"), bg="white")
        face_id_label.grid(row=5, column=0, padx=10, pady=5, sticky=W)
        face_id_entry = ttk.Entry(class_student_frame, textvariable=self.var_face_id, width=20, font=("times new roman", 12, "bold")) # Removed state="readonly"
        face_id_entry.grid(row=5, column=1, padx=10, pady=5, sticky=W)

        # Radio Buttons for Photo Sample Status
        radiobtn1 = ttk.Radiobutton(class_student_frame, variable=self.var_radio1, text="Take Photo Sample", value="Yes")
        radiobtn1.grid(row=5, column=2, padx=10, pady=5, sticky=W)

        radiobtn2 = ttk.Radiobutton(class_student_frame, variable=self.var_radio1, text="No Photo Sample", value="No")
        radiobtn2.grid(row=5, column=3, padx=10, pady=5, sticky=W)

        # --- Buttons Frame ---
        btn_frame = Frame(class_student_frame, bd=2, relief=RIDGE, bg="white")
        btn_frame.place(x=0, y=240, width=635, height=70) # Adjusted y position

        # Save Button
        save_btn = Button(btn_frame, text="Save", command=self.add_data, width=15, font=("times new roman", 12, "bold"), bg="blue", fg="white")
        save_btn.grid(row=0, column=0, padx=5, pady=10)

        # Update Button
        update_btn = Button(btn_frame, text="Update", command=self.update_data, width=15, font=("times new roman", 12, "bold"), bg="blue", fg="white")
        update_btn.grid(row=0, column=1, padx=5, pady=10)

        # Delete Button
        delete_btn = Button(btn_frame, text="Delete", command=self.delete_data, width=15, font=("times new roman", 12, "bold"), bg="blue", fg="white")
        delete_btn.grid(row=0, column=2, padx=5, pady=10)

        # Reset Button
        reset_btn = Button(btn_frame, text="Reset", command=self.reset_data, width=15, font=("times new roman", 12, "bold"), bg="blue", fg="white")
        reset_btn.grid(row=0, column=3, padx=5, pady=10)

        # --- Button Frame 2 (for photo actions) ---
        btn_frame1 = Frame(class_student_frame, bd=2, relief=RIDGE, bg="white")
        btn_frame1.place(x=0, y=310, width=635, height=35) # Adjusted y position

        # Take Photo Button
        take_photo_btn = Button(btn_frame1, text="Take Photo Sample", command=self.generate_dataset, width=30, font=("times new roman", 12, "bold"), bg="blue", fg="white")
        take_photo_btn.grid(row=0, column=0, padx=170, pady=0) # Adjusted padx

        # --- Right Frame (Student Data Table) ---
        Right_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE, text="Student Data", font=("times new roman", 12, "bold")) # Changed text
        Right_frame.place(x=680, y=10, width=630, height=580)

        # --- Search System ---
        search_frame = LabelFrame(Right_frame, bd=2, bg="white", relief=RIDGE, text="Search System", font=("times new roman", 12, "bold"))
        search_frame.place(x=5, y=15, width=615, height=70)

        search_label = Label(search_frame, text="Search By:", font=("times new roman", 12, "bold"), bg="white")
        search_label.grid(row=0, column=0, padx=10, pady=5, sticky=W)

        self.var_search_combo = StringVar()
        search_combo = ttk.Combobox(search_frame, textvariable=self.var_search_combo, font=("times new roman", 12, "bold"), state="readonly", width=15)
        search_combo["values"] = ("Select", "Roll", "Phone", "Student_id") # Changed to match DB column names
        search_combo.current(0)
        search_combo.grid(row=0, column=1, padx=2, pady=10, sticky=W)

        self.var_search = StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.var_search, width=15, font=("times new roman", 12, "bold"))
        search_entry.grid(row=0, column=2, padx=10, pady=5, sticky=W)

        search_btn = Button(search_frame, text="Search", command=self.search_data, width=10, font=("times new roman", 12, "bold"), bg="blue", fg="white")
        search_btn.grid(row=0, column=3, padx=4)

        showAll_btn = Button(search_frame, text="Show All", command=self.fetch_data, width=10, font=("times new roman", 12, "bold"), bg="blue", fg="white")
        showAll_btn.grid(row=0, column=4, padx=4)

        # --- Table Frame ---
        table_frame = Frame(Right_frame, bd=2, bg="white", relief=RIDGE)
        table_frame.place(x=5, y=100, width=615, height=450)

        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

        # IMPORTANT: The number of columns here must match your actual database table
        # If 'Face_ID' is the first column in your DB, it should be first here too.
        self.student_table = ttk.Treeview(table_frame, column=("face_id", "dep", "course", "year", "sem", "id", "name", "div", "roll", "gender", "dob", "email", "phone", "address", "teacher", "photo"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)

        # Define headings and column widths
        self.student_table.heading("face_id", text="Face ID")
        self.student_table.heading("dep", text="Department")
        self.student_table.heading("course", text="Course")
        self.student_table.heading("year", text="Year")
        self.student_table.heading("sem", text="Semester")
        self.student_table.heading("id", text="StudentID")
        self.student_table.heading("name", text="Name")
        self.student_table.heading("div", text="Division")
        self.student_table.heading("roll", text="Roll No")
        self.student_table.heading("gender", text="Gender")
        self.student_table.heading("dob", text="DOB")
        self.student_table.heading("email", text="Email")
        self.student_table.heading("phone", text="Phone")
        self.student_table.heading("address", text="Address")
        self.student_table.heading("teacher", text="Teacher")
        self.student_table.heading("photo", text="PhotoSampleStatus")
        self.student_table["show"] = "headings"

        # Set column widths
        self.student_table.column("face_id", width=70)
        self.student_table.column("dep", width=100)
        self.student_table.column("course", width=100)
        self.student_table.column("year", width=80)
        self.student_table.column("sem", width=80)
        self.student_table.column("id", width=80)
        self.student_table.column("name", width=120)
        self.student_table.column("div", width=70)
        self.student_table.column("roll", width=70)
        self.student_table.column("gender", width=80)
        self.student_table.column("dob", width=90)
        self.student_table.column("email", width=120)
        self.student_table.column("phone", width=100)
        self.student_table.column("address", width=150)
        self.student_table.column("teacher", width=120)
        self.student_table.column("photo", width=120)

        self.student_table.pack(fill=BOTH, expand=1)
        self.student_table.bind("<<TreeviewSelect>>", self.get_cursor)
        self.fetch_data() # Load data when the application starts
   
        try:
            self.face_classifier = cv2.CascadeClassifier(self.haarcascade_path)
            self.recognizer = cv2.face.LBPHFaceRecognizer_create()
            if os.path.exists(self.trained_model_path):
                self.recognizer.read(self.trained_model_path)
                print("Trained model loaded successfully.")
            else:
                print(f"Warning: Trained model not found at {self.trained_model_path}. Recognition might not work.")
        except Exception as e:
            messagebox.showerror("Recognition Init Error", f"Failed to load face recognition components: {e}", parent=self.root)
            self.face_classifier = None
            self.recognizer = None
 
    # --- Database Connection Helper ---
    def get_db_connection(self):
        try:
            conn = mysql.connector.connect(username='root', password='Micky@1404sai', host='localhost', database='face_recognition')
            return conn
        except mysql.connector.Error as err:
            messagebox.showerror("Database Connection Error", f"Failed to connect to database: {err}", parent=self.root)
            return None

    # --- CRUD Functions ---
    def add_data(self):
        # Validate all required fields (now including Face_ID)
        if (self.var_dep.get() == "Select Department" or
            self.var_course.get() == "Select Course" or
            self.var_year.get() == "Select Year" or
            self.var_semester.get() == "Select Semester" or
            self.var_std_id.get() == "" or
            self.var_std_name.get() == "" or
            self.var_div.get() == "Select Division" or
            self.var_roll.get() == "" or
            self.var_gender.get() == "Select Gender" or
            self.var_dob.get() == "" or
            self.var_email.get() == "" or
            self.var_mob.get() == "" or
            self.var_address.get() == "" or
            self.var_teacher.get() == "" or
            self.var_radio1.get() == "" or
            self.var_face_id.get() == ""): # Face_ID is now a required input
            messagebox.showerror("Error", "All fields are required!", parent=self.root)
            return

        conn = self.get_db_connection()
        if not conn: return

        try:
            my_cursor = conn.cursor()

            # --- Check if Student ID already exists ---
            my_cursor.execute("SELECT Student_id FROM student WHERE Student_id = %s", (self.var_std_id.get(),))
            if my_cursor.fetchone():
                messagebox.showerror("Error", "Student with this ID already exists. Please use a unique Student ID.", parent=self.root)
                return

            # --- Check if Face_ID already exists ---
            my_cursor.execute("SELECT Face_ID FROM student WHERE Face_ID = %s", (self.var_face_id.get(),))
            if my_cursor.fetchone():
                messagebox.showerror("Error", "Face ID already exists. Please enter a unique Face ID.", parent=self.root)
                return

            # Insert statement - Face_ID is now included in the values
            my_cursor.execute("INSERT INTO student (Face_ID, Dep, course, Year, Semester, Student_id, Name, Division, Roll, Gender, Dob, Email, Phone, Address, Teacher, PhotoSample) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (
                self.var_face_id.get(), # Included Face_ID here
                self.var_dep.get(),
                self.var_course.get(),
                self.var_year.get(),
                self.var_semester.get(),
                self.var_std_id.get(),
                self.var_std_name.get(),
                self.var_div.get(),
                self.var_roll.get(),
                self.var_gender.get(),
                self.var_dob.get(),
                self.var_email.get(),
                self.var_mob.get(),
                self.var_address.get(),
                self.var_teacher.get(),
                self.var_radio1.get()
            ))
            conn.commit()
            self.fetch_data()
            messagebox.showinfo("Success", "Student details added successfully!", parent=self.root)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to add data: {err}", parent=self.root)
        finally:
            if conn: conn.close()

    def fetch_data(self):
        conn = self.get_db_connection()
        if not conn: return

        try:
            my_cursor = conn.cursor()
            my_cursor.execute("SELECT * FROM student")
            data = my_cursor.fetchall()

            if len(data) != 0:
                self.student_table.delete(*self.student_table.get_children())
                for i in data:
                    self.student_table.insert("", END, values=i)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to fetch data: {err}", parent=self.root)
        finally:
            if conn: conn.close()

    def get_cursor(self, event=""):
        cursor_row = self.student_table.focus()
        content = self.student_table.item(cursor_row)
        data = content["values"]

        # Ensure 'data' has enough elements based on your DB columns (16 columns)
        if len(data) >= 16:
            self.var_face_id.set(data[0]) # Face_ID is at index 0 in the tuple
            self.var_dep.set(data[1])
            self.var_course.set(data[2])
            self.var_year.set(data[3])
            self.var_semester.set(data[4])
            self.var_std_id.set(data[5])
            self.var_std_name.set(data[6])
            self.var_div.set(data[7])
            self.var_roll.set(data[8])
            self.var_gender.set(data[9])
            self.var_dob.set(data[10])
            self.var_email.set(data[11])
            self.var_mob.set(data[12])
            self.var_address.set(data[13])
            self.var_teacher.set(data[14])
            self.var_radio1.set(data[15])
        else:
            self.reset_data() # Clear fields if incomplete data is selected

    def update_data(self):
        # Validate essential fields for update
        if (self.var_dep.get() == "Select Department" or
            self.var_std_name.get() == "" or
            self.var_std_id.get() == "" or
            self.var_face_id.get() == ""): # Ensure Face_ID is also present for update criteria
            messagebox.showerror("Error", "Student ID, Face ID, Department, and Name are required for update.", parent=self.root)
            return

        update = messagebox.askyesno("Update", "Do you want to update this student's details?", parent=self.root)
        if not update:
            return

        conn = self.get_db_connection()
        if not conn: return

        try:
            my_cursor = conn.cursor()
            # Update statement - Face_ID is used in WHERE clause to identify the record
            # Face_ID itself is NOT updated here, as it's meant to be an immutable identifier
            my_cursor.execute("UPDATE student SET Dep=%s, course=%s, Year=%s, Semester=%s, Name=%s, Division=%s, Roll=%s, Gender=%s, Dob=%s, Email=%s, Phone=%s, Address=%s, Teacher=%s, PhotoSample=%s WHERE Student_id=%s AND Face_ID=%s", (
                self.var_dep.get(),
                self.var_course.get(),
                self.var_year.get(),
                self.var_semester.get(),
                self.var_std_name.get(),
                self.var_div.get(),
                self.var_roll.get(),
                self.var_gender.get(),
                self.var_dob.get(),
                self.var_email.get(),
                self.var_mob.get(),
                self.var_address.get(),
                self.var_teacher.get(),
                self.var_radio1.get(),
                self.var_std_id.get(),
                self.var_face_id.get() # Used here for identification in WHERE clause
            ))
            conn.commit()
            self.fetch_data()
            messagebox.showinfo("Success", "Student details successfully updated!", parent=self.root)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to update data: {err}", parent=self.root)
        finally:
            if conn: conn.close()

    def delete_data(self):
        if self.var_std_id.get() == "" or self.var_face_id.get() == "":
            messagebox.showerror("Error", "Student ID and Face ID are required to delete a student.", parent=self.root)
            return

        delete = messagebox.askyesno("Delete Student", "Do you want to delete this student and their associated photo samples?", parent=self.root)
        if not delete:
            return

        conn = self.get_db_connection()
        if not conn: return

        try:
            cursor = conn.cursor()

            # Get the Face_ID associated with the student to delete photo samples
            # Using both Student_id and Face_ID for a more specific deletion
            cursor.execute("SELECT Face_ID FROM student WHERE Student_id = %s AND Face_ID = %s", (self.var_std_id.get(), self.var_face_id.get()))
            result = cursor.fetchone()

            face_id_to_delete_samples = result[0] if result else None

            # Delete record from database
            sql = "DELETE FROM student WHERE Student_id=%s AND Face_ID=%s"
            val = (self.var_std_id.get(), self.var_face_id.get())
            cursor.execute(sql, val)
            conn.commit()

            # Delete associated photo samples if Face_ID was found
            if face_id_to_delete_samples:
                for filename in os.listdir(self.data_img_dir):
                    if filename.startswith(f"{face_id_to_delete_samples}_"):
                        try:
                            os.remove(os.path.join(self.data_img_dir, filename))
                        except OSError as e:
                            print(f"Error deleting photo {filename}: {e}") # Log error but don't stop process

            self.fetch_data()
            self.reset_data()
            messagebox.showinfo("Delete", "Successfully deleted student details and associated photos!", parent=self.root)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to delete data: {err}", parent=self.root)
        except Exception as es:
            messagebox.showerror("Error", f"An unexpected error occurred during deletion: {str(es)}", parent=self.root)
        finally:
            if conn: conn.close()

    def reset_data(self):
        self.var_dep.set("Select Department")
        self.var_course.set("Select Course")
        self.var_year.set("Select Year")
        self.var_semester.set("Select Semester")
        self.var_std_id.set("")
        self.var_std_name.set("")
        self.var_div.set("Select Division")
        self.var_roll.set("")
        self.var_gender.set("Select Gender")
        self.var_dob.set("")
        self.var_email.set("")
        self.var_mob.set("")
        self.var_address.set("")
        self.var_teacher.set("")
        self.var_radio1.set("")
        self.var_face_id.set("") # Clear Face ID on reset

    def search_data(self):
        if self.var_search_combo.get() == "Select" or self.var_search.get() == "":
            messagebox.showerror("Error", "Please select a search criterion and enter a value.", parent=self.root)
            return

        conn = self.get_db_connection()
        if not conn: return

        try:
            my_cursor = conn.cursor()
            search_by = self.var_search_combo.get()
            search_value = self.var_search.get()

            # Ensure column names match your database schema
            if search_by == "Roll":
                my_cursor.execute("SELECT * FROM student WHERE Roll = %s", (search_value,))
            elif search_by == "Phone":
                my_cursor.execute("SELECT * FROM student WHERE Phone = %s", (search_value,))
            elif search_by == "Student_id":
                my_cursor.execute("SELECT * FROM student WHERE Student_id = %s", (search_value,))
            else:
                messagebox.showerror("Error", "Invalid search criterion selected.", parent=self.root)
                conn.close()
                return

            data = my_cursor.fetchall()

            self.student_table.delete(*self.student_table.get_children())
            if len(data) != 0:
                for i in data:
                    self.student_table.insert("", END, values=i)
                messagebox.showinfo("Search Results", f"{len(data)} record(s) found.", parent=self.root)
            else:
                messagebox.showinfo("No Data", "No data found for your search criteria.", parent=self.root)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to search data: {err}", parent=self.root)
        finally:
            if conn: conn.close()
    
    def face_cropped(self, img):
        try:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            if self.face_classifier is None:
                return None
            faces = self.face_classifier.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                face_cropped_region = img[y:y+h, x:x+w]
                return face_cropped_region
            return None
        except Exception as e:
            return None


    def generate_dataset(self):
        if self.var_face_id.get() == "" or self.var_radio1.get() != "Yes":
            messagebox.showerror("Error", "Face ID is required, and 'Take Photo Sample' must be selected.", parent=self.root)
            return

        conn = self.get_db_connection()
        if not conn: return
        try:
            my_cursor = conn.cursor()
            # Double-check column names here: 'Student_id' and 'Face_ID' match your actual table?
            my_cursor.execute("SELECT Student_id FROM student WHERE Student_id = %s AND Face_ID = %s", (self.var_std_id.get(), self.var_face_id.get()))
            student_exists_in_db = my_cursor.fetchone()
            if not student_exists_in_db:
                messagebox.showerror("Error", "No student found with the provided Student ID and Face ID. Please save student details first.", parent=self.root)
                return
        except mysql.connector.Error as err:
            messagebox.showerror("DB Error", f"Error checking student existence: {err}", parent=self.root)
            return
        finally:
            if conn: conn.close()

        face_id_to_capture = self.var_face_id.get()
        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            messagebox.showerror("Camera Error", "Failed to open webcam.", parent=self.root)
            return

        img_id = 0
        recognition_checked = False
        check_frame_count = 0
        MAX_CHECK_FRAMES = 50

        messagebox.showinfo("Prepare for Photo Samples", "Look at the camera. The system will first check if you are an existing student. Please hold still.", parent=self.root)

        while True:
            ret, img = cam.read()
            if not ret:
                messagebox.showerror("Camera Error", "Failed to capture image from webcam.", parent=self.root)
                break

            img = cv2.flip(img, 1)

            if not recognition_checked and self.recognizer and self.face_classifier and not self.recognizer.empty(): # Changed empty() == False to not empty()
                gray_for_rec = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces_for_rec = self.face_classifier.detectMultiScale(gray_for_rec, 1.3, 5)

                if len(faces_for_rec) > 0:
                    (x_rec, y_rec, w_rec, h_rec) = faces_for_rec[0]
                    roi_gray_rec = gray_for_rec[y_rec:y_rec+h_rec, x_rec:x_rec+w_rec]
                    roi_gray_rec = cv2.resize(roi_gray_rec, (200, 200))

                    try:
                        id_predicted, confidence = self.recognizer.predict(roi_gray_rec)

                        if confidence < 70:
                            conn = self.get_db_connection()
                            student_details = None
                            if conn:
                                try:
                                    my_cursor = conn.cursor()
                                    # --- CRITICAL CHANGE HERE ---
                                    # Ensure these column names ('Student_id', 'Name', 'Face_ID')
                                    # EXACTLY match your database table's column names, including case.
                                    my_cursor.execute("SELECT Student_id, Name, Face_ID FROM student WHERE Face_ID = %s", (int(id_predicted),))
                                    student_details = my_cursor.fetchone() # This will be (Student_id, Name, Face_ID)
                                except Exception as e:
                                    print(f"DB error fetching details for recognized ID: {e}")
                                    messagebox.showwarning("DB Fetch Error", f"Could not fetch student details: {e}", parent=self.root)
                                finally:
                                    conn.close()

                            if student_details:
                                # Unpack the tuple correctly
                                existing_student_id, existing_name, existing_face_id = student_details

                                if str(existing_face_id) == face_id_to_capture:
                                    messagebox.showinfo("Student Exists",
                                                        f"Hello {existing_name}! You are already registered with Face ID: {existing_face_id} and Student ID: {existing_student_id}. No new photo samples needed.",
                                                        parent=self.root)
                                    cam.release()
                                    cv2.destroyAllWindows()
                                    return
                                else:
                                    messagebox.showwarning("Already Existing Student",
                                                        f"You are recognized as an existing student! "
                                                        f"Name: {existing_name}, Student ID: {existing_student_id}, Face ID: {existing_face_id}. "
                                                        f"You are not allowed to register again with a new Face ID.",
                                                        parent=self.root)
                                    cam.release()
                                    cv2.destroyAllWindows()
                                    return
                            else:
                                cv2.putText(img, "UNKNOWN/DB ID NOT FOUND", (x_rec, y_rec - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 165, 255), 2)
                        else:
                            cv2.putText(img, "Scanning...", (x_rec, y_rec - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
                    except cv2.error as e:
                        print(f"Error during prediction: {e}. Model might not be trained or input invalid.")
                        cv2.putText(img, "TRAIN MODEL!", (x_rec, y_rec - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                        if "model is not computed yet" in str(e) and check_frame_count > MAX_CHECK_FRAMES:
                            messagebox.showerror("Training Required", "The face recognition model is not trained. Please train the model before taking samples.", parent=self.root)
                            cam.release()
                            cv2.destroyAllWindows()
                            return
                else:
                    cv2.putText(img, "Align Face for Check", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                check_frame_count += 1
                if check_frame_count > MAX_CHECK_FRAMES:
                    recognition_checked = True
                    messagebox.showinfo("Proceeding", "No existing student recognized, proceeding to take new photo samples.", parent=self.root)

            if recognition_checked:
                face = self.face_cropped(img)
                if face is not None:
                    img_id += 1
                    face = cv2.resize(face, (200, 200))
                    face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

                    file_name_path = os.path.join(self.data_img_dir, f"{face_id_to_capture}_{img_id}.jpg")
                    cv2.imwrite(file_name_path, face)

                    cv2.putText(img, f"Samples: {img_id}/100", (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                else:
                    cv2.putText(img, "No Face Detected", (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)

            cv2.imshow("Capturing Face Samples (Press 'q' to quit)", img)

            if cv2.waitKey(1) == ord('q') or (recognition_checked and img_id >= 100):
                break

        cam.release()
        cv2.destroyAllWindows()
        if recognition_checked and img_id >= 100:
            messagebox.showinfo("Dataset Generation", f"Collected {img_id} face samples for Face ID: {face_id_to_capture}.", parent=self.root)
            conn = self.get_db_connection()
            if conn:
                try:
                    my_cursor = conn.cursor()
                    my_cursor.execute("UPDATE student SET PhotoSample = %s WHERE Student_id = %s AND Face_ID = %s",
                                     ("Yes", self.var_std_id.get(), self.var_face_id.get()))
                    conn.commit()
                except mysql.connector.Error as err:
                    print(f"Warning: Could not update PhotoSample status in DB: {err}")
                finally:
                    conn.close()
        elif not recognition_checked:
            pass
        else:
            # If img_id is 0, it means no samples were taken, possibly due to no face or early exit.
            # The "already exists" message should cover the primary reason.
            pass # No message needed here if the "already exists" message is handled above


    def update_photo_sample_status(self, face_id, status):
        conn = self.get_db_connection()
        if not conn: return
        try:
            my_cursor = conn.cursor()
            my_cursor.execute("UPDATE student SET PhotoSample = %s WHERE Face_ID = %s", (status, face_id))
            conn.commit()
        except mysql.connector.Error as err:
            messagebox.showerror("DB Update Error", f"Failed to update photo sample status: {err}", parent=self.root)
        finally:
            if conn: conn.close()

if __name__ == "__main__":
    root = Tk()
    obj = Student(root)
    root.mainloop()