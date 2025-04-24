import customtkinter as ctk
import threading
from assistant import speak, listen, execute_command  # Ensure assistant.py is in the same folder

ctk.set_appearance_mode("dark")

class AssistantApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("PySeraph Assistant")
        self.geometry("600x400")
        self.resizable(False, False)

        self.label = ctk.CTkLabel(self, text="PySeraph is ready...", font=("Arial", 20))
        self.label.pack(pady=20)

        self.output_textbox = ctk.CTkTextbox(self, width=500, height=200)
        self.output_textbox.pack(pady=10)
        self.output_textbox.insert("end", "[System] Ready to assist you!\n")

        self.listen_button = ctk.CTkButton(self, text="Start Listening", command=self.start_listening)
        self.listen_button.pack(pady=10)

        self.exit_button = ctk.CTkButton(self, text="Exit", command=self.quit)
        self.exit_button.pack(pady=10)

    def start_listening(self):
        self.output_textbox.insert("end", "[System] Listening...\n")
        self.output_textbox.see("end")
        threading.Thread(target=self.listen_loop, daemon=True).start()

    def listen_loop(self):
        speak("I'm listening.")
        while True:
            command = listen()
            if command:
                self.output_textbox.insert("end", f"You: {command}\n")
                self.output_textbox.see("end")
                execute_command(command)

if __name__ == "__main__":
    app = AssistantApp()
    app.mainloop()
