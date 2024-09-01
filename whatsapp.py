import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk  # Correct import for customtkinter
import pywhatkit
import pandas as pd

# Initialize an empty dictionary for contacts
contacts = {}

def format_phone_number(number):
    """Formats phone numbers based on specific rules."""
    number = number.strip()  # Remove any leading or trailing whitespace
    if number.startswith("2"):
        return f"+{number}"
    elif number.startswith("7"):
        return f"+254{number[1:]}"  # Replace the leading 7 with +254
    elif number.startswith("0"):
        return f"+254{number[1:]}"  # Replace the leading 0 with +254
    else:
        return number

def load_contacts_from_csv():
    """Load contacts from a CSV file and update the dropdown menu."""
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        try:
            # Load the CSV file into a pandas DataFrame
            df = pd.read_csv(file_path)
            
            # Ensure the CSV has the correct columns: 'Name' and 'Phone'
            if 'Name' in df.columns and 'Phone' in df.columns:
                # Format and update the contacts dictionary
                global contacts
                contacts = {name: format_phone_number(phone) for name, phone in zip(df['Name'], df['Phone'])}
                
                # Update the dropdown menu
                contact_menu['values'] = list(contacts.keys())
                if contacts:
                    selected_contact.set(next(iter(contacts)))  # Reset to first contact

                messagebox.showinfo("Success", "Contacts loaded successfully!")
            else:
                messagebox.showerror("Error", "CSV file must have 'Name' and 'Phone' columns.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load contacts: {str(e)}")

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

    # Configure grid weights to center elements
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(2, weight=1)
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)
    root.grid_rowconfigure(2, weight=1)
    root.grid_rowconfigure(3, weight=1)
    root.grid_rowconfigure(4, weight=1)

    # Load Contacts Button
    load_contacts_button = create_button(root, "Load Contacts", load_contacts_from_csv, 0, 0, 3, 10, 10)
    load_contacts_button.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

    contact_label = create_label(root, "Select Contact:", 1, 0, 10, 5)
    contact_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")

    # Dropdown menu to select a contact
    global selected_contact, contact_menu
    selected_contact = tk.StringVar(root)
    selected_contact.set("Select a contact")  # Default value before loading contacts
    contact_menu = ctk.CTkOptionMenu(root, variable=selected_contact, values=[])
    contact_menu.grid(row=1, column=1, columnspan=2, padx=10, pady=5, sticky="ew")

    message_label = create_label(root, "Message:", 2, 0, 10, 5)
    message_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
    
    message_entry = ctk.CTkEntry(root, font=("Helvetica", 14), width=300, height=100)  # Increased size and font
    message_entry.grid(row=2, column=1, columnspan=2, padx=10, pady=10, sticky="ew")

    time_label = create_label(root, "Send at (HH:MM):", 3, 0, 10, 5)
    time_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
    
    # Frame for the time selection (clock interface)
    time_frame = tk.Frame(root)
    time_frame.grid(row=3, column=1, columnspan=2, padx=10, pady=5, sticky="ew")

    # Set the default time to 07:00 using Spinboxes
    hours_spinbox = create_spinbox(time_frame, 0, 23, 0, 0, 5, 5, "07")
    tk.Label(time_frame, text=":", font=("Helvetica", 12)).grid(row=0, column=1)
    minutes_spinbox = create_spinbox(time_frame, 0, 59, 0, 2, 5, 5, "00")

    result_label = create_label(root, "", 4, 0, 10, 5, tk.W)
    result_label.grid(row=4, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

    def on_send_button_click():
        contact_name = selected_contact.get()
        phone_number = contacts.get(contact_name, None)
        if phone_number:
            message = message_entry.get()
            hours = int(hours_spinbox.get())
            minutes = int(minutes_spinbox.get())
            send_whatsapp_message(phone_number, message, hours, minutes, result_label)
        else:
            result_label.config(text="Please select a contact.")

    send_button = create_button(root, "Send Message", on_send_button_click, 4, 0, 3, 10, 10)
    send_button.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

    root.mainloop()

if __name__ == "__main__":
    main()
