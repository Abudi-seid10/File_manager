"""Unit tests for File Organizer."""

import unittest
import tempfile
import shutil
from pathlib import Path
import json
import sys
import os

# Add parent directory to path to import main
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import (
    get_file_type,
    get_file_hash,
    rename_file,
    check_for_duplicates,
    load_config,
    save_config,
    DEFAULT_FILE_TYPES
)


class TestFileOrganizer(unittest.TestCase):
    """Test cases for file organizer functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.test_path = Path(self.test_dir)

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_get_file_type_image(self):
        """Test file type detection for image files."""
        test_file = self.test_path / "test.jpg"
        self.assertEqual(get_file_type(test_file), "Images")
        
        test_file = self.test_path / "test.png"
        self.assertEqual(get_file_type(test_file), "Images")

    def test_get_file_type_video(self):
        """Test file type detection for video files."""
        test_file = self.test_path / "test.mp4"
        self.assertEqual(get_file_type(test_file), "Videos")
        
        test_file = self.test_path / "test.mkv"
        self.assertEqual(get_file_type(test_file), "Videos")

    def test_get_file_type_document(self):
        """Test file type detection for document files."""
        test_file = self.test_path / "test.pdf"
        self.assertEqual(get_file_type(test_file), "Documents")
        
        test_file = self.test_path / "test.docx"
        self.assertEqual(get_file_type(test_file), "Documents")

    def test_get_file_type_unknown(self):
        """Test file type detection for unknown files."""
        test_file = self.test_path / "test.xyz"
        self.assertIsNone(get_file_type(test_file))

    def test_get_file_hash(self):
        """Test file hashing functionality."""
        test_file = self.test_path / "test.txt"
        test_file.write_text("Hello, World!")
        
        hash1 = get_file_hash(test_file)
        self.assertIsNotNone(hash1)
        self.assertEqual(len(hash1), 64)  # SHA256 hash length
        
        # Create identical file
        test_file2 = self.test_path / "test2.txt"
        test_file2.write_text("Hello, World!")
        
        hash2 = get_file_hash(test_file2)
        self.assertEqual(hash1, hash2)

    def test_rename_file_dry_run(self):
        """Test file renaming in dry run mode."""
        test_file = self.test_path / "test.with.dots.txt"
        test_file.touch()
        
        new_path = rename_file(test_file, "Documents", dry_run=True)
        
        # Original file should still exist
        self.assertTrue(test_file.exists())
        # New path should have spaces instead of dots
        self.assertEqual(new_path.stem, "test with dots")

    def test_rename_file_actual(self):
        """Test actual file renaming."""
        test_file = self.test_path / "test.with.dots.txt"
        test_file.touch()
        
        new_path = rename_file(test_file, "Documents", dry_run=False)
        
        # Original file should not exist
        self.assertFalse(test_file.exists())
        # New file should exist
        self.assertTrue(new_path.exists())
        # Name should have spaces instead of dots
        self.assertEqual(new_path.stem, "test with dots")

    def test_check_for_duplicates(self):
        """Test duplicate file detection."""
        # Create two identical files
        file1 = self.test_path / "file1.txt"
        file1.write_text("Identical content")
        
        file2 = self.test_path / "file2.txt"
        file2.write_text("Identical content")
        
        # Create a different file
        file3 = self.test_path / "file3.txt"
        file3.write_text("Different content")
        
        duplicates = check_for_duplicates(str(self.test_path))
        
        # Should find one duplicate pair
        self.assertEqual(len(duplicates), 1)
        self.assertIn(str(file2), duplicates[0][0])

    def test_config_operations(self):
        """Test configuration save and load."""
        # Save to a temporary location
        original_dir = os.getcwd()
        os.chdir(self.test_dir)
        
        try:
            test_config = {
                "directories": ["/test/path1", "/test/path2"],
                "file_types": {".custom": "CustomType"}
            }
            
            save_config(test_config)
            
            # Check file was created
            config_file = Path("config.json")
            self.assertTrue(config_file.exists())
            
            # Load and verify
            loaded_config = load_config()
            self.assertEqual(loaded_config["directories"], test_config["directories"])
            self.assertEqual(loaded_config["file_types"], test_config["file_types"])
        finally:
            os.chdir(original_dir)


class TestDefaultFileTypes(unittest.TestCase):
    """Test cases for default file type mappings."""

    def test_default_file_types_exist(self):
        """Test that default file types are defined."""
        self.assertIsNotNone(DEFAULT_FILE_TYPES)
        self.assertIsInstance(DEFAULT_FILE_TYPES, dict)
        self.assertGreater(len(DEFAULT_FILE_TYPES), 0)

    def test_common_extensions_covered(self):
        """Test that common file extensions are covered."""
        common_extensions = [
            '.jpg', '.png', '.pdf', '.mp4', '.mp3', 
            '.doc', '.docx', '.zip', '.txt'
        ]
        
        for ext in common_extensions:
            self.assertIn(ext, DEFAULT_FILE_TYPES)


if __name__ == "__main__":
    unittest.main()
