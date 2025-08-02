# Image PDF Processor

A desktop application built with Python and Tkinter for processing images and PDF files. This tool provides two main functions: merging images into PDF and merging multiple PDF files.

## Features

### 1. Image to PDF Merger
- Select a folder containing images
- Support multiple image formats: PNG, JPG, JPEG, WEBP, BMP, TIFF
- Choose specific image types to process
- Automatically sort images in dictionary order
- Merge selected images into a single PDF file

### 2. PDF Merger
- Select multiple PDF files
- Reorder files (move up/down)
- Remove unwanted files from the list
- Merge PDFs in the specified order

## Installation

1. Make sure you have Python 3.x installed
2. Install required dependencies:

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install Pillow PyPDF2
```

## Usage

### Method 1: Run the main application
```bash
python image_pdf_processor.py
```

### Method 2: Use the startup script
```bash
python start_app.py
```

### Method 3: Use batch file (Windows)
```bash
start_app.bat
```

## Interface Features

- **Tabbed Interface**: Separate tabs for different functions
- **File List Display**: Intuitive file list with selection capabilities
- **Progress Indicators**: Progress bars show processing status
- **Error Handling**: Friendly error messages and success notifications
- **Multi-threading**: Non-blocking UI during processing

## File Structure

- `image_pdf_processor.py` - Main application with GUI
- `image_merger.py` - Original image merging script
- `pdf_merger.py` - Original PDF merging script
- `start_app.py` - Application launcher with dependency checking
- `start_app.bat` - Windows batch file launcher
- `requirements.txt` - Python dependencies
- `README.md` - This documentation

## Requirements

- Python 3.x
- Pillow (PIL) >= 9.0.0
- PyPDF2 >= 3.0.0
- Tkinter (usually included with Python)

## Supported Formats

### Images
- PNG
- JPG/JPEG
- WEBP
- BMP
- TIFF

### PDF
- Standard PDF files (non-encrypted)

## Notes

1. **File Paths**: Avoid special characters in file paths
2. **Permissions**: Ensure the application has read/write permissions for selected files
3. **Memory Usage**: Processing large images or PDF files may consume significant memory
4. **Image Conversion**: Images are automatically converted to RGB format for PDF compatibility
5. **Error Handling**: If a file fails to process, the application will skip it and continue with others

## Troubleshooting

**Q: Missing module error when running?**
A: Install all dependencies using `pip install -r requirements.txt`

**Q: Large PDF file size after merging images?**
A: This is normal as the application preserves original image quality

**Q: Some images cannot be processed?**
A: Check if the image files are corrupted or in an unsupported format

**Q: PDF merge fails?**
A: Ensure PDF files are not corrupted or encrypted

## Technical Details

- **GUI Framework**: Tkinter
- **Image Processing**: Pillow (PIL)
- **PDF Processing**: PyPDF2
- **Threading**: Python threading module for non-blocking operations
- **File Sorting**: Python built-in sorting for dictionary order

## Version

- Version: 1.0
- Language: Python 3.x
- Supported OS: Windows, macOS, Linux

## License

This project is open source. Feel free to use and modify as needed.