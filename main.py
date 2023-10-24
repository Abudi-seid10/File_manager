import os
import shutil
from pathlib import Path
import hashlib
import tkinter as tk
from tkinter import filedialog, ttk, messagebox, Text, Scrollbar
import json


# Config file operations
def load_config():
    if Path('config.json').exists():
        with open('config.json', 'r') as file:
            return json.load(file)
    return {}


def save_config(config_data):
    with open('config.json', 'w') as file:
        json.dump(config_data, file)


# To compute a file's hash
def get_file_hash(filepath):
    BUF_SIZE = 65536
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha256.update(data)
    return sha256.hexdigest()

# Checks for duplicates in a directory
def check_for_duplicates(directory_path, logger=None):
    hashes = {}
    duplicates = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            filepath = os.path.join(root, file)
            filehash = get_file_hash(filepath)
            if filehash in hashes:
                duplicates.append((filepath, hashes[filehash]))
            else:
                hashes[filehash] = filepath
    for dup in duplicates:
        if logger:
            logger(f"Duplicate: {dup[0]} | Original: {dup[1]}")
    return duplicates


# Maintaining a history of actions for undo functionality
action_history = []

def undo_last_action():
    if action_history:
        last_action = action_history.pop()
        if last_action["type"] == "rename":
            os.rename(last_action["to"], last_action["from"])
        elif last_action["type"] == "move":
            shutil.move(last_action["from"], last_action["to"])



# Getting the file type using the config file if available
config = load_config()
DEFAULT_FILE_TYPES = {
    '.jpg': 'Images',
    '.jpeg': 'Images',
    '.png': 'Images',
    '.gif': 'Images',
    '.mp4': 'Videos',
    '.mkv': 'Videos',
    '.ts': 'Videos',
    '.pdf': 'Documents',
    '.doc': 'Documents',
    '.docx': 'Documents'
}


def get_file_type(file_path):
    file_extension = file_path.suffix.lower()
    return config.get(file_extension, DEFAULT_FILE_TYPES.get(file_extension, None))





def rename_file(file_path, category, dry_run=False):
    try:
        file_name = file_path.stem
        file_extension = file_path.suffix
        file_name = file_name.replace(".", " ")
        file_name = file_name.replace("  ", " ")
        new_file_name = f"{file_name}{file_extension}"
        new_file_path = file_path.with_name(new_file_name)
        if not dry_run:
            os.rename(file_path, new_file_path)
            action_history.append({
                "type": "rename",
                "from": new_file_path,
                "to": file_path
            })
        return new_file_path
    except Exception as e:
        print(f"Error renaming {file_path}. Error: {e}")
        return file_path




def organize_file(file_path, category, dry_run=False, custom_actions=None):
    try:
        if category == 'Videos':
            parent_folder = file_path.parent
            video_name = file_path.stem

            # Extract series name and season
            parts = video_name.split(' ')
            series_name = ' '.join(parts[:-1])
            season = parts[-1][:3]  # Taking only the first 3 characters like "S01"

            new_folder_name = f"{series_name} {season}"
            # If the new folder name isn't in the parent folder name, rename parent folder
            if new_folder_name not in parent_folder.name:
                new_parent_folder = parent_folder.parent / new_folder_name
                if not dry_run:
                    parent_folder.rename(new_parent_folder)
                    action_history.append({
                        "type": "rename",
                        "from": new_parent_folder,
                        "to": parent_folder
                    })

            if custom_actions and category in custom_actions:
                action = custom_actions[category]
                # Execute custom action, could be a script or command
        else:
            category_folder = file_path.parent / category
            category_folder.mkdir(exist_ok=True)
            if not dry_run:
                shutil.move(file_path, category_folder / file_path.name)
                action_history.append({
                    "type": "move",
                    "from": category_folder / file_path.name,
                    "to": file_path
                })
    except Exception as e:
        print(f"Error organizing {file_path}. Error: {e}")
    


def process_directory(directory_path, progress_bar=None, recursive=True, logger=None):
    file_count = 0
    for root, dirs, files in os.walk(directory_path):
        file_count += len(files)

    processed_files = 0

    for root, dirs, files in os.walk(directory_path):
        for entry in files:
            file_path = Path(root) / entry
            file_type = get_file_type(file_path)
            if file_type:
                new_file_path = rename_file(file_path, file_type)
                organize_file(new_file_path, file_type)

            processed_files += 1
            if progress_bar:
                progress_bar["value"] = (processed_files / file_count) * 100
                progress_bar.update()
    if logger:
        logger(f"Processed: {file_path}")
    new_file_path = rename_file(file_path, file_type, dry_run=dry_run)
    organize_file(new_file_path, file_type, dry_run=dry_run)


class FileOrganizerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("File Organizer")

        self.selected_directory = tk.StringVar()
        self.recursive = tk.BooleanVar(value=True)

        self.directories_used = config.get("directories", [])

        self.create_gui()

    def create_gui(self):
        # Initialize the dry_run_mode variable first
        self.dry_run_mode = tk.BooleanVar(value=False)
        
        frame = tk.Frame(self.root, padx=30, pady=20)
        frame.pack()

        select_button = tk.Button(frame, text="Select Directory", command=self.select_directory)
        select_button.grid(row=0, column=0, pady=(0, 10), padx=10)

        self.directory_combo = ttk.Combobox(frame, textvariable=self.selected_directory, values=self.directories_used)
        self.directory_combo.grid(row=0, column=1, pady=(0, 10), padx=10)

        start_button = tk.Button(frame, text="Start", command=self.process_selected_directory)
        start_button.grid(row=1, column=0, columnspan=2, pady=(0, 10), padx=10)

        recursive_check = ttk.Checkbutton(frame, text="Recursive", variable=self.recursive)
        recursive_check.grid(row=2, column=0, columnspan=2, pady=(0, 10))

        dry_run_check = ttk.Checkbutton(frame, text="Dry Run Mode", variable=self.dry_run_mode)
        dry_run_check.grid(row=3, column=0, columnspan=2, pady=(0, 10))

        undo_button = tk.Button(frame, text="Undo", command=self.undo)
        undo_button.grid(row=6, column=0, pady=(10, 10), padx=10)

        find_duplicates_button = tk.Button(frame, text="Find Duplicates", command=self.find_duplicates)
        find_duplicates_button.grid(row=6, column=1, pady=(10, 10), padx=10)

        self.progress_bar = ttk.Progressbar(frame, orient="horizontal", length=200, mode="determinate")
        self.progress_bar.grid(row=3, column=0, columnspan=2, pady=10)

        log_label = ttk.Label(frame, text="Logs:")
        log_label.grid(row=4, column=0, columnspan=2, pady=(10, 5))

        self.log_area = Text(frame, width=50, height=10, wrap=tk.WORD)
        self.log_area.grid(row=5, column=0, columnspan=2)

        scroll = Scrollbar(frame, command=self.log_area.yview)
        self.log_area.configure(yscrollcommand=scroll.set)
        scroll.grid(row=5, column=2, sticky="ns")

        self.root.mainloop()



    def log(self, message):
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.yview(tk.END)

    def select_directory(self):
        selected = filedialog.askdirectory()
        self.selected_directory.set(selected)
        if selected and selected not in self.directories_used:
            self.directories_used.append(selected)
            self.directory_combo['values'] = self.directories_used
            save_config({"directories": self.directories_used})

    def process_selected_directory(self):
        directory_path = self.selected_directory.get()
        if directory_path:
            self.progress_bar["value"] = 0
            self.progress_bar.update()
            try:
                process_directory(Path(directory_path), self.progress_bar, self.recursive.get(), self.log)
                messagebox.showinfo("Done", "✅ All files have been processed successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"❌ An error occurred:\n\n{str(e)}")
        if not self.dry_run_mode.get():
            check_for_duplicates(directory_path, self.log)

    def undo(self):
        try:
            undo_last_action()
            self.log("Undid the last action.")
        except Exception as e:
            self.log(f"Error: {str(e)}")

    def find_duplicates(self):
        directory_path = self.selected_directory.get()
        if directory_path:
            self.log("Checking for duplicates...")
            check_for_duplicates(directory_path, self.log)
            self.log("Done checking for duplicates.")
        else:
            self.log("Please select a directory first.")

if __name__ == "__main__":
    app = FileOrganizerGUI()