# File Organizer

File Organizer is a production-ready Python application that organizes files in a directory based on their file type. The application features a user-friendly GUI built with tkinter, enabling easy file management with advanced features like duplicate detection, dry-run mode, and undo functionality.

## Features

- 🗂️ **Automatic Organization**: Organizes files by type (Images, Videos, Documents, Audio, Archives, etc.)
- 🖥️ **User-Friendly GUI**: Simple and intuitive interface built with tkinter
- 📊 **Progress Tracking**: Real-time progress bar during file organization
- 🔍 **Duplicate Detection**: Find and identify duplicate files using SHA256 hashing
- 🧪 **Dry Run Mode**: Preview changes before applying them
- ↩️ **Undo Functionality**: Revert the last file operation
- 📝 **Activity Logging**: Comprehensive logging of all operations
- 🔄 **Recursive Processing**: Optionally process subdirectories
- 🎯 **History Tracking**: Remember previously used directories
- ⚙️ **Customizable**: Support for custom file type mappings via configuration

## Supported File Types

The application recognizes and organizes the following file types:

- **Images**: jpg, jpeg, png, gif, bmp, svg, webp
- **Videos**: mp4, mkv, ts, avi, mov, wmv, flv, webm
- **Documents**: pdf, doc, docx, txt, odt, rtf, xls, xlsx, ppt, pptx
- **Audio**: mp3, wav, flac, aac, ogg, wma, m4a
- **Archives**: zip, rar, 7z, tar, gz, bz2, xz

## Requirements

- Python 3.8 or higher
- tkinter library (included with most Python installations)

### Platform-Specific Requirements

**Linux/Ubuntu:**
```bash
sudo apt-get install python3-tk
```

**macOS:**
tkinter is included with Python installations from python.org

**Windows:**
tkinter is included with Python installations from python.org

## Installation

### Option 1: Clone from GitHub

```bash
# Clone the repository
git clone https://github.com/Abudi-seid10/File_manager.git
cd File_manager

# (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the application
pip install -e .
```

### Option 2: Direct Download

1. Download the repository as a ZIP file
2. Extract the contents
3. Navigate to the directory in your terminal
4. Run: `python main.py`

## Usage

### Running the Application

```bash
# Run directly
python main.py

# Or if installed via pip
file-organizer
```

### Using the GUI

1. **Select Directory**: Click "Select Directory" to choose a folder to organize
2. **Configure Options**:
   - ✅ **Recursive**: Process subdirectories
   - 🧪 **Dry Run Mode**: Preview changes without applying them
3. **Start Processing**: Click "Start" to begin organizing files
4. **Additional Features**:
   - **Undo**: Revert the last file operation
   - **Find Duplicates**: Scan for duplicate files in the selected directory

### Configuration

Create a `config.json` file to customize file type mappings:

```json
{
  "directories": [],
  "file_types": {
    ".custom": "CustomCategory",
    ".special": "SpecialFiles"
  }
}
```

The application will automatically save your directory history to `config.json`.

## Development

### Running Tests

```bash
# Run all tests
python -m unittest discover tests -v

# Run specific test file
python -m unittest tests.test_main -v
```

### Code Quality

```bash
# Format code
pip install black
black main.py

# Check types
pip install mypy
mypy main.py --ignore-missing-imports

# Lint code
pip install flake8
flake8 main.py --max-line-length=120
```

## Project Structure

```
File_manager/
├── main.py                 # Main application file
├── config.json             # User configuration (auto-generated)
├── config.example.json     # Example configuration
├── requirements.txt        # Python dependencies
├── setup.py               # Installation script
├── LICENSE                # MIT License
├── README.md              # This file
├── .gitignore            # Git ignore rules
├── tests/                # Test suite
│   ├── __init__.py
│   └── test_main.py
└── .github/
    └── workflows/
        └── ci.yml        # CI/CD configuration
```

## Safety Features

- **Dry Run Mode**: Test operations without making actual changes
- **Undo Functionality**: Revert accidental operations
- **Duplicate Detection**: Avoid data loss by identifying duplicates
- **Error Handling**: Comprehensive error handling and logging
- **Input Validation**: Validates directories and file paths

## Logging

All operations are logged to:
- Console output
- `file_organizer.log` file in the application directory

Log entries include timestamps, operation types, and detailed messages.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Known Limitations

- The application requires a graphical environment (GUI)
- Video series organization follows a specific naming pattern (Series Name SxxExx)
- Large directories may take time to process

## Troubleshooting

**Issue**: "No module named 'tkinter'"
**Solution**: Install tkinter for your platform (see Requirements section)

**Issue**: Application doesn't start
**Solution**: Ensure Python 3.8+ is installed and tkinter is available

**Issue**: Files not being organized
**Solution**: Check the log output for errors and ensure files have recognized extensions

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with Python and tkinter
- Uses SHA256 for file hash comparison
- Inspired by the need for better file organization tools

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check the log file for detailed error messages
