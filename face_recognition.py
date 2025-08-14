import re
import os
from sys import path
from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector
import cv2
import numpy as np
from time import strftime
from datetime import datetime

class Face_Recognition:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1366x768+0+0")
        self.root.title("Face Recognition Panel")

        # --- Image loading for GUI ---
        # Header image
        try:
            img = Image.open(r"C:\Users\chintu\OneDrive\Desktop\student\Python_Test_Projects\Images_GUI\banner.jpg")
            img = img.resize((1366, 130), Image.Resampling.LANCZOS)
            self.photoimg = ImageTk.PhotoImage(img)
            f_lb1 = Label(self.root, image=self.photoimg)
            f_lb1.place(x=0, y=0, width=1366, height=130)
        except FileNotFoundError:
            messagebox.showerror("Image Error", "Banner image not found. Check path: C:\\Users\\chintu\\OneDrive\\Desktop\\student\\Python_Test_Projects\\Images_GUI\\banner.jpg")
            exit() # Exit if crucial images are missing

        # Background image
        try:
            bg1 = Image.open(r"C:\Users\chintu\OneDrive\Desktop\student\Python_Test_Projects\Images_GUI\bg2.jpg")
            bg1 = bg1.resize((1366, 768), Image.Resampling.LANCZOS)
            self.photobg1 = ImageTk.PhotoImage(bg1)
            bg_img = Label(self.root, image=self.photobg1)
            bg_img.place(x=0, y=130, width=1366, height=768)
        except FileNotFoundError:
            messagebox.showerror("Image Error", "Background image not found. Check path: C:\\Users\\chintu\\OneDrive\\Desktop\\student\\Python_Test_Projects\\Images_GUI\\bg2.jpg")
            exit()

        # Title section
        title_lb1 = Label(bg_img, text="Welcome to Face Recognition Panel", font=("verdana", 30, "bold"), bg="white", fg="navyblue")
        title_lb1.place(x=0, y=0, width=1366, height=45)

        # Face Detector button
        try:
            std_img_btn = Image.open(r"C:\Users\chintu\OneDrive\Desktop\student\Python_Test_Projects\Images_GUI\f_det.jpg")
            std_img_btn = std_img_btn.resize((180, 180), Image.Resampling.LANCZOS)
            self.std_img1 = ImageTk.PhotoImage(std_img_btn)
            std_b1 = Button(bg_img, command=self.face_recog, image=self.std_img1, cursor="hand2")
            std_b1.place(x=600, y=170, width=180, height=180)
            std_b1_1 = Button(bg_img, command=self.face_recog, text="Face Detector", cursor="hand2", font=("tahoma", 15, "bold"), bg="white", fg="navyblue")
            std_b1_1.place(x=600, y=350, width=180, height=45)
        except FileNotFoundError:
            messagebox.showerror("Image Error", "Face Detector button image not found. Check path: C:\\Users\\chintu\\OneDrive\\Desktop\\student\\Python_Test_Projects\\Images_GUI\\f_det.jpg")
            # The button might not appear, but the app can still run for debugging

    # ===================== Attendance ===================
    def ensure_attendance_file_exists(file_path):
        """
        Checks if the attendance.csv file exists at the given path.
        If it doesn't exist, it creates an empty file.
        """ 
        # Check if the file exists
        if not os.path.exists(file_path):
            try:
                # Create the file in write mode ('w').
                # If the file doesn't exist, it will be created.
                # If it exists, its content will be truncated (emptied).
                # We use 'with' to ensure the file is properly closed even if errors occur.
                with open(file_path, 'w') as f:
                    # Optionally, you can write a header to the CSV file here
                    # For example: f.write("ID,Name,Roll,Timestamp\n")
                    print(f"File '{file_path}' did not exist and was created.")
            except IOError as e:
                # Handle potential errors during file creation (e.g., permission issues)
                print(f"Error creating file '{file_path}': {e}")
        else:
            print(f"File '{file_path}' already exists.")

    # Define the full path to your attendance.csv file
    # Make sure this path exactly matches the one in your error message
    attendance_file_path = 'C:\\Users\\chintu\\OneDrive\\Desktop\\student\\Python_Test_Projects\\attendance.csv'

    # Call the function to ensure the file exists
    ensure_attendance_file_exists(attendance_file_path)

    # You can add your existing attendance logging logic here now,
    # as you can be sure the file exists.
    print("\nProceeding with attendance logging...")

    def mark_attendance(self, student_id, roll_no, name):
        """Marks attendance once per hour in attendance.csv."""
        try:
            file_path = "C:\\Users\\chintu\\OneDrive\\Desktop\\student\\Python_Test_Projects\\attendance.csv"
            student_id_str = str(student_id).strip()
            roll_no_str = str(roll_no).strip()
            name_str = str(name).strip()

            if not student_id_str:
                print("Invalid Student ID. Attendance not marked.")
                return

            now = datetime.now()
            current_date = now.strftime("%d%m/%Y")
            current_hour = now.strftime("%H")  # Only the hour part
            already_marked = False

            # Read existing entries
            with open(file_path, "r", newline="\n") as f:
                for line in f:
                    entry = line.strip().split(",")
                    if len(entry) >= 5:
                        existing_id = entry[0].strip()
                        time_str = entry[3].strip()
                        date_str = entry[4].strip()

                        # Extract hour from time
                        recorded_hour = time_str.split(":")[0]

                        if (existing_id == student_id_str and
                            date_str == current_date and
                            recorded_hour == current_hour):
                            already_marked = True
                            break

            if not already_marked:
                time_str = now.strftime("%H:%M:%S")
                with open(file_path, "a", newline="\n") as f:
                    f.write(f"{student_id_str},{roll_no_str},{name_str},{time_str},{current_date},Present\n")
                print(f"✅ Attendance marked for {name_str} (ID: {student_id_str}) at {time_str}")
            else:
                print(f"⏱️ Attendance already marked for {name_str} (ID: {student_id_str}) in this hour.")

        except Exception as e:
            print(f"❌ Failed to store attendance: {e}")


    # ==================== Face Recognition ==================
    def face_recog(self):
        def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text, clf_model):
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            features = classifier.detectMultiScale(gray_image, scaleFactor, minNeighbors)

            all_coords = [] # To store all detected face coordinates if needed later

            if len(features) == 0:
                cv2.putText(img, "No Face Detected", (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 255), 2)
                return all_coords # Return empty list if no faces

            for (x, y, w, h) in features:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3) # Green box for detected face
                id_predicted, confidence_raw = clf_model.predict(gray_image[y:y+h, x:x+w])

                confidence = int(100 * (1 - confidence_raw / 300)) # Convert raw confidence to percentage

                Name = "Unknown"
                Roll = "Unknown"
                Student_ID_from_DB = "Unknown" # Renamed to avoid confusion with predicted 'id_predicted'

                conn = None
                cursor = None
                try:
                    conn = mysql.connector.connect(
                        username='root',
                        password='Micky@1404sai',
                        host='localhost',
                        database='face_recognition',
                        port=3306
                    )
                    cursor = conn.cursor()

                    # *** CRUCIAL FIX: Querying by Student_id ***
                    # Use the predicted 'id_predicted' (e.g., 5) to look up the student in the database
                    print(f"Attempting to query DB for Face_ID: {id_predicted} (Confidence: {confidence_raw:.2f})")

                    sql_query = "SELECT Name, Roll, Student_ID FROM student WHERE Face_ID= %s"
                    cursor.execute(sql_query, (id_predicted,)) # Pass the integer ID directly
                    result = cursor.fetchone() # Fetches one row as a tuple (Name, Roll, Student_ID)

                    if result:
                        Name = result[0]
                        Roll = result[1]
                        Student_ID_from_DB = result[2]
                        print(f"Retrieved - ID: {Student_ID_from_DB}, Name: {Name}, Roll: {Roll}")
                    else:
                        print(f"No record found in DB for Face_ID: {id_predicted}")

                except mysql.connector.Error as err:
                    print(f"Database Error: {err}")
                    messagebox.showerror("Database Error", f"Failed to connect or query database: {err}")
                    Name = "DB Error"
                    Roll = "DB Error"
                    Student_ID_from_DB = "DB Error"
                finally:
                    if cursor:
                        cursor.close()
                    if conn:
                        conn.close()

                if confidence > 77 : # Adjustable confidence threshold
                    cv2.putText(img, f"Student_ID: {Student_ID_from_DB}", (x, y - 80), cv2.FONT_HERSHEY_COMPLEX, 0.8, (64, 15, 223), 2)
                    cv2.putText(img, f"Name: {Name}", (x, y - 55), cv2.FONT_HERSHEY_COMPLEX, 0.8, (64, 15, 223), 2)
                    cv2.putText(img, f"Roll-No: {Roll}", (x, y - 30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (64, 15, 223), 2)
                    
                    # Mark attendance only if data was successfully retrieved (not "Unknown" or "DB Error")
                    if Name != "Unknown" and Name != "DB Error" and Student_ID_from_DB != "Unknown" and Student_ID_from_DB != "DB Error":
                        self.mark_attendance(Student_ID_from_DB, Roll, Name)
                else:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3) # Red box for unknown
                    cv2.putText(img, "Unknown Face", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 0), 3)

                all_coords.append([x, y, w, h])

            return all_coords # Return the list of all detected face coordinates

        def recognize_and_display(img_frame, clf_model, faceCascade_classifier):
            # The 'coord_list' returned here will be a list of lists (all_coords)
            coord_list = draw_boundary(img_frame, faceCascade_classifier, 1.1, 10, (255, 25, 255), "Face", clf_model)
            return img_frame

        # Load Haar Cascade Classifier
        faceCascade_path = r"C:\Users\chintu\OneDrive\Desktop\student\Python_Test_Projects\haarcascade_frontalface_default.xml"
        if not os.path.exists(faceCascade_path):
            messagebox.showerror("Error", f"Haar Cascade XML not found: {faceCascade_path}\nPlease ensure it exists.")
            return

        faceCascade = cv2.CascadeClassifier(faceCascade_path)
        clf = cv2.face.LBPHFaceRecognizer_create()

        # Load Trained Model (clf.xml)
        clf_model_path = r"C:\Users\chintu\OneDrive\Desktop\student\Python_Test_Projects\clf.xml"
        if not os.path.exists(clf_model_path):
            messagebox.showerror("Error", "Trained model (clf.xml) not found. Please train the model first.")
            return # Exit the face_recog function if model is missing

        try:
            clf.read(clf_model_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load trained model (clf.xml): {e}\nPlease ensure the model is valid and trained.")
            return

        # Open Webcam
        videoCap = cv2.VideoCapture(0)
        if not videoCap.isOpened():
            messagebox.showerror("Error", "Could not open webcam. Please check if camera is connected and not in use.")
            return

        # Main loop for real-time recognition
        while True:
            ret, img = videoCap.read()
            if not ret:
                print("Failed to grab frame from webcam. Exiting...")
                break # Exit loop if frame cannot be read

            img = recognize_and_display(img, clf, faceCascade)
            cv2.imshow("Face Detector", img)

            if cv2.waitKey(1) == 13: # 13 is the Enter key
                break
        
        videoCap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognition(root)
    root.mainloop()