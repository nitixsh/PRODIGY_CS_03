import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import string
import re
import random
import math

# Function to assess the password strength and return feedback, score, and color
def assess_password(password):
    length = len(password)
    contains_lower = any(c.islower() for c in password)
    contains_upper = any(c.isupper() for c in password)
    contains_digits = any(c.isdigit() for c in password)
    contains_symbols = any(c in string.punctuation for c in password)
    
    # Character set size
    charset_size = 0
    if contains_lower:
        charset_size += 26  # Lowercase a-z
    if contains_upper:
        charset_size += 26  # Uppercase A-Z
    if contains_digits:
        charset_size += 10  # Digits 0-9
    if contains_symbols:
        charset_size += len(string.punctuation)  # Punctuation symbols

    # Calculate entropy
    if charset_size > 0:
        entropy = length * math.log2(charset_size)
    else:
        entropy = 0

    # Estimate time to crack (in seconds)
    guesses_per_second = 1e9  # 1 billion guesses per second
    if entropy > 0:
        time_to_crack_seconds = 2**entropy / guesses_per_second
    else:
        time_to_crack_seconds = 0

    # Convert time to more readable format
    if time_to_crack_seconds < 1:
        time_to_crack = "Less than a second"
    elif time_to_crack_seconds < 60:
        time_to_crack = f"{int(time_to_crack_seconds)} seconds"
    elif time_to_crack_seconds < 3600:
        time_to_crack = f"{int(time_to_crack_seconds // 60)} minutes"
    elif time_to_crack_seconds < 86400:
        time_to_crack = f"{int(time_to_crack_seconds // 3600)} hours"
    elif time_to_crack_seconds < 31536000:
        time_to_crack = f"{int(time_to_crack_seconds // 86400)} days"
    elif time_to_crack_seconds < 3153600000:
        time_to_crack = f"{int(time_to_crack_seconds // 31536000)} years"
    else:
        time_to_crack = f"{int(time_to_crack_seconds // 31536000)} centuries"

    # Password strength feedback based on entropy
    if entropy < 28:
        feedback = "Very Weak"
        color = "danger"
    elif entropy < 36:
        feedback = "Weak"
        color = "warning"
    elif entropy < 60:
        feedback = "Medium"
        color = "info"
    elif entropy < 128:
        feedback = "Strong"
        color = "success"
    else:
        feedback = "Very Strong"
        color = "success"
    
    return feedback, color, time_to_crack

# Function to update the feedback and progress bar in real-time
def update_feedback(*args):
    password = password_entry.get()
    feedback, color, time_to_crack = assess_password(password)

    feedback_label.config(text=feedback, bootstyle=color)
    time_label.config(text=f"Estimated time to crack: {time_to_crack}")

    # Update character type indicators
    lower_case_var.set(bool(re.search(r'[a-z]', password)))
    upper_case_var.set(bool(re.search(r'[A-Z]', password)))
    numbers_var.set(bool(re.search(r'\d', password)))
    symbols_var.set(bool(re.search(r'\W', password)))

# Function to generate a random strong password
def generate_password():
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(12))
    password_entry.delete(0, END)
    password_entry.insert(0, password)
    update_feedback()

# Create the main window with ttkbootstrap theme
root = ttk.Window(themename="darkly")
root.title("Task-03 Password Complexity Checker")

# Main Frame (centered content)
main_frame = ttk.Frame(root, padding="30")
main_frame.grid(row=0, column=0, sticky="")

# Center the main frame in the window
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Define custom style for Checkbuttons
style = ttk.Style()
style.configure('Custom.TCheckbutton', font=("Arial", 14))

# Tip Label
tip_label = ttk.Label(main_frame, text="Tip: Use a combination of uppercase, lowercase, numbers, and symbols.", font=("Arial", 16))
tip_label.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="w")

# Password Entry
password_entry = ttk.Entry(main_frame, show="*", font=("Arial", 18), width=35)
password_entry.grid(row=1, column=0, padx=15, pady=15)
password_entry.bind("<KeyRelease>", update_feedback)

# Show Password Checkbox
show_password_var = ttk.BooleanVar()
show_password_check = ttk.Checkbutton(main_frame, text="Show password", variable=show_password_var, command=lambda: password_entry.config(show='' if show_password_var.get() else '*'), style='Custom.TCheckbutton')
show_password_check.grid(row=1, column=1, padx=15)

# Password Generator Button
generate_button = ttk.Button(main_frame, text="Generate Password", bootstyle="primary", command=generate_password, style="success.TButton")
generate_button.grid(row=2, column=1, padx=15, pady=10)

# Password Strength Feedback Label
feedback_label = ttk.Label(main_frame, text="No Password", font=("Arial", 18))
feedback_label.grid(row=2, column=0, columnspan=2, pady=(15, 10))

# Character type indicators frame
char_types_frame = ttk.Frame(main_frame)
char_types_frame.grid(row=4, column=0, columnspan=2, pady=(15, 15))

lower_case_var = ttk.BooleanVar()
lower_case_check = ttk.Checkbutton(char_types_frame, text="Lower case", variable=lower_case_var, state="disabled", style='Custom.TCheckbutton')
lower_case_check.grid(row=0, column=0, padx=10)

upper_case_var = ttk.BooleanVar()
upper_case_check = ttk.Checkbutton(char_types_frame, text="Upper case", variable=upper_case_var, state="disabled", style='Custom.TCheckbutton')
upper_case_check.grid(row=0, column=1, padx=10)

numbers_var = ttk.BooleanVar()
numbers_check = ttk.Checkbutton(char_types_frame, text="Numbers", variable=numbers_var, state="disabled", style='Custom.TCheckbutton')
numbers_check.grid(row=0, column=2, padx=10)

symbols_var = ttk.BooleanVar()
symbols_check = ttk.Checkbutton(char_types_frame, text="Symbols", variable=symbols_var, state="disabled", style='Custom.TCheckbutton')
symbols_check.grid(row=0, column=3, padx=10)

# Time to crack label
time_label = ttk.Label(main_frame, text="Estimated time to crack: 0 seconds", font=("Arial", 16))
time_label.grid(row=5, column=0, columnspan=2, pady=15)

# Start the GUI event loop
root.mainloop()