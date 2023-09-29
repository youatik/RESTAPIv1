import tkinter as tk
from tkinter import simpledialog, messagebox

def greet():
    # Ask for the user's name
    name = simpledialog.askstring("Input", "What is your name?")

    # Show a greeting message
    if name:
        messagebox.showinfo("Hello", f"Hello {name}!")

# Create the main window
root = tk.Tk()
root.title("Name Greeting")

# Set the dimensions and make it non-resizable
root.geometry("300x150")  # You can adjust "300x150" to your preferred dimensions
root.resizable(False, False)

# Configure backgrounds to be grey
root.configure(bg="grey")
btn_greet = tk.Button(root, text="Enter Your Name", command=greet, bg="grey")
btn_greet.pack(pady=20)

root.mainloop()
