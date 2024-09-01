import tkinter as tk
import customtkinter as ctk  # Correct import for customtkinter
import pywhatkit

# Predefined list of contacts
contacts = {
    "Alice": "+1234567890",
    "Bob": "+0987654321",
    "Charlie": "+1122334455"
}

def send_whatsapp_message(phone_number, message, hours, minutes, result_label):
    pywhatkit.sendwhatmsg(phone_number, message, hours, minutes)
    result_label.config(text="Message sent successfully!")

def create_label(parent, text, row, column, padx, pady, sticky=tk.W):
    label = ctk.CTkLabel(parent, text=text)  # Use CTkLabel
    label.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky)
    return label

def create_spinbox(parent, from_, to, row, column, padx, pady, default_value):
    spinbox = tk.Spinbox(parent, from_=from_, to=to, width=3, font=("Helvetica", 12), format="%02.0f")
    spinbox.grid(row=row, column=column, padx=padx, pady=pady)
    spinbox.delete(0, tk.END)  # Clear the default value
    spinbox.insert(0, default_value)  # Set the default value
    return spinbox

def create_button(parent, text, command, row, column, columnspan, padx, pady):
    button = ctk.CTkButton(parent, text=text, command=command)  # Use CTkButton
    button.grid(row=row, column=column, columnspan=columnspan, padx=padx, pady=pady)
    return button

def main():
    ctk.set_appearance_mode("dark")  # Options: "light", "dark"
    ctk.set_default_color_theme("blue")  # Other options: "green", "dark-blue"

    root = ctk.CTk()  # Use CTk() to create the main window
    root.title("WhatsApp Message Scheduler")
    
    contact_label = create_label(root, "Select Contact:", 0, 0, 10, 5)

    # Dropdown menu to select a contact
    selected_contact = tk.StringVar(root)
    selected_contact.set(next(iter(contacts)))  # Set default contact
    contact_menu = ctk.CTkOptionMenu(root, variable=selected_contact, values=list(contacts.keys()))
    contact_menu.grid(row=0, column=1, columnspan=2, padx=10, pady=5)

    message_label = create_label(root, "Message:", 1, 0, 10, 5)
    message_entry = ctk.CTkEntry(root, font=("Helvetica", 14), width=300, height=100)  # Increased size and font
    message_entry.grid(row=1, column=1, columnspan=2, padx=10, pady=10)

    time_label = create_label(root, "Send at (HH:MM):", 2, 0, 10, 5)
    
    # Frame for the time selection (clock interface)
    time_frame = tk.Frame(root)
    time_frame.grid(row=2, column=1, columnspan=2, padx=10, pady=5, sticky="w")

    # Set the default time to 07:00 using Spinboxes
    hours_spinbox = create_spinbox(time_frame, 0, 23, 0, 0, 5, 5, "07")
    tk.Label(time_frame, text=":", font=("Helvetica", 12)).grid(row=0, column=1)
    minutes_spinbox = create_spinbox(time_frame, 0, 59, 0, 2, 5, 5, "00")

    result_label = create_label(root, "", 4, 0, 10, 5, tk.W)

    def on_send_button_click():
        contact_name = selected_contact.get()
        phone_number = contacts[contact_name]
        message = message_entry.get()
        hours = int(hours_spinbox.get())
        minutes = int(minutes_spinbox.get())
        send_whatsapp_message(phone_number, message, hours, minutes, result_label)

    send_button = create_button(root, "Send Message", on_send_button_click, 3, 0, 3, 10, 10)

    root.mainloop()

if __name__ == "__main__":
    main()
