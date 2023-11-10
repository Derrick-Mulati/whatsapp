import tkinter as tk
from tkinter import ttk
import pywhatkit

def send_whatsapp_message():
    phone_number = phone_entry.get()
    message = message_entry.get()
    hours = int(hours_entry.get())
    minutes = int(minutes_entry.get())
    
    pywhatkit.sendwhatmsg(phone_number, message, hours, minutes)
    result_label.config(text="Message sent successfully!")

# Create the main window
root = tk.Tk()
root.title("WhatsApp Message Scheduler")

# Create and pack labels and entry fields with improved style
phone_label = ttk.Label(root, text="Phone Number:")
phone_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
phone_entry = ttk.Entry(root)
phone_entry.grid(row=0, column=1, padx=10, pady=5)

message_label = ttk.Label(root, text="Message:")
message_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
message_entry = ttk.Entry(root)
message_entry.grid(row=1, column=1, padx=10, pady=5)

time_label = ttk.Label(root, text="Send at (HH:MM):")
time_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
hours_entry = ttk.Entry(root)
hours_entry.grid(row=2, column=1, padx=10, pady=5)
minutes_entry = ttk.Entry(root)
minutes_entry.grid(row=2, column=2, padx=10, pady=5)

# Create and pack the send button with improved style
send_button = ttk.Button(root, text="Send Message", command=send_whatsapp_message)
send_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Create and pack the result label with improved style
result_label = ttk.Label(root, text="")
result_label.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

root.mainloop()
