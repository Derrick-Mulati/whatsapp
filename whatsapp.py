import tkinter as tk
import customtkinter as ctk  # Correct import for customtkinter
import pywhatkit

def send_whatsapp_message(phone_number, message, hours, minutes, result_label):
    pywhatkit.sendwhatmsg(phone_number, message, hours, minutes)
    result_label.config(text="Message sent successfully!")

def create_label(parent, text, row, column, padx, pady, sticky=tk.W):
    label = ctk.CTkLabel(parent, text=text)  # Use CTkLabel
    label.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky)
    return label

def create_entry(parent, row, column, padx, pady):
    entry = ctk.CTkEntry(parent)  # Use CTkEntry
    entry.grid(row=row, column=column, padx=padx, pady=pady)
    return entry

def create_button(parent, text, command, row, column, columnspan, padx, pady):
    button = ctk.CTkButton(parent, text=text, command=command)  # Use CTkButton
    button.grid(row=row, column=column, columnspan=columnspan, padx=padx, pady=pady)
    return button

def main():
    ctk.set_appearance_mode("dark")  # Options: "light", "dark"
    ctk.set_default_color_theme("blue")  # Other options: "green", "dark-blue"

    root = ctk.CTk()  # Use CTk() to create the main window
    root.title("WhatsApp Message Scheduler")
    
    phone_label = create_label(root, "Phone Number:", 0, 0, 10, 5)
    phone_entry = create_entry(root, 0, 1, 10, 5)

    message_label = create_label(root, "Message:", 1, 0, 10, 5)
    message_entry = create_entry(root, 1, 1, 10, 5)

    time_label = create_label(root, "Send at (HH:MM):", 2, 0, 10, 5)
    hours_entry = create_entry(root, 2, 1, 10, 5)
    minutes_entry = create_entry(root, 2, 2, 10, 5)

    result_label = create_label(root, "", 4, 0, 10, 5, tk.W)

    def on_send_button_click():
        phone_number = phone_entry.get()
        message = message_entry.get()
        hours = int(hours_entry.get())
        minutes = int(minutes_entry.get())
        send_whatsapp_message(phone_number, message, hours, minutes, result_label)

    send_button = create_button(root, "Send Message", on_send_button_click, 3, 0, 2, 10, 10)

    root.mainloop()

if __name__ == "__main__":
    main()
