import os
import shutil
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, ttk, messagebox



def get_file_type(file_path):
    file_extension = file_path.suffix.lower()
    file_type = None

    if file_extension in ['.jpg', '.jpeg', '.png', '.gif']:
        file_type = 'Images'
    elif file_extension in ['.mp4', '.mkv', '.ts']:
        file_type = 'Videos'
    # Add more file types and categories as needed
    else:
        print("Sorry!! unknown file extention.")
    return file_type


def rename_file(file_path, category):
    file_name = file_path.stem
    file_extension = file_path.suffix

    # Replace dots between words in the file name with spaces
    file_name = file_name.replace(".", " ")
    file_name = file_name.replace("  ", " ")

    new_file_name = f"{file_name}{file_extension}"
    new_file_path = file_path.with_name(new_file_name)
    os.rename(file_path, new_file_path)
    return new_file_path



def organize_file(file_path, category):
    category_folder = file_path.parent / category
    


def process_directory(directory_path, progress_bar=None):
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



def select_directory():
    global selected_directory
    selected_directory.set(filedialog.askdirectory())

def process_selected_directory():
    directory_path = selected_directory.get()
    if directory_path:
        progress_bar["value"] = 0
        progress_bar.update()
        try:
            process_directory(Path(directory_path), progress_bar)
            messagebox.showinfo("Done", "✅ All files have been processed successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"❌ An error occurred:\n\n{str(e)}")


def create_gui():
    global selected_directory, progress_bar
    root = tk.Tk()
    root.title("File Organizer")

    frame = tk.Frame(root, padx=30, pady=40)
    frame.pack()

    selected_directory = tk.StringVar()

    select_button = tk.Button(frame, text="Select Directory", command=select_directory)
    select_button.pack(pady=(0, 10))

    directory_label = tk.Label(frame, textvariable=selected_directory)
    directory_label.pack(pady=(0, 10))

    start_button = tk.Button(frame, text="Start", command=process_selected_directory)
    start_button.pack(pady=(0, 10))

    progress_bar = ttk.Progressbar(frame, orient="horizontal", length=200, mode="determinate")
    progress_bar.pack()

    root.mainloop()



if __name__ == "__main__":
    create_gui()

