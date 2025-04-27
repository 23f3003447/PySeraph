import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
import os
import random
import smtplib
from email.message import EmailMessage

# Connect to MySQL database
def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Avmn#4561",
            database="user_auth"
        )
        return conn
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Failed to connect: {e}")
        return None

# Function to handle login
def login():
    username = entry_username.get()
    password = entry_password.get()
    
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            messagebox.showinfo("Login Successful", f"Welcome, {username}!")
            root.destroy()
            os.system("python \"D:\\Frontend\\PySeraph\\assistant_gui.py\"")
        else:
            messagebox.showerror("Login Failed", "Invalid credentials!")

# Function to open registration page
def open_registration():
    root.destroy()
    os.system(f"python \"{os.path.join(script_dir, 'registration.py')}\"")

# Function to handle forgot password
def forgot_password():
    otp_code = str(random.randint(100000, 999999))
    username = ""

    def send_otp(email):
        try:
            sender_email = "pyseraphai@gmail.com"
            sender_password = "tpmp qotf wevy onih"  

            msg = EmailMessage()
            msg['Subject'] = "Your OTP for Password Reset"
            msg['From'] = sender_email
            msg['To'] = email
            msg.set_content(f"Your OTP is {otp_code}")

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(sender_email, sender_password)
                server.send_message(msg)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send OTP: {str(e)}")
            return False

    def verify_otp_and_reset():
        entered_otp = entry_otp.get()
        new_password = entry_new_password.get()

        if entered_otp == otp_code:
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET password=%s WHERE username=%s", (new_password, username))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Password reset successful!")
                forgot_window.destroy()
        else:
            messagebox.showerror("Error", "Invalid OTP!")

    def find_user():
        nonlocal username
        username = entry_forgot_username.get()

        if not username:
            messagebox.showerror("Error", "Enter your username.")
            return

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT email FROM users WHERE username=%s", (username,))
            user = cursor.fetchone()
            conn.close()

            if user:
                email = user[0]
                success = send_otp(email)
                if success:
                    entry_forgot_username.pack_forget()
                    submit_username_button.pack_forget()

                    ctk.CTkLabel(forgot_window, text="Enter OTP sent to your email").pack(pady=10)
                    global entry_otp
                    entry_otp = ctk.CTkEntry(forgot_window, width=250)
                    entry_otp.pack()

                    ctk.CTkLabel(forgot_window, text="Enter New Password").pack(pady=10)
                    global entry_new_password
                    entry_new_password = ctk.CTkEntry(forgot_window, width=250, show="*")
                    entry_new_password.pack()

                    reset_button = ctk.CTkButton(forgot_window, text="Reset Password", command=verify_otp_and_reset)
                    reset_button.pack(pady=20)
            else:
                messagebox.showerror("Error", "Username not found!")

    forgot_window = ctk.CTkToplevel(root)
    forgot_window.title("Forgot Password")
    forgot_window.geometry("400x300")
    forgot_window.grab_set()

    ctk.CTkLabel(forgot_window, text="Enter your username").pack(pady=10)
    entry_forgot_username = ctk.CTkEntry(forgot_window, width=250)
    entry_forgot_username.pack()

    submit_username_button = ctk.CTkButton(forgot_window, text="Send OTP", command=find_user)
    submit_username_button.pack(pady=20)

ctk.set_appearance_mode("dark")

root = ctk.CTk()
root.title("Login Page")
root.geometry("500x400")

script_dir = os.path.dirname(os.path.abspath(__file__))

bg_path = os.path.join(script_dir, "bg.jpg")
bg_image = Image.open(bg_path)
width, height = root.winfo_screenwidth(), root.winfo_screenheight()
bg_image = bg_image.resize((width, height))

bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = ctk.CTkLabel(root, image=bg_photo, text="")
bg_label.place(relwidth=1, relheight=1)

entry_username = ctk.CTkEntry(root,
                              width=250,
                              fg_color="transparent",
                              border_color="white",
                              border_width=2,
                              placeholder_text="Username")
entry_username.place(relx=0.5, rely=0.4, anchor="center")

entry_password = ctk.CTkEntry(root,
                              width=250,
                              fg_color="transparent",
                              border_color="white",
                              border_width=2,
                              show="*",
                              placeholder_text="Password")
entry_password.place(relx=0.5, rely=0.5, anchor="center")

login_button = ctk.CTkButton(root, text="Login", fg_color="blue", text_color="white", hover_color="darkblue", corner_radius=15, command=login)
login_button.place(relx=0.5, rely=0.6, anchor="center")

signup_button = ctk.CTkButton(root, text="Sign Up", fg_color="gray", text_color="white", hover_color="black", corner_radius=15, command=open_registration)
signup_button.place(relx=0.5, rely=0.7, anchor="center")

forgot_button = ctk.CTkButton(root, text="Forgot Password?", fg_color="transparent", text_color="white", hover_color="gray", corner_radius=15, command=forgot_password)
forgot_button.place(relx=0.5, rely=0.78, anchor="center")

root.attributes('-alpha', 0.98)

root.mainloop()
