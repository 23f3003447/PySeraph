import os
import smtplib
import random
import mysql.connector
import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import messagebox

conn = mysql.connector.connect(
    host="localhost",
    user="root",  
    password="Avmn#4561",  
    database="user_auth"
)
cursor = conn.cursor()

# Generate OTP
otp = str(random.randint(100000, 999999))

def send_otp():
    global otp
    email = entry_email.get()
    sender_email = "pyseraphai@gmail.com"
    sender_password = "tpmp qotf wevy onih"  

    message = f"Subject: Your OTP Code\n\nYour OTP is {otp}. It expires in 5 minutes."

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, message)
        server.quit()
        messagebox.showinfo("OTP Sent", f"OTP sent to {email}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send OTP: {str(e)}")

def verify_otp():
    if entry_otp.get() == otp:
        username = entry_username.get()
        email = entry_email.get()
        password = entry_password.get()
        
        try:
            cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
            conn.commit()
            messagebox.showinfo("Success", "Registration Successful! Redirecting to login...")
            root.destroy()  
            os.system("python \"D:\\Frontend\\PySeraph\\PySeraph\\assistant.py\"") 
        except Exception as e:
            messagebox.showerror("Error", f"Database error: {str(e)}")
    else:
        messagebox.showerror("Error", "Invalid OTP")

ctk.set_appearance_mode("dark")

# Registration UI
root = ctk.CTk()
root.title("Registration Page")
root.geometry("500x400")

script_dir = os.path.dirname(os.path.abspath(__file__))
bg_path = os.path.join(script_dir, "bg.jpg")
bg_image = Image.open(bg_path)
width, height = root.winfo_screenwidth(), root.winfo_screenheight()
bg_image = bg_image.resize((width, height))
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = ctk.CTkLabel(root, image=bg_photo, text="")
bg_label.place(relwidth=1, relheight=1)

entry_username = ctk.CTkEntry(root, width=250, fg_color="transparent", border_color="white", border_width=2, placeholder_text="Username")
entry_username.place(relx=0.5, rely=0.3, anchor="center")

entry_email = ctk.CTkEntry(root, width=250, fg_color="transparent", border_color="white", border_width=2, placeholder_text="Email")
entry_email.place(relx=0.5, rely=0.4, anchor="center")

entry_password = ctk.CTkEntry(root, width=250, fg_color="transparent", border_color="white", border_width=2, show="*", placeholder_text="Password")
entry_password.place(relx=0.5, rely=0.5, anchor="center")

entry_otp = ctk.CTkEntry(root, width=150, fg_color="transparent", border_color="white", border_width=2, placeholder_text="Enter OTP")
entry_otp.place(relx=0.5, rely=0.6, anchor="center")

send_otp_button = ctk.CTkButton(root, text="Send OTP", fg_color="gray", text_color="white", command=send_otp)
send_otp_button.place(relx=0.3, rely=0.7, anchor="center")

verify_button = ctk.CTkButton(root, text="Verify & Register", fg_color="blue", text_color="white", command=verify_otp)
verify_button.place(relx=0.7, rely=0.7, anchor="center")

root.attributes('-alpha', 0.98)
root.mainloop()
