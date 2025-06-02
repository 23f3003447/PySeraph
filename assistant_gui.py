import customtkinter as ctk
import threading
import builtins
import random
from assistant import speak, listen, execute_command

ctk.set_appearance_mode("dark") 

class AssistantApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("PySeraph Assistant")
        self.geometry("600x400")
        self.resizable(False, False)

        welcome_messages = [
            "Oh great, you're back. Let's do this.",
            "Wow, you again? Fine, I'm ready.",
            "I've been doing absolutely nothing... just waiting for you.",
            "Sure, I'm just a voice assistant with infinite patience. Let's go.",
            "Speak now, or forever wonder what I could’ve done for you.",
            "Yes, I'm listening. Shocking, I know.",
            "Oh joy, another session of voice commands. Can't wait.",
            "Please, interrupt my zero thoughts with your human brilliance.",
            "Ready to help — because clearly you can't do it alone.",
            "You talk, I listen. This is the highlight of my circuits.",
            "If enthusiasm could be downloaded, I’d still pretend to care."
        ]

        selected_message = random.choice(welcome_messages)
        speak(selected_message)

        self.label = ctk.CTkLabel(self, text=selected_message, font=("Arial", 20), wraplength=550, justify="center")
        self.label.pack(pady=20)

        self.output_textbox = ctk.CTkTextbox(self, width=500, height=200)
        self.output_textbox.pack(pady=10)
        self.output_textbox.insert("end", f"[System] {selected_message}\n")

        self.listen_button = ctk.CTkButton(self, text="Start Listening", command=self.start_listening)
        self.listen_button.pack(pady=10)

        self.exit_button = ctk.CTkButton(self, text="Exit", command=self.quit)
        self.exit_button.pack(pady=10)

        self.listening = True

    def start_listening(self):
        self.output_textbox.insert("end", "[System] Listening...\n")
        self.output_textbox.see("end")
        self.listening = True
        threading.Thread(target=self.listen_loop, daemon=True).start()

    def display_output(self, label, text):
        self.output_textbox.insert("end", f"[{label}] {text}\n")
        self.output_textbox.see("end")

    def gui_input(self, prompt):
        input_window = ctk.CTkToplevel(self)
        input_window.title("Input Required")
        input_window.geometry("400x150")
        input_window.grab_set()

        label = ctk.CTkLabel(input_window, text=prompt)
        label.pack(pady=10)

        entry = ctk.CTkEntry(input_window, width=300)
        entry.pack(pady=5)

        result = {"value": None}

        def submit():
            result["value"] = entry.get()
            input_window.destroy()

        button = ctk.CTkButton(input_window, text="Submit", command=submit)
        button.pack(pady=10)

        input_window.wait_window()
        return result["value"]

    def listen_loop(self):
        speak("I'm listening.")
        while self.listening:
            command = listen()
            if command:
                self.display_output("You", command)
                try:
                    original_speak = speak
                    original_print = print
                    original_input = input

                    def gui_speak(text):
                        original_speak(text)
                        self.display_output("Assistant", text)

                    def gui_print(*args, **kwargs):
                        original_print(*args, **kwargs)
                        self.display_output("Console", " ".join(str(a) for a in args))

                    def gui_input_wrapper(prompt=""):
                        self.display_output("Prompt", prompt)
                        return self.gui_input(prompt)

                    builtins.print = gui_print
                    builtins.input = gui_input_wrapper
                    globals()['speak'] = gui_speak

                    if "exit" in command or "quit" in command:
                        gui_speak("Goodbye! Have a great day.")
                        self.destroy()
                        return

                    execute_command(command)

                    builtins.print = original_print
                    builtins.input = original_input
                    globals()['speak'] = original_speak

                except Exception as e:
                    self.display_output("Error", str(e))

if __name__ == "__main__":
    app = AssistantApp()
    app.mainloop()
