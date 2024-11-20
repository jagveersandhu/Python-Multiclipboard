import os
import shelve
import tkinter as tk
from tkinter import messagebox

# Define the fixed directory for the shelve file
shelve_directory = r"D:\Python Projects\multiclipboard\clipboard"
os.makedirs(shelve_directory, exist_ok=True)  # Ensure the directory exists
shelve_path = os.path.join(shelve_directory, 'mcb')

def save_content():
    """Save the heading and content to the shelf."""
    heading = entry_heading.get()
    content = text_content.get("1.0", tk.END).strip()

    if not heading:
        messagebox.showerror("Error", "Heading cannot be empty.")
        return

    if not content:
        messagebox.showerror("Error", "Content cannot be empty.")
        return

    with shelve.open(shelve_path) as mcb_shelf:
        mcb_shelf[heading] = content  # Save content under the heading

    update_keyword_list()
    messagebox.showinfo("Success", f"Content added under the heading '{heading}'.")

def load_content(event=None):
    """Load content for the selected heading."""
    selected = listbox_headings.get(tk.ACTIVE)
    if not selected:
        return  # Do nothing if no heading is selected

    with shelve.open(shelve_path) as mcb_shelf:
        if selected in mcb_shelf:
            entry_heading.delete(0, tk.END)
            entry_heading.insert(0, selected)  # Display the heading
            text_content.delete("1.0", tk.END)
            text_content.insert(tk.END, mcb_shelf[selected])  # Display the content
        else:
            messagebox.showerror("Error", f"No content found for heading '{selected}'.")

def delete_heading():
    """Delete the selected heading and its content."""
    selected = listbox_headings.get(tk.ACTIVE)
    if not selected:
        messagebox.showerror("Error", "No heading selected.")
        return

    with shelve.open(shelve_path) as mcb_shelf:
        if selected in mcb_shelf:
            del mcb_shelf[selected]
            update_keyword_list()
            messagebox.showinfo("Success", f"Deleted heading '{selected}'.")
        else:
            messagebox.showerror("Error", f"No content found for heading '{selected}'.")

def update_keyword_list():
    """Update the listbox with current headings."""
    with shelve.open(shelve_path) as mcb_shelf:
        headings = list(mcb_shelf.keys())
    listbox_headings.delete(0, tk.END)
    for heading in headings:
        listbox_headings.insert(tk.END, heading)

# Create the main Tkinter window
root = tk.Tk()
root.title("Multi-Clipboard Manager")
root.geometry("600x400")

# Heading input and content text area
frame_input = tk.Frame(root)
frame_input.pack(pady=10, fill=tk.X)

tk.Label(frame_input, text="Heading:").pack(side=tk.LEFT, padx=5)
entry_heading = tk.Entry(frame_input, width=40)
entry_heading.pack(side=tk.LEFT, padx=5)

frame_text = tk.Frame(root)
frame_text.pack(pady=10, fill=tk.BOTH, expand=True)

tk.Label(frame_text, text="Content:").pack(anchor=tk.W, padx=5)
text_content = tk.Text(frame_text, height=8, wrap=tk.WORD)
text_content.pack(fill=tk.BOTH, expand=True, padx=5)

# Action buttons
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)
btn_save = tk.Button(frame_buttons, text="Save", command=save_content)
btn_save.pack(side=tk.LEFT, padx=5)
btn_delete = tk.Button(frame_buttons, text="Delete", command=delete_heading)
btn_delete.pack(side=tk.LEFT, padx=5)

# Listbox for headings
frame_listbox = tk.Frame(root)
frame_listbox.pack(pady=10, fill=tk.BOTH, expand=True)

listbox_headings = tk.Listbox(frame_listbox, height=5)
listbox_headings.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
scrollbar = tk.Scrollbar(frame_listbox, orient=tk.VERTICAL, command=listbox_headings.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox_headings.config(yscrollcommand=scrollbar.set)

# Bind listbox selection to load_content function
listbox_headings.bind("<<ListboxSelect>>", load_content)

# Populate the heading list
update_keyword_list()

# Run the application
root.mainloop()
