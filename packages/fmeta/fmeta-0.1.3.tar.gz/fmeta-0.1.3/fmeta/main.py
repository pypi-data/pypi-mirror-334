import os
import sys
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from fmeta.version import __version__
from fmeta.version import __author__
from fmeta.version import __email__

# varaible
size_col="Size (MB)"

# Function to display help
def print_help():
	help_message = """
Usage: fmeta [OPTIONS] [DIRECTORY]

A small package to scan directories and list file metadata in a tabular format.

Options:
	--version, -v      Show the version of fmeta and exit
	--help, -h         Show this help message and exit
	--sort COLUMN      Sort by the specified column (CLI mode)
	(No arguments)     Launch the GUI application
	[DIRECTORY]        Launch GUI with the number of files in the specified directory
	"""
	print(help_message)
	sys.exit(0)

# Function to get file metadata
def get_file_metadata(folder, sort_by=size_col):
	file_data = []
	for root, _, files in os.walk(folder):
		for file in files:
			file_path = os.path.join(root, file)
			try:
				stat = os.stat(file_path)
				file_data.append({
					"Path": file_path,
					size_col: round(stat.st_size / (1024 * 1024), 4),
					"Created": pd.to_datetime(stat.st_ctime, unit="s").strftime("%Y-%m-%d %H:%M:%S"),
					"Modified": pd.to_datetime(stat.st_mtime, unit="s").strftime("%Y-%m-%d %H:%M:%S"),
					"File Type": os.path.splitext(file)[1]
				})
			except Exception as e:
				print(f"Error reading file: {file_path} - {e}")
	df = pd.DataFrame(file_data)
	return df.sort_values(by=sort_by, ascending=False) if not df.empty else df

# GUI Application
def create_gui(initial_folder=None,sort_col=size_col):
	def select_folder():
		path = filedialog.askdirectory(title="Select a Folder")
		if path:
			folder_var.set(path)
	
	def scan():
		folder = folder_var.get()
		if not folder:
			messagebox.showerror("Error", "Please select a folder")
			return
		if not os.path.exists(folder):
			messagebox.showerror("Error", "Selected folder does not exist")
			return
		
		df = get_file_metadata(folder, sort_by=sort_option.get())
		file_count = len(df)
		
		if df.empty:
			messagebox.showinfo("No Files", "No files found in the selected directory.")
			return
		
		messagebox.showinfo("Scan Complete", f"Total files found: {file_count}")
		
		# Display results in a popup window
		popup = tk.Toplevel(root)
		popup.title("File Metadata Results")
		popup.geometry("900x400")
		
		tree = ttk.Treeview(popup, columns=list(df.columns), show="headings")
		for col in df.columns:
			tree.heading(col, text=col, anchor="center")
			tree.column(col, width=150, anchor="w")
		
		for _, row in df.iterrows():
			tree.insert("", tk.END, values=list(row))
		
		tree.pack(expand=True, fill=tk.BOTH)
		scrollbar = ttk.Scrollbar(popup, orient="vertical", command=tree.yview)
		tree.configure(yscrollcommand=scrollbar.set)
		scrollbar.pack(side="right", fill="y")
	
	root = tk.Tk()
	root.title("File Metadata Scanner")
	root.geometry("500x250")
	
	folder_var = tk.StringVar()
	sort_option = tk.StringVar(value=sort_col)
	if initial_folder:
		folder_var.set(initial_folder)
		root.after(100, scan)  # Auto-scan after GUI loads
	
	tk.Label(root, text="Folder Path:", font=("Arial", 12)).pack(pady=5)
	tk.Entry(root, textvariable=folder_var, width=50).pack()
	tk.Button(root, text="Select Folder", command=select_folder).pack(pady=5)
	
	tk.Label(root, text="Sort By:", font=("Arial", 12)).pack(pady=5)
	tk.OptionMenu(root, sort_option, size_col,"Path", "Created", "Modified", "File Type").pack()
	
	tk.Button(root, text="Scan Files", command=scan, font=("Arial", 12, "bold"), bg="lightblue").pack(pady=20)
	
	root.mainloop()

# Main entry point
def main():
	sort_by = size_col

	if "--version" in sys.argv or "-v" in sys.argv:
		print(f"fmeta version {__version__}")
		sys.exit(0)

	if "--author" in sys.argv or "-a" in sys.argv:
		print(f"Author {__author__}")
		sys.exit(0)

	if "--email" in sys.argv or "-e" in sys.argv:
		print(f"Mailto {__email__}")
		sys.exit(0)

	if "--help" in sys.argv or "-h" in sys.argv:
		print_help()
		sys.exit(0)
	
	if "--sort" in sys.argv:
		try:
			sort_by = sys.argv[sys.argv.index("--sort") + 1]
		except IndexError:
			print("Error: Please provide a column name for sorting.")
			sys.exit(1)

	if len(sys.argv) > 1 and sys.argv[-1] not in ["--sort", sort_by]:
		directory = sys.argv[-1]
		if os.path.exists(directory):
			create_gui(initial_folder=directory,sort_col=sort_by)
		else:
			print(f"Error: Directory '{directory}' does not exist.")
			sys.exit(1)
	else:
		create_gui()

if __name__ == "__main__":
	main()