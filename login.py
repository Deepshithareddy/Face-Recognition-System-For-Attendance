from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
from register import Register 
import mysql.connector
import bcrypt # Import bcrypt

# Ensure these classes are defined in their respective files or above this code
# if they are not in separate files.
# For this example, I'm assuming they are in separate files or will be defined
# before Face_Recognition_System is used.
from train import Train
from student import Student
from face_recognition import Face_Recognition
from attendance import Attendance
from developer import Developer
from helpsupport import Helpsupport
import os


# =====================main program Face deteion system====================
# Define Face_Recognition_System before Login, as Login uses it.
class Face_Recognition_System:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1366x768+0+0")
        self.root.title("Face_Recognition_System")

        # This part is image labels setting start
        # first header image
        img = Image.open(r"C:\Users\chintu\OneDrive\Desktop\student\Python_Test_Projects\Images_GUI\banner.jpg")
        img = img.resize((1366, 130), Image.Resampling.LANCZOS)
        self.photoimg = ImageTk.PhotoImage(img)

        # set image as lable
        f_lb1 = Label(self.root, image=self.photoimg)
        f_lb1.place(x=0, y=0, width=1366, height=130)

        # backgorund image
        bg1 = Image.open(r"C:\Users\chintu\OneDrive\Desktop\student\Python_Test_Projects\Images_GUI\bg3.jpg")
        bg1 = bg1.resize((1366, 768), Image.Resampling.LANCZOS)
        self.photobg1 = ImageTk.PhotoImage(bg1)

        # set image as lable
        bg_img = Label(self.root, image=self.photobg1)
        bg_img.place(x=0, y=130, width=1366, height=768)

        # title section
        title_lb1 = Label(bg_img, text="Attendance Management System Using Facial Recognition",
                          font=("verdana", 30, "bold"), bg="white", fg="navyblue")
        title_lb1.place(x=0, y=0, width=1366, height=45)

        # Create buttons below the section
        # -------------------------------------------------------------------------------------------------------------------
        # student button 1
        std_img_btn = Image.open(r"C:\Users\chintu\OneDrive\Desktop\student\Python_Test_Projects\Images_GUI\std1.jpg")
        std_img_btn = std_img_btn.resize((180, 180), Image.Resampling.LANCZOS)
        self.std_img1 = ImageTk.PhotoImage(std_img_btn)

        std_b1 = Button(bg_img, command=self.student_pannels, image=self.std_img1, cursor="hand2")
        std_b1.place(x=250, y=100, width=180, height=180)

        std_b1_1 = Button(bg_img, command=self.student_pannels, text="Student Panel", cursor="hand2",
                          font=("tahoma", 15, "bold"), bg="white", fg="navyblue")
        std_b1_1.place(x=250, y=280, width=180, height=45)

        # Detect Face  button 2
        det_img_btn = Image.open(r"C:\Users\chintu\OneDrive\Desktop\student\Python_Test_Projects\Images_GUI\det1.jpg")
        det_img_btn = det_img_btn.resize((180, 180), Image.Resampling.LANCZOS)
        self.det_img1 = ImageTk.PhotoImage(det_img_btn)

        det_b1 = Button(bg_img, command=self.face_recog, image=self.det_img1, cursor="hand2", )
        det_b1.place(x=480, y=100, width=180, height=180)

        det_b1_1 = Button(bg_img, command=self.face_recog, text="Face Detector", cursor="hand2",
                          font=("tahoma", 15, "bold"), bg="white", fg="navyblue")
        det_b1_1.place(x=480, y=280, width=180, height=45)

        # Attendance System  button 3
        att_img_btn = Image.open(r"C:\Users\chintu\OneDrive\Desktop\student\Python_Test_Projects\Images_GUI\att.jpg")
        att_img_btn = att_img_btn.resize((180, 180), Image.Resampling.LANCZOS)
        self.att_img1 = ImageTk.PhotoImage(att_img_btn)

        att_b1 = Button(bg_img, command=self.attendance_pannel, image=self.att_img1, cursor="hand2", )
        att_b1.place(x=710, y=100, width=180, height=180)

        att_b1_1 = Button(bg_img, command=self.attendance_pannel, text="Attendance", cursor="hand2",
                          font=("tahoma", 15, "bold"), bg="white", fg="navyblue")
        att_b1_1.place(x=710, y=280, width=180, height=45)

        # Help  Support  button 4
        hlp_img_btn = Image.open(r"C:\Users\chintu\OneDrive\Desktop\student\Python_Test_Projects\Images_GUI\hlp.jpg")
        hlp_img_btn = hlp_img_btn.resize((180, 180), Image.Resampling.LANCZOS)
        self.hlp_img1 = ImageTk.PhotoImage(hlp_img_btn)

        hlp_b1 = Button(bg_img, command=self.helpSupport, image=self.hlp_img1, cursor="hand2", )
        hlp_b1.place(x=940, y=100, width=180, height=180)

        hlp_b1_1 = Button(bg_img, command=self.helpSupport, text="Help Support", cursor="hand2",
                          font=("tahoma", 15, "bold"), bg="white", fg="navyblue")
        hlp_b1_1.place(x=940, y=280, width=180, height=45)

        # Top 4 buttons end.......
        # ---------------------------------------------------------------------------------------------------------------------------
        # Start below buttons.........
        # Train   button 5
        tra_img_btn = Image.open(r"C:\Users\chintu\OneDrive\Desktop\student\Python_Test_Projects\Images_GUI\tra1.jpg")
        tra_img_btn = tra_img_btn.resize((180, 180), Image.Resampling.LANCZOS)
        self.tra_img1 = ImageTk.PhotoImage(tra_img_btn)

        tra_b1 = Button(bg_img, command=self.train_pannels, image=self.tra_img1, cursor="hand2", )
        tra_b1.place(x=250, y=330, width=180, height=180)

        tra_b1_1 = Button(bg_img, command=self.train_pannels, text="Data Train", cursor="hand2",
                          font=("tahoma", 15, "bold"), bg="white", fg="navyblue")
        tra_b1_1.place(x=250, y=510, width=180, height=45)

        # Data Sets   button 6
        pho_img_btn = Image.open(r"C:\Users\chintu\OneDrive\Desktop\student\Python_Test_Projects\Images_GUI\db.jpg")
        pho_img_btn = pho_img_btn.resize((180, 180), Image.Resampling.LANCZOS)
        self.pho_img1 = ImageTk.PhotoImage(pho_img_btn)

        pho_b1 = Button(bg_img, command=self.open_img, image=self.pho_img1, cursor="hand2", )
        pho_b1.place(x=480, y=330, width=180, height=180)

        pho_b1_1 = Button(bg_img, command=self.open_img, text="Data Sets", cursor="hand2",
                          font=("tahoma", 15, "bold"), bg="white", fg="navyblue")
        pho_b1_1.place(x=480, y=510, width=180, height=45)

        # Developers   button 7
        dev_img_btn = Image.open(r"C:\Users\chintu\OneDrive\Desktop\student\Python_Test_Projects\Images_GUI\dev.jpg")
        dev_img_btn = dev_img_btn.resize((180, 180), Image.Resampling.LANCZOS)
        self.dev_img1 = ImageTk.PhotoImage(dev_img_btn)

        dev_b1 = Button(bg_img, command=self.developr, image=self.dev_img1, cursor="hand2", )
        dev_b1.place(x=710, y=330, width=180, height=180)

        dev_b1_1 = Button(bg_img, command=self.developr, text="Developers", cursor="hand2",
                          font=("tahoma", 15, "bold"), bg="white", fg="navyblue")
        dev_b1_1.place(x=710, y=510, width=180, height=45)

        # exit   button 8
        exi_img_btn = Image.open(r"C:\Users\chintu\OneDrive\Desktop\student\Python_Test_Projects\Images_GUI\exi.jpg")
        exi_img_btn = exi_img_btn.resize((180, 180), Image.Resampling.LANCZOS)
        self.exi_img1 = ImageTk.PhotoImage(exi_img_btn)

        exi_b1 = Button(bg_img, command=self.Close, image=self.exi_img1, cursor="hand2", )
        exi_b1.place(x=940, y=330, width=180, height=180)

        exi_b1_1 = Button(bg_img, command=self.Close, text="Exit", cursor="hand2", font=("tahoma", 15, "bold"),
                          bg="white", fg="navyblue")
        exi_b1_1.place(x=940, y=510, width=180, height=45)

    # ==================Funtion for Open Images Folder==================
    def open_img(self):
        os.startfile(r"C:\Users\chintu\OneDrive\Desktop\student\Python_Test_Projects\data_img")

    # ==================Functions Buttons=====================
    def student_pannels(self):
        self.new_window = Toplevel(self.root)
        self.app = Student(self.new_window)

    def train_pannels(self):
        self.new_window = Toplevel(self.root)
        self.app = Train(self.new_window)

    def face_recog(self):
        self.new_window = Toplevel(self.root)
        self.app = Face_Recognition(self.new_window)

    def attendance_pannel(self):
        self.new_window = Toplevel(self.root)
        self.app = Attendance(self.new_window)

    def developr(self):
        self.new_window = Toplevel(self.root)
        self.app = Developer(self.new_window)

    def helpSupport(self):
        self.new_window = Toplevel(self.root)
        self.app = Helpsupport(self.new_window)

    def Close(self):
        self.root.destroy() # Changed from root.destroy() to self.root.destroy()

