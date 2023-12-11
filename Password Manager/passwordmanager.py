import tkinter as tk  # Importing Tkinter for GUI
from tkinter import messagebox  # Importing messagebox for displaying messages
from cryptography.fernet import Fernet  # Importing Fernet for encryption

# Function to generate a Fernet key
def generate_key():
    return Fernet.generate_key()

# Function to encrypt a password using the provided key
def encrypt_password(key, password):
    f = Fernet(key)
    return f.encrypt(password.encode()).decode()

# Function to decrypt an encrypted password using the provided key
def decrypt_password(key, encrypted_password):
    f = Fernet(key)
    return f.decrypt(encrypted_password.encode()).decode()

# Dictionary to store passwords (service: {username, encrypted_password})
passwords = {}

# Function to add a password to the dictionary
def add_password():
    # Retrieving input data from the GUI entries
    service = service_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    # Checking if all fields are filled
    if service and username and password:
        # Encrypting the password
        encrypted_password = encrypt_password(key, password)
        # Storing service details with username and encrypted password
        passwords[service] = {'username': username, 'password': encrypted_password}
        # Displaying success message
        messagebox.showinfo("Success", "Password added successfully!")
    else:
        # Displaying a warning if any field is empty
        messagebox.showwarning("Error", "Please fill in all the fields.")

# Function to retrieve a password for a given service
def get_password():
    # Retrieving service from the GUI entry
    service = service_entry.get()
    if service in passwords:
        # Decrypting the password using the key and displaying username and decrypted password
        encrypted_password = passwords[service]['password']
        decrypted_password = decrypt_password(key, encrypted_password)
        messagebox.showinfo("Password", f"Username: {passwords[service]['username']}\nPassword: {decrypted_password}")
    else:
        # Displaying a warning if the service is not found in passwords
        messagebox.showwarning("Error", "Password not found.")

# Generating a Fernet key
key = generate_key()

# Instructions for the user displayed in the GUI
instructions = '''To add password fill all the fields and press "Add Password"
To view password, enter Account Name and press "Get Password"'''

# Setting up the Tkinter window
window = tk.Tk()
window.title("Password Manager")
window.configure(bg="orange")  # Setting background color

window.resizable(False, False)  # Making window non-resizable

# Creating a frame for organizing widgets
center_frame = tk.Frame(window, bg="#d3d3d3")
center_frame.grid(row=0, column=0, padx=10, pady=10)

# Labels and Entry fields for service, username, and password
instruction_label = tk.Label(center_frame, text=instructions, bg="#d3d3d3")
instruction_label.grid(row=0, column=1, padx=10, pady=5)

service_label = tk.Label(center_frame, text="Account:", bg="#d3d3d3")
service_label.grid(row=1, column=0, padx=10, pady=5)
service_entry = tk.Entry(center_frame)
service_entry.grid(row=1, column=1, padx=10, pady=5)

username_label = tk.Label(center_frame, text="Username:", bg="#d3d3d3")
username_label.grid(row=2, column=0, padx=10, pady=5)
username_entry = tk.Entry(center_frame)
username_entry.grid(row=2, column=1, padx=10, pady=5)

password_label = tk.Label(center_frame, text="Password:", bg="#d3d3d3")
password_label.grid(row=3, column=0, padx=10, pady=5)
password_entry = tk.Entry(center_frame, show="*")  # Hides the password
password_entry.grid(row=3, column=1, padx=10, pady=5)

# Buttons to add and get passwords
add_button = tk.Button(center_frame, text="Add Password", command=add_password, height=1, width=10)
add_button.grid(row=5, column=4, padx=10, pady=5)

get_button = tk.Button(center_frame, text="Get Password", command=get_password, height=1, width=10)
get_button.grid(row=6, column=4, padx=10, pady=5)

# Initiating the GUI window
window.mainloop()
