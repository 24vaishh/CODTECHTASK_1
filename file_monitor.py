import os
import hashlib
import json
from tkinter import filedialog, messagebox, Tk, Button, Label

HASH_DB = "hashes.json"

def calculate_hash(filepath):
    hasher = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception as e:
        return None

def load_hash_db():
    if os.path.exists(HASH_DB):
        with open(HASH_DB, "r") as f:
            return json.load(f)
    return {}

def save_hash_db(data):
    with open(HASH_DB, "w") as f:
        json.dump(data, f, indent=4)

def monitor_file():
    file_path = filedialog.askopenfilename()
    if not file_path:
        return
    
    hash_db = load_hash_db()
    current_hash = calculate_hash(file_path)

    if current_hash is None:
        messagebox.showerror("Error", f"Unable to read {file_path}")
        return

    if file_path in hash_db:
        if hash_db[file_path] == current_hash:
            messagebox.showinfo("No Change", "The file has not been modified.")
        else:
            messagebox.showwarning("Changed", "The file has been modified!")
            hash_db[file_path] = current_hash
            save_hash_db(hash_db)
    else:
        hash_db[file_path] = current_hash
        save_hash_db(hash_db)
        messagebox.showinfo("Monitored", "File added to monitoring list.")

def reset_db():
    if os.path.exists(HASH_DB):
        os.remove(HASH_DB)
        messagebox.showinfo("Reset", "Hash database has been cleared.")
    else:
        messagebox.showinfo("No DB", "No database found to reset.")

# GUI Setup
root = Tk()
root.title("File Change Monitor")

Label(root, text="File Hash Change Detector", font=("Arial", 14)).pack(pady=10)
Button(root, text="Monitor a File", command=monitor_file, width=30).pack(pady=5)
Button(root, text="Reset Monitoring", command=reset_db, width=30).pack(pady=5)
Button(root, text="Exit", command=root.destroy, width=30).pack(pady=20)

root.geometry("350x200")
root.mainloop()