class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("1366x768+0+0")

        # variables
        self.var_ssq = StringVar()
        self.var_sa = StringVar()
        self.var_pwd = StringVar()
        self.email_for_reset = "" # To store the email during password reset flow

        # Associate StringVar with Entry widgets for easier management
        self.var_username = StringVar()
        self.var_password = StringVar()

        self.bg = ImageTk.PhotoImage(file=r"C:\Users\chintu\OneDrive\Desktop\student\Python_Test_Projects\Images_GUI\loginBg1.jpg")

        lb1_bg = Label(self.root, image=self.bg)
        lb1_bg.place(x=0, y=0, relwidth=1, relheight=1)

        frame1 = Frame(self.root, bg="#002B53")
        frame1.place(x=560, y=170, width=340, height=450)

        img1 = Image.open(r"C:\Users\chintu\OneDrive\Desktop\student\Python_Test_Projects\Images_GUI\log1.png")
        img1 = img1.resize((100, 100), Image.Resampling.LANCZOS)
        self.photoimage1 = ImageTk.PhotoImage(img1)
        lb1img1 = Label(image=self.photoimage1, bg="#002B53")
        lb1img1.place(x=690, y=175, width=100, height=100)

        get_str = Label(frame1, text="Login", font=("times new roman", 20, "bold"), fg="white", bg="#002B53")
        get_str.place(x=140, y=100)

        # label1
        username = lb1 = Label(frame1, text="Email ID", font=("times new roman", 15, "bold"), fg="white", bg="#002B53")
        username.place(x=30, y=160)

        # entry1
        self.txtuser = ttk.Entry(frame1, textvariable=self.var_username, font=("times new roman", 15, "bold"))
        self.txtuser.place(x=33, y=190, width=270)

        # label2
        pwd = lb1 = Label(frame1, text="Password:", font=("times new roman", 15, "bold"), fg="white", bg="#002B53")
        pwd.place(x=30, y=230)

        # entry2
        self.txtpwd = ttk.Entry(frame1, textvariable=self.var_password, font=("times new roman", 15, "bold"), show="*") # Added show="*" for password
        self.txtpwd.place(x=33, y=260, width=270)

        # Creating Button Login
        loginbtn = Button(frame1, command=self.login, text="Login", font=("times new roman", 15, "bold"), bd=0,
                          relief=RIDGE, fg="#002B53", bg="white", activeforeground="white", activebackground="#007ACC")
        loginbtn.place(x=33, y=320, width=270, height=35)

        # Creating Button Registration
        reg_btn = Button(frame1, command=self.reg, text="Register", font=("times new roman", 10, "bold"), bd=0,
                         relief=RIDGE, fg="white", bg="#002B53", activeforeground="orange", activebackground="#002B53")
        reg_btn.place(x=33, y=370, width=50, height=20)

        # Creating Button Forget
        forget_btn = Button(frame1, command=self.forget_pwd, text="Forget", font=("times new roman", 10, "bold"), bd=0,
                            relief=RIDGE, fg="white", bg="#002B53", activeforeground="orange", activebackground="#002B53")
        forget_btn.place(x=90, y=370, width=50, height=20)

    # THis function is for open register window
    def reg(self):
        self.new_window = Toplevel(self.root)
        self.app = Register(self.new_window)

    def login(self):
        username = self.var_username.get()
        password = self.var_password.get()

        if not username or not password: # More concise check for empty fields
            messagebox.showerror("Error", "All Fields Required!", parent=self.root)
            return

        if username == "admin" and password == "admin": # Admin bypass
            messagebox.showinfo("Successfully", "Welcome to Attendance Management System Using Facial Recognition", parent=self.root)
            self.new_window = Toplevel(self.root)
            self.app = Face_Recognition_System(self.new_window)
            return

        conn = None # Initialize conn to None
        try:
            conn = mysql.connector.connect(username='root', password='Micky@1404sai', host='localhost', database='face_recognition', port=3306)
            mycursor = conn.cursor()
            mycursor.execute("SELECT pwd FROM regteach WHERE email=%s", (username,)) # Only fetch the password hash

            row = mycursor.fetchone()

            if row is None:
                messagebox.showerror("Error", "Invalid Username or Password!", parent=self.root)
            else:
                stored_hashed_password = row[0]
                # Verify the password using bcrypt
                if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
                    open_min = messagebox.askyesno("Confirm", "Access only Admin", parent=self.root)
                    if open_min > 0:
                        self.new_window = Toplevel(self.root)
                        self.app = Face_Recognition_System(self.new_window)
                    # No else here, if open_min is false, nothing happens and the login window remains.
                else:
                    messagebox.showerror("Error", "Invalid Username or Password!", parent=self.root)

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Login failed due to database error: {err}", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"An unexpected error occurred: {ex}", parent=self.root)
        finally:
            if conn and conn.is_connected():
                conn.close()

    # =======================Reset Password Function=============================
    def reset_pass(self):
        if self.var_ssq.get() == "Select":
            messagebox.showerror("Error", "Select the Security Question!", parent=self.root2)
        elif not self.var_sa.get():
            messagebox.showerror("Error", "Please Enter the Answer!", parent=self.root2)
        elif not self.var_pwd.get():
            messagebox.showerror("Error", "Please Enter the New Password!", parent=self.root2)
        else:
            conn = None # Initialize conn to None
            try:
                conn = mysql.connector.connect(username='root', password='Micky@1404sai', host='localhost', database='face_recognition', port=3306)
                mycursor = conn.cursor()
                # Use the stored email for reset, not the one from the main login field
                query = ("SELECT * FROM regteach WHERE email=%s AND security_question=%s AND security_answer=%s")
                value = (self.email_for_reset, self.var_ssq.get(), self.var_sa.get())
                mycursor.execute(query, value)
                row = mycursor.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Please Enter the Correct Security Answer!", parent=self.root2)
                else:
                    new_password_plain = self.var_pwd.get()
                    # Hash the new password before updating
                    new_hashed_password = bcrypt.hashpw(new_password_plain.encode('utf-8'), bcrypt.gensalt())

                    # Use your correct password column name (e.g., 'pwd' or 'user_password')
                    query = ("UPDATE regteach SET pwd=%s WHERE email=%s")
                    value = (new_hashed_password, self.email_for_reset)
                    mycursor.execute(query, value)

                    conn.commit()
                    messagebox.showinfo("Info", "Successfully! Your password has been reset. Please login with your new Password.", parent=self.root2)
                    self.root2.destroy() # Close the reset password window
                    self.var_username.set("") # Clear username field in main login
                    self.var_password.set("") # Clear password field in main login

            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Password reset failed due to database error: {err}", parent=self.root2)
            except Exception as ex:
                messagebox.showerror("Error", f"An unexpected error occurred: {ex}", parent=self.root2)
            finally:
                if conn and conn.is_connected():
                    conn.close()

    # =====================Forget Password Window Function=====================
    def forget_pwd(self):
        if not self.var_username.get():
            messagebox.showerror("Error", "Please Enter the Email ID to reset Password!", parent=self.root)
            return

        conn = None # Initialize conn to None
        try:
            conn = mysql.connector.connect(username='root', password='Micky@1404sai', host='localhost', database='face_recognition', port=3306)
            mycursor = conn.cursor()
            query = ("SELECT * FROM regteach WHERE email=%s")
            value = (self.var_username.get(),)
            mycursor.execute(query, value)
            row = mycursor.fetchone()

            if row is None:
                messagebox.showerror("Error", "Please Enter a Valid Email ID!", parent=self.root)
            else:
                self.email_for_reset = self.var_username.get() # Store the validated email

                self.root2 = Toplevel(self.root) # Make it a child of self.root
                self.root2.title("Forget Password")
                self.root2.geometry("400x400+610+170")
                self.root2.transient(self.root) # Make it modal to the parent window
                self.root2.grab_set() # Grab focus, so main window cannot be interacted with

                l = Label(self.root2, text="Forget Password", font=("times new roman", 30, "bold"), fg="#002B53", bg="#fff")
                l.place(x=0, y=10, relwidth=1)
                # -------------------fields-------------------
                # label1
                ssq = Label(self.root2, text="Select Security Question:", font=("times new roman", 15, "bold"), fg="#002B53",
                            bg="#F2F2F2")
                ssq.place(x=70, y=80)

                # Combo Box1
                self.combo_security = ttk.Combobox(self.root2, textvariable=self.var_ssq,
                                                   font=("times new roman", 15, "bold"), state="readonly")
                self.combo_security["values"] = ("Select", "Your Date of Birth", "Your Nick Name", "Your Favorite Book")
                self.combo_security.current(0)
                self.combo_security.place(x=70, y=110, width=270)

                # label2
                sa = Label(self.root2, text="Security Answer:", font=("times new roman", 15, "bold"), fg="#002B53", bg="#F2F2F2")
                sa.place(x=70, y=150)

                # entry2 for Security Answer (renamed for clarity)
                self.txt_security_answer_entry = ttk.Entry(self.root2, textvariable=self.var_sa,
                                                           font=("times new roman", 15, "bold"))
                self.txt_security_answer_entry.place(x=70, y=180, width=270)

                # label2
                new_pwd_label = Label(self.root2, text="New Password:", font=("times new roman", 15, "bold"),
                                      fg="#002B53", bg="#F2F2F2")
                new_pwd_label.place(x=70, y=220)

                # entry2 for New Password (renamed for clarity and uses show="*")
                self.new_pwd_entry = ttk.Entry(self.root2, textvariable=self.var_pwd,
                                               font=("times new roman", 15, "bold"), show="*")
                self.new_pwd_entry.place(x=70, y=250, width=270)

                # Creating Button New Password
                reset_btn = Button(self.root2, command=self.reset_pass, text="Reset Password",
                                   font=("times new roman", 15, "bold"), bd=0, relief=RIDGE, fg="#fff", bg="#002B53",
                                   activeforeground="white", activebackground="#007ACC")
                reset_btn.place(x=70, y=300, width=270, height=35)
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to connect to database: {err}", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"An unexpected error occurred: {ex}", parent=self.root)
        finally:
            if conn and conn.is_connected():
                conn.close()


if __name__ == "__main__":
    root = Tk()
    app = Login(root)
    root.mainloop()