import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, messagebox
import time

sort_by=None

def browse_directory():
    directory = filedialog.askdirectory()
    if directory:
        directory_label.config(text=directory)
        list_files(directory)

def list_files(directory):
    file_listbox.delete(0, tk.END)
    if not os.listdir(directory):
        messagebox.showerror("Empty", "The selected directory is empty.")
        return
    files = os.listdir(directory)
    file_info = [
        (filename,
        os.path.getsize(os.path.join(directory, filename)),
        os.path.getmtime(os.path.join(directory, filename)))
        for filename in files
    ]
    if sort_by == 'name':
        file_info.sort(key=lambda x: x[0].lower())
    elif sort_by == 'size':
        file_info.sort(key=lambda x: x[1])
    elif sort_by == 'date':
        file_info.sort(key=lambda x: x[2], reverse=True)
    for filename, size, mtime in file_info:
        display_txt = f"{filename} - {size} bytes - {time.ctime(mtime)}"
        file_listbox.insert(tk.END, display_txt)
        
def set_sorting(criterion):
    global sort_by
    sort_by=criterion
    directory=directory_label.cget("text")
    if os.path.isdir(directory):
        list_files(directory)
    else:
        messagebox.showwarning("No Directory Selected","Please select a directory first.")           
   
def open_file():
    file_path=filedialog.askopenfilename()
    if file_path:
        messagebox.showinfo("Selected file", f"You selected: {file_path}") 

def search_file():
    query = search_entry.get()
    directory = directory_label.cget("text")
    if os.path.isdir(directory):
        matching_files=[f for f in os.listdir(directory) if query.lower() in f.lower()]
        if matching_files:
            file_listbox.delete(0,tk.END)
            for file in matching_files:
                file_listbox.insert(tk.END, file)
        else:
            messagebox.showinfo("No Match", "No matching files found.")
    else:
        messagebox.showwarning("No Directory Selected", "Please select a directory first.")

def delete_file():
    selected=file_listbox.curselection()
    if selected:
        filename = file_listbox.get(selected[0]).split(" - ")[0]
        directory = directory_label.cget("text")
        filepath = os.path.join(directory, filename)
        
        confirm = messagebox.askyesno("Delete", f"Are you sure you want to delete {filename}?")
        if confirm:
            try:
                os.remove(filepath)
                messagebox.showinfo("Deleted", f"{filename} has been deleted.")
                list_files(directory)
            except Exception as e:
                messagebox.showerror("Error", f"Could not delete file: {e}")
    else:
        messagebox.showwarning("No File Selected", "Please select a file to delete.")

def rename_file():
    selected=file_listbox.curselection()
    if selected:
        filename = file_listbox.get(selected[0]).split(" - ")[0]
        directory = directory_label.cget("text")
        filepath = os.path.join(directory, filename)
        new_name = filedialog.asksaveasfilename(initialdir=directory, initialfile=filename, title="Rename file")
        if new_name:
            try:
                os.rename(filepath, new_name)
                messagebox.showinfo("Renamed", f"{filename} has been renamed to {os.path.basename(new_name)}.")
                list_files(directory)
            except Exception as e:
                messagebox.showerror("Error", f"Could not rename file: {e}")
    else:
        messagebox.showwarning("No File Selected", "Please select a file to rename.")

    
root = tk.Tk()
root.title("File Explorer")
root.geometry("600x500")

style=ttk.Style()
style.theme_use('clam')


browse_button = tk.Button(root, text="Browse Directory", command=browse_directory, bg="#008CBA", fg="white")
browse_button.pack(pady=10)

directory_label = tk.Label(root, text="No directory selected", wraplength=400)
directory_label.pack(pady=5)

file_frame = ttk.Frame(root)
file_frame.pack(pady=10, fill=tk.BOTH, expand=True)


file_listbox = tk.Listbox(file_frame, height=15, width=70)
file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(file_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
file_listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=file_listbox.yview)

sort_frame = tk.Frame(root)
sort_frame.pack(pady=5)

sortname_button = tk.Button(sort_frame, text="Sort by name", command=lambda: set_sorting('name'), bg="#008CBA", fg="white")
sortname_button.pack(side=tk.LEFT, padx=5)

sortsize_button = tk.Button(sort_frame, text="Sort by size", command=lambda: set_sorting('size'), bg="#008CBA", fg="white")
sortsize_button.pack(side=tk.LEFT, padx=5)

sortdate_button = tk.Button(sort_frame, text="Sort by date", command=lambda: set_sorting('date'), bg="#008CBA", fg="white")
sortdate_button.pack(side=tk.LEFT, padx=5)

action_frame = tk.Frame(root)
action_frame.pack(pady=5)

openfile_button = tk.Button(action_frame, text="Open File", command=open_file, bg="#008CBA", fg="white")
openfile_button.pack(side=tk.LEFT, padx=5)

delete_button = tk.Button(action_frame, text="Delete File", command=delete_file, bg="#008CBA", fg="white")
delete_button.pack(side=tk.LEFT, padx=5)

rename_button = tk.Button(action_frame, text="Rename File", command=rename_file, bg="#008CBA", fg="white")
rename_button.pack(side=tk.LEFT, padx=5)

search_frame = tk.Frame(root)
search_frame.pack(pady=5)

search_label = tk.Label(search_frame, text="Search Files:")
search_label.pack(side=tk.LEFT, padx=5)

search_entry = tk.Entry(search_frame)
search_entry.pack(side=tk.LEFT, padx=5)

search_button = tk.Button(search_frame, text="Search", command=search_file, bg="#008CBA", fg="white")
search_button.pack(side=tk.LEFT, pady=5)

status_bar = ttk.Label(root, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

root.mainloop()