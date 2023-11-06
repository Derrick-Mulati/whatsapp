import tkinter as tk
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
root.title("WhatsApp Message Sender")

# Create and pack labels and entry fields
phone_label = tk.Label(root, text="Phone Number:")
phone_label.pack()
phone_entry = tk.Entry(root)
phone_entry.pack()

message_label = tk.Label(root, text="Message:")
message_label.pack()
message_entry = tk.Entry(root)
message_entry.pack()

time_label = tk.Label(root, text="Send at (HH:MM):")
time_label.pack()
hours_entry = tk.Entry(root)
hours_entry.pack()
minutes_entry = tk.Entry(root)
minutes_entry.pack()

# Create and pack the send button
send_button = tk.Button(root, text="Send Message", command=send_whatsapp_message)
send_button.pack()

# Create and pack the result label
result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()
