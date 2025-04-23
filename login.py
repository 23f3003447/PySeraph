import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
import os

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
            root.destroy()  # Close login window after success
            os.system("python \"D:\\Frontend\\PySeraph\\PySeraph\\assistant.py\"") # 🔹Launch PySeraph 
        else:
            messagebox.showerror("Login Failed", "Invalid credentials!")

# Function to open registration page
def open_registration():
    root.destroy()
    os.system(f"python \"{os.path.join(script_dir, 'registration.py')}\"")

ctk.set_appearance_mode("dark")

# Create main window
root = ctk.CTk()
root.title("Login Page")
root.geometry("500x400")

# Load and set background image
# Get the directory where the script (login.py) is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Set the correct path to background.jpg
bg_path = os.path.join(script_dir, "bg.jpg")
bg_image = Image.open(bg_path)  # Make sure you have this image in the same folder
width, height = root.winfo_screenwidth(), root.winfo_screenheight()
bg_image = bg_image.resize((width, height))

bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = ctk.CTkLabel(root, image=bg_photo, text="")
bg_label.place(relwidth=1, relheight=1)  # Stretch image to full window

entry_username = ctk.CTkEntry(root, 
                              width=250, 
                              fg_color="transparent",  # Remove background color
                              border_color="white",   # Add border for visibility
                              border_width=2, 
                              placeholder_text="Username")  # Use placeholder text
entry_username.place(relx=0.5, rely=0.4, anchor="center")  # Adjust position

entry_password = ctk.CTkEntry(root, 
                              width=250, 
                              fg_color="transparent",  
                              border_color="white",  
                              border_width=2, 
                              show="*",  # Hide password input
                              placeholder_text="Password")  
entry_password.place(relx=0.5, rely=0.5, anchor="center")  # Adjust position

# 🔹 Login Button now launches assistant.py after successful login
login_button = ctk.CTkButton(root, text="Login", fg_color="blue", text_color="white", hover_color="darkblue", corner_radius=15, command=login)
login_button.place(relx=0.5, rely=0.6, anchor="center")

# Sign Up Button (Redirects to Registration Page)
signup_button = ctk.CTkButton(root, text="Sign Up", fg_color="gray", text_color="white", hover_color="black", corner_radius=15, command=open_registration)
signup_button.place(relx=0.5, rely=0.7, anchor="center")

# ✅ Step 4: Add Slight Transparency to the Window (Optional)
root.attributes('-alpha', 0.98)  # Gives a smooth UI effect

# Run application
root.mainloop()
