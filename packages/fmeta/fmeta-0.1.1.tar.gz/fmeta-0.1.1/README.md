# fmeta - File Metadata Scanner

`fmeta` is a lightweight tool to scan directories and list file metadata in a tabular format.  
It supports sorting, GUI mode, and command-line usage.

## Features
- Scan a folder and list file metadata (size, creation date, modification date, etc.).
- Sort files based on different metadata fields.
- Supports both **CLI mode** and **GUI mode** for interactive browsing.

## Installation
Install `fmeta` using pip:
```sh
pip install fmeta
```

## Example Usage  
### Scan a folder and display file details in a table:  
```sh
fmeta /path/to/directory
```

### Sort files by creation date in CLI mode:  
```sh
fmeta --sort <Column name> /path/to/directory
```

### Launch GUI for interactive file browsing:  
```sh
fmeta
```