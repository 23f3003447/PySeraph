import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import subprocess
import requests
import os
import shutil
import json
from pptx import Presentation
from fpdf import FPDF
from email.message import EmailMessage
import smtplib

# Initialize Text-to-Speech engine
engine = pyttsx3.init()

# DeepSeek API Configuration
DEEPSEEK_API_KEY = "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"

# Function to interact with DeepSeek AI
def ai_chat(query):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek/deepseek-v3-base:free",
        "messages": [{"role": "user", "content": query}]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        try:
            return response.json()["choices"][0]["message"]["content"]
        except KeyError:
            return "Error: Unexpected API response format."
    else:
        return f"Error: {response.status_code} - {response.text}"


# Function to send email securely
def send_email(recipient, subject, body):
    sender_email = os.getenv("EMAIL_USER")
    sender_password = os.getenv("EMAIL_PASS")

    if not sender_email or not sender_password:
        speak("Email credentials are missing!")
        return

    msg = EmailMessage()
    msg['From'] = sender_email
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.set_content(body)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        speak("Email has been sent successfully.")
    except Exception as e:
        speak(f"Failed to send email: {e}")


# Function to generate PowerPoint presentations
def create_ppt():
    prs = Presentation()
    slide_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    subtitle = slide.placeholders[1]

    title.text = "Automated PPT"
    subtitle.text = "Created by PySeraph AI Assistant"

    prs.save("Generated_Presentation.pptx")
    speak("PowerPoint presentation created successfully.")


# Function to generate PDF
def create_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Automated PDF", ln=True, align='C')

    pdf.output("Generated_Document.pdf")
    speak("PDF file created successfully.")


# Speech Functions
def speak(text):
    engine.say(text)
    engine.runAndWait()


def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=10)
            command = recognizer.recognize_google(audio).lower()
            print(f"User said: {command}")
            return command
        except sr.WaitTimeoutError:
            speak("I didn't hear anything. Please try again.")
            return None
        except sr.UnknownValueError:
            speak("Sorry, I couldn't understand.")
            return None
        except sr.RequestError:
            speak("Error connecting to speech recognition service.")
            return None


def execute_command(command):
    if not command:
        return

    if "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {current_time}")

    elif "search" in command:
        search_query = command.replace("search", "").strip()
        url = f"https://www.google.com/search?q={search_query}"
        speak(f"Searching for {search_query}")
        webbrowser.open(url)

    elif "chat" in command:
        query = command.replace("chat", "").strip()
        response = ai_chat(query)
        print(f"AI Response: {response}")  # Displays response as text
        speak(response)  # Speaks the response


    elif "send email" in command:
        recipient = input("Enter recipient email: ")
        subject = input("Enter subject: ")
        body = input("Enter message: ")
        send_email(recipient, subject, body)

    elif "create ppt" in command:
        create_ppt()

    elif "create pdf" in command:
        create_pdf()

    elif "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube.")

    elif "open instagram" in command:
        webbrowser.open("https://www.instagram.com")
        speak("Opening Instagram.")

    elif "exit" in command or "quit" in command:
        speak("Goodbye! Have a great day.")
        exit()

    else:
        speak("I'm sorry, I don't understand that command.")


if __name__ == "__main__":
    speak("Hello! PySeraph here. How can I help you?")
    while True:
        command = listen()
        if command:
            execute_command(command)
