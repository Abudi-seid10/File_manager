"""
File Organizer - A Python application for organizing files by type.

This module provides functionality to organize files in directories based on their
file extensions, with features like duplicate detection, undo functionality, and
a GUI interface built with tkinter.
"""

import os
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Callable, Any
import hashlib
import tkinter as tk
from tkinter import filedialog, ttk, messagebox, Text, Scrollbar
import json
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('file_organizer.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# Config file operations
def load_config() -> Dict[str, Any]:
    """
    Load configuration from config.json file.
    
    Returns:
        Dict[str, Any]: Configuration dictionary. Returns empty dict if file doesn't exist.
    """
    config_path = Path('config.json')
    if config_path.exists():
        try:
            with open(config_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except json.JSONDecodeError as e:
            logger.error(f"Error loading config.json: {e}")
            return {}
        except Exception as e:
            logger.error(f"Unexpected error loading config: {e}")
            return {}
    return {}


def save_config(config_data: Dict[str, Any]) -> None:
    """
    Save configuration to config.json file.
    
    Args:
        config_data: Dictionary containing configuration data to save.
    """
    try:
        with open('config.json', 'w', encoding='utf-8') as file:
            json.dump(config_data, file, indent=2)
        logger.info("Configuration saved successfully")
    except Exception as e:
        logger.error(f"Error saving config: {e}")


# To compute a file's hash
def get_file_hash(filepath: Path) -> str:
    """
    Calculate SHA256 hash of a file.
    
    Args:
        filepath: Path to the file to hash.
        
    Returns:
        str: Hexadecimal string representation of the file's SHA256 hash.
    """
    BUF_SIZE = 65536  # 64KB chunks
    sha256 = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            while True:
                data = f.read(BUF_SIZE)
                if not data:
                    break
                sha256.update(data)
        return sha256.hexdigest()
    except Exception as e:
        logger.error(f"Error hashing file {filepath}: {e}")
        return ""


# Checks for duplicates in a directory
def check_for_duplicates(
    directory_path: str, 
    logger_func: Optional[Callable[[str], None]] = None
) -> List[Tuple[str, str]]:
    """
    Find duplicate files in a directory based on file content hash.
    
    Args:
        directory_path: Path to the directory to scan for duplicates.
        logger_func: Optional callback function to log messages.
        
    Returns:
        List[Tuple[str, str]]: List of tuples containing (duplicate_path, original_path).
    """
    hashes: Dict[str, str] = {}
    duplicates: List[Tuple[str, str]] = []
    
    try:
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                filepath = os.path.join(root, file)
                filehash = get_file_hash(Path(filepath))
                
                if not filehash:  # Skip files that couldn't be hashed
                    continue
                    
                if filehash in hashes:
                    duplicates.append((filepath, hashes[filehash]))
                else:
                    hashes[filehash] = filepath
                    
        for dup in duplicates:
            message = f"Duplicate: {dup[0]} | Original: {dup[1]}"
            if logger_func:
                logger_func(message)
            logger.info(message)
            
    except Exception as e:
        error_msg = f"Error checking for duplicates: {e}"
        logger.error(error_msg)
        if logger_func:
            logger_func(error_msg)
            
    return duplicates


# Maintaining a history of actions for undo functionality
action_history: List[Dict[str, Any]] = []


def undo_last_action() -> bool:
    """
    Undo the last file operation (rename or move).
    
    Returns:
        bool: True if an action was undone, False if no actions to undo.
    """
    if not action_history:
        logger.warning("No actions to undo")
        return False
        
    try:
        last_action = action_history.pop()
        if last_action["type"] == "rename":
            # Revert: new name back to original name
            os.rename(last_action["to"], last_action["from"])
            logger.info(f"Undid rename: {last_action['to']} -> {last_action['from']}")
        elif last_action["type"] == "move":
            # Revert: new location back to original location
            shutil.move(last_action["to"], last_action["from"])
            logger.info(f"Undid move: {last_action['to']} -> {last_action['from']}")
        return True
    except Exception as e:
        logger.error(f"Error undoing action: {e}")
        return False



# Getting the file type using the config file if available
config = load_config()
DEFAULT_FILE_TYPES: Dict[str, str] = {
    '.jpg': 'Images',
    '.jpeg': 'Images',
    '.png': 'Images',
    '.gif': 'Images',
    '.bmp': 'Images',
    '.svg': 'Images',
    '.webp': 'Images',
    '.mp4': 'Videos',
    '.mkv': 'Videos',
    '.ts': 'Videos',
    '.avi': 'Videos',
    '.mov': 'Videos',
    '.wmv': 'Videos',
    '.flv': 'Videos',
    '.webm': 'Videos',
    '.pdf': 'Documents',
    '.doc': 'Documents',
    '.docx': 'Documents',
    '.txt': 'Documents',
    '.odt': 'Documents',
    '.rtf': 'Documents',
    '.xls': 'Documents',
    '.xlsx': 'Documents',
    '.ppt': 'Documents',
    '.pptx': 'Documents',
    '.mp3': 'Audio',
    '.wav': 'Audio',
    '.flac': 'Audio',
    '.aac': 'Audio',
    '.ogg': 'Audio',
    '.wma': 'Audio',
    '.m4a': 'Audio',
    '.zip': 'Archives',
    '.rar': 'Archives',
    '.7z': 'Archives',
    '.tar': 'Archives',
    '.gz': 'Archives',
    '.bz2': 'Archives',
    '.xz': 'Archives',
}


def get_file_type(file_path: Path) -> Optional[str]:
    """
    Determine the category/type of a file based on its extension.
    
    Args:
        file_path: Path object representing the file.
        
    Returns:
        Optional[str]: Category name (e.g., 'Images', 'Videos') or None if unknown.
    """
    file_extension = file_path.suffix.lower()
    # First check custom config, then fall back to defaults
    custom_types = config.get('file_types', {})
    return custom_types.get(file_extension, DEFAULT_FILE_TYPES.get(file_extension, None))




def rename_file(file_path: Path, category: str, dry_run: bool = False) -> Path:
    """
    Rename a file by replacing dots with spaces in the filename.
    
    Args:
        file_path: Path to the file to rename.
        category: Category of the file (for logging purposes).
        dry_run: If True, don't actually rename the file.
        
    Returns:
        Path: New path of the renamed file, or original path if rename failed.
    """
    try:
        file_name = file_path.stem
        file_extension = file_path.suffix
        
        # Replace dots with spaces and clean up multiple spaces
        file_name = file_name.replace(".", " ")
        file_name = file_name.replace("  ", " ").strip()
        
        new_file_name = f"{file_name}{file_extension}"
        new_file_path = file_path.with_name(new_file_name)
        
        if not dry_run and new_file_path != file_path:
            # Check if target already exists
            if new_file_path.exists():
                logger.warning(f"Target file already exists: {new_file_path}")
                return file_path
                
            os.rename(file_path, new_file_path)
            action_history.append({
                "type": "rename",
                "from": str(file_path),
                "to": str(new_file_path)
            })
            logger.info(f"Renamed: {file_path} -> {new_file_path}")
            
        return new_file_path
    except Exception as e:
        logger.error(f"Error renaming {file_path}: {e}")
        return file_path




def organize_file(
    file_path: Path, 
    category: str, 
    dry_run: bool = False, 
    custom_actions: Optional[Dict[str, Any]] = None
) -> None:
    """
    Organize a file by moving it to a category-specific folder.
    
    For videos, special handling creates folders based on series name and season.
    For other files, they are moved to a folder named after their category.
    
    Args:
        file_path: Path to the file to organize.
        category: Category of the file (e.g., 'Images', 'Videos').
        dry_run: If True, don't actually move files.
        custom_actions: Optional dictionary of custom actions per category.
    """
    try:
        if category == 'Videos':
            parent_folder = file_path.parent
            video_name = file_path.stem

            # Extract series name and season
            parts = video_name.split(' ')
            if len(parts) > 1:
                series_name = ' '.join(parts[:-1])
                season = parts[-1][:3]  # Taking only the first 3 characters like "S01"

                new_folder_name = f"{series_name} {season}"
                # If the new folder name isn't in the parent folder name, rename parent folder
                if new_folder_name not in parent_folder.name:
                    new_parent_folder = parent_folder.parent / new_folder_name
                    if not dry_run:
                        if not new_parent_folder.exists():
                            parent_folder.rename(new_parent_folder)
                            action_history.append({
                                "type": "rename",
                                "from": str(parent_folder),
                                "to": str(new_parent_folder)
                            })
                            logger.info(f"Renamed folder: {parent_folder} -> {new_parent_folder}")

            if custom_actions and category in custom_actions:
                action = custom_actions[category]
                # Execute custom action, could be a script or command
                logger.info(f"Custom action for {category}: {action}")
        else:
            category_folder = file_path.parent / category
            target_path = category_folder / file_path.name
            
            if not dry_run:
                category_folder.mkdir(exist_ok=True)
                
                # Check if target already exists
                if target_path.exists():
                    logger.warning(f"Target file already exists: {target_path}")
                    return
                    
                shutil.move(str(file_path), str(target_path))
                action_history.append({
                    "type": "move",
                    "from": str(file_path),
                    "to": str(target_path)
                })
                logger.info(f"Moved: {file_path} -> {target_path}")
    except Exception as e:
        logger.error(f"Error organizing {file_path}: {e}")
    



def process_directory(
    directory_path: Path,
    progress_bar: Optional[ttk.Progressbar] = None,
    recursive: bool = True,
    logger_func: Optional[Callable[[str], None]] = None,
    dry_run: bool = False
) -> None:
    """
    Process all files in a directory, organizing them by type.
    
    Args:
        directory_path: Path to the directory to process.
        progress_bar: Optional progress bar widget to update.
        recursive: If True, process subdirectories recursively.
        logger_func: Optional callback function for logging messages.
        dry_run: If True, simulate operations without making changes.
    """
    try:
        # Count total files for progress tracking
        file_count = 0
        for root, dirs, files in os.walk(directory_path):
            file_count += len(files)
            if not recursive:
                break

        if file_count == 0:
            message = "No files found to process"
            logger.info(message)
            if logger_func:
                logger_func(message)
            return

        processed_files = 0

        for root, dirs, files in os.walk(directory_path):
            for entry in files:
                file_path = Path(root) / entry
                file_type = get_file_type(file_path)
                
                if file_type:
                    new_file_path = rename_file(file_path, file_type, dry_run=dry_run)
                    organize_file(new_file_path, file_type, dry_run=dry_run)
                    
                    if logger_func:
                        status = "Would process" if dry_run else "Processed"
                        logger_func(f"{status}: {file_path} -> {file_type}")

                processed_files += 1
                if progress_bar:
                    progress_bar["value"] = (processed_files / file_count) * 100
                    progress_bar.update()
            
            if not recursive:
                break
                
        message = f"Completed processing {processed_files} files"
        logger.info(message)
        if logger_func:
            logger_func(message)
            
    except Exception as e:
        error_msg = f"Error processing directory: {e}"
        logger.error(error_msg)
        if logger_func:
            logger_func(error_msg)
        raise


class FileOrganizerGUI:
    """
    GUI application for organizing files by type.
    
    Provides a tkinter-based interface for selecting directories and organizing
    files with features like progress tracking, dry run mode, duplicate detection,
    and undo functionality.
    """
    
    def __init__(self):
        """Initialize the File Organizer GUI application."""
        self.root = tk.Tk()
        self.root.title("File Organizer")
        self.root.geometry("600x550")

        self.selected_directory = tk.StringVar()
        self.recursive = tk.BooleanVar(value=True)

        self.directories_used = config.get("directories", [])

        self.create_gui()

    def create_gui(self) -> None:
        """Create and layout all GUI widgets."""
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


    def log(self, message: str) -> None:
        """
        Add a message to the log display area.
        
        Args:
            message: Message to log.
        """
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.yview(tk.END)

    def select_directory(self) -> None:
        """
        Open a directory selection dialog and save the selection.
        
        Updates the directory combo box and saves to config if a new directory is selected.
        """
        selected = filedialog.askdirectory()
        if selected:
            self.selected_directory.set(selected)
            if selected not in self.directories_used:
                self.directories_used.append(selected)
                self.directory_combo['values'] = self.directories_used
                save_config({"directories": self.directories_used, "file_types": config.get("file_types", {})})

    def process_selected_directory(self) -> None:
        """
        Process the selected directory to organize files.
        
        Shows progress and handles errors with appropriate message boxes.
        Optionally checks for duplicates after processing.
        """
        directory_path = self.selected_directory.get()
        
        if not directory_path:
            messagebox.showwarning("No Directory", "Please select a directory first.")
            return
            
        if not Path(directory_path).exists():
            messagebox.showerror("Invalid Directory", "The selected directory does not exist.")
            return
            
        self.progress_bar["value"] = 0
        self.progress_bar.update()
        
        try:
            process_directory(
                Path(directory_path), 
                self.progress_bar, 
                self.recursive.get(), 
                self.log, 
                self.dry_run_mode.get()
            )
            messagebox.showinfo("Done", "✅ All files have been processed successfully!")
            
            if not self.dry_run_mode.get():
                self.log("Checking for duplicates...")
                check_for_duplicates(directory_path, self.log)
        except Exception as e:
            logger.exception("Error processing directory")
            messagebox.showerror("Error", f"❌ An error occurred:\n\n{str(e)}")

    def undo(self) -> None:
        """
        Undo the last file operation.
        
        Logs success or failure message.
        """
        if undo_last_action():
            self.log("✅ Undid the last action.")
        else:
            self.log("⚠️ No actions to undo.")

    def find_duplicates(self) -> None:
        """
        Find and display duplicate files in the selected directory.
        
        Logs all duplicate files found with their original counterparts.
        """
        directory_path = self.selected_directory.get()
        
        if not directory_path:
            self.log("⚠️ Please select a directory first.")
            messagebox.showwarning("No Directory", "Please select a directory first.")
            return
            
        if not Path(directory_path).exists():
            self.log("❌ Selected directory does not exist.")
            messagebox.showerror("Invalid Directory", "The selected directory does not exist.")
            return
            
        self.log("🔍 Checking for duplicates...")
        duplicates = check_for_duplicates(directory_path, self.log)
        
        if duplicates:
            self.log(f"✅ Found {len(duplicates)} duplicate file(s).")
        else:
            self.log("✅ No duplicates found.")


def main() -> None:
    """Main entry point for the application."""
    try:
        app = FileOrganizerGUI()
    except Exception as e:
        logger.exception("Fatal error starting application")
        print(f"Error: {e}")


if __name__ == "__main__":
    main()