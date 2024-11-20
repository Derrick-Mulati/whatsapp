import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
import pywhatkit
import pandas as pd
import datetime

class WhatsAppSchedulerApp:
    def __init__(self, root):
        self.contacts = {}
        self.scheduled_messages = []

        # Configure root
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        root.title("WhatsApp Scheduler")
        root.geometry("600x500")
        root.resizable(False, False)

        # Layout: Header, Body, Footer
        self.create_header(root)
        self.create_body(root)
        self.create_footer(root)

    def create_header(self, root):
        header_frame = ctk.CTkFrame(root)
        header_frame.pack(fill="x", padx=10, pady=5)

        title_label = ctk.CTkLabel(header_frame, text="WhatsApp Scheduler", font=("Arial", 18, "bold"))
        title_label.pack()

    def create_body(self, root):
        body_frame = ctk.CTkFrame(root)
        body_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Left Panel: Contacts
        self.create_contacts_section(body_frame)

        # Right Panel: Message and Time
        self.create_message_section(body_frame)

    def create_contacts_section(self, parent):
        contacts_frame = ctk.CTkFrame(parent, width=250)
        contacts_frame.pack(side="left", fill="y", padx=5, pady=5)

        ctk.CTkLabel(contacts_frame, text="Contacts", font=("Arial", 14, "bold")).pack(pady=5)

        self.contacts_listbox = tk.Listbox(contacts_frame, height=15, bg="#2e2e2e", fg="white", font=("Arial", 12))
        self.contacts_listbox.pack(fill="both", expand=True, padx=5, pady=5)

        load_button = ctk.CTkButton(contacts_frame, text="Load Contacts", command=self.load_contacts)
        load_button.pack(pady=5)

    def create_message_section(self, parent):
        message_frame = ctk.CTkFrame(parent)
        message_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        # Message Input
        ctk.CTkLabel(message_frame, text="Message", font=("Arial", 14, "bold")).pack(pady=5)
        self.message_entry = ctk.CTkTextbox(message_frame, height=100)
        self.message_entry.pack(fill="x", padx=5, pady=5)

        # Time Selection
        ctk.CTkLabel(message_frame, text="Schedule Time", font=("Arial", 14, "bold")).pack(pady=5)
        time_frame = tk.Frame(message_frame)
        time_frame.pack(pady=5)

        self.hours_spinbox = tk.Spinbox(time_frame, from_=0, to=23, width=3, font=("Arial", 12), format="%02.0f")
        self.hours_spinbox.grid(row=0, column=0, padx=2)
        tk.Label(time_frame, text=":", font=("Arial", 12)).grid(row=0, column=1)
        self.minutes_spinbox = tk.Spinbox(time_frame, from_=0, to=59, width=3, font=("Arial", 12), format="%02.0f")
        self.minutes_spinbox.grid(row=0, column=2, padx=2)

        # Schedule Button
        schedule_button = ctk.CTkButton(message_frame, text="Schedule Message", command=self.schedule_message)
        schedule_button.pack(pady=10)

        # Live Preview
        ctk.CTkLabel(message_frame, text="Scheduled Messages", font=("Arial", 14, "bold")).pack(pady=5)
        self.scheduled_listbox = tk.Listbox(message_frame, height=8, bg="#2e2e2e", fg="white", font=("Arial", 12))
        self.scheduled_listbox.pack(fill="both", expand=True, padx=5, pady=5)

    def create_footer(self, root):
        footer_frame = ctk.CTkFrame(root)
        footer_frame.pack(fill="x", padx=10, pady=5)

        send_all_button = ctk.CTkButton(footer_frame, text="Send All Scheduled Messages", command=self.send_all_messages)
        send_all_button.pack(pady=5)

    def load_contacts(self):
        """Load contacts from a CSV file."""
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                df = pd.read_csv(file_path)
                if 'Name' in df.columns and 'Phone' in df.columns:
                    df['Phone'] = df['Phone'].apply(self.format_phone_number)
                    self.contacts = dict(zip(df['Name'], df['Phone']))
                    self.contacts_listbox.delete(0, tk.END)
                    for name in self.contacts:
                        self.contacts_listbox.insert(tk.END, name)
                    messagebox.showinfo("Success", "Contacts loaded successfully!")
                else:
                    raise ValueError("CSV must contain 'Name' and 'Phone' columns.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load contacts: {e}")

    def format_phone_number(self, number):
        """Format phone numbers to international format."""
        number = number.strip()
        if number.startswith("2"):
            return f"+{number}"
        elif number.startswith("7") or number.startswith("0"):
            return f"+254{number[1:]}"
        return number

    def schedule_message(self):
        """Schedule a message to send."""
        selected_contact = self.contacts_listbox.get(tk.ACTIVE)
        message = self.message_entry.get("1.0", "end").strip()
        hours = int(self.hours_spinbox.get())
        minutes = int(self.minutes_spinbox.get())

        if not selected_contact or not message:
            messagebox.showwarning("Warning", "Please select a contact and write a message.")
            return

        if not self.is_future_time(hours, minutes):
            messagebox.showwarning("Warning", "Please select a future time.")
            return

        phone_number = self.contacts[selected_contact]
        self.scheduled_messages.append((selected_contact, phone_number, message, hours, minutes))
        self.scheduled_listbox.insert(tk.END, f"{selected_contact} @ {hours:02}:{minutes:02} - {message}")
        self.message_entry.delete("1.0", "end")

    def is_future_time(self, hours, minutes):
        now = datetime.datetime.now()
        scheduled_time = now.replace(hour=hours, minute=minutes, second=0, microsecond=0)
        return scheduled_time > now

    def send_all_messages(self):
        """Send all scheduled messages."""
        for contact, phone, message, hours, minutes in self.scheduled_messages:
            try:
                pywhatkit.sendwhatmsg(phone, message, hours, minutes)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to send message to {contact}: {e}")

        self.scheduled_listbox.delete(0, tk.END)
        self.scheduled_messages.clear()
        messagebox.showinfo("Success", "All messages sent!")

def main():
    root = ctk.CTk()
    app = WhatsAppSchedulerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
