import os
import tkinter as tk
from tkinter import filedialog, simpledialog
from pypdf import PdfReader, PdfWriter

# Hide the main Tkinter window
root = tk.Tk()
root.withdraw()

def select_pdf_files(multiple=True, title="Select PDF file(s)"):
    filetypes = [("PDF files", "*.pdf")]
    if multiple:
        return list(filedialog.askopenfilenames(title=title, filetypes=filetypes))
    else:
        return filedialog.askopenfilename(title=title, filetypes=filetypes)

def save_pdf_file(title="Save PDF As"):
    return filedialog.asksaveasfilename(
        title=title,
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf")]
    )

# ------------------ Merge ------------------
def merge_pdfs():
    files = select_pdf_files(multiple=True, title="Select PDFs to Merge")
    if not files:
        print("[ERROR] No files selected.")
        return
    output_path = save_pdf_file("Save Merged PDF As")
    if not output_path:
        return

    writer = PdfWriter()
    for pdf in files:
        reader = PdfReader(pdf)
        for page in reader.pages:
            writer.add_page(page)
    with open(output_path, "wb") as out_file:
        writer.write(out_file)
    print(f"[OK] Merged {len(files)} PDFs → {output_path}")

# ------------------ Split ------------------
def split_single_pages():
    file = select_pdf_files(multiple=False, title="Select PDF to Split into Single Pages")
    if not file:
        return
    output_folder = filedialog.askdirectory(title="Select Output Folder")
    if not output_folder:
        return

    reader = PdfReader(file)
    for i, page in enumerate(reader.pages, start=1):
        writer = PdfWriter()
        writer.add_page(page)
        out_path = os.path.join(output_folder, f"page_{i}.pdf")
        with open(out_path, "wb") as out_file:
            writer.write(out_file)
    print(f"[OK] Split into {len(reader.pages)} single-page files in {output_folder}")

def split_chunks():
    file = select_pdf_files(multiple=False, title="Select PDF to Split into Chunks")
    if not file:
        return
    output_folder = filedialog.askdirectory(title="Select Output Folder")
    if not output_folder:
        return
    chunk_size = simpledialog.askinteger("Chunk Size", "Enter number of pages per chunk:")
    if not chunk_size or chunk_size <= 0:
        return

    reader = PdfReader(file)
    total_pages = len(reader.pages)
    for start in range(0, total_pages, chunk_size):
        writer = PdfWriter()
        for i in range(start, min(start + chunk_size, total_pages)):
            writer.add_page(reader.pages[i])
        out_path = os.path.join(output_folder, f"chunk_{start//chunk_size + 1}.pdf")
        with open(out_path, "wb") as out_file:
            writer.write(out_file)
    print(f"[OK] Split into chunks of {chunk_size} pages in {output_folder}")

# ------------------ Extract ------------------
def extract_pages():
    file = select_pdf_files(multiple=False, title="Select PDF to Extract Pages From")
    if not file:
        return
    start_page = simpledialog.askinteger("Start Page", "Enter start page number:")
    end_page = simpledialog.askinteger("End Page", "Enter end page number:")
    if not start_page or not end_page:
        return
    output_path = save_pdf_file("Save Extracted PDF As")
    if not output_path:
        return

    reader = PdfReader(file)
    writer = PdfWriter()
    for i in range(start_page - 1, end_page):
        writer.add_page(reader.pages[i])
    with open(output_path, "wb") as out_file:
        writer.write(out_file)
    print(f"[OK] Extracted pages {start_page}-{end_page} → {output_path}")

# ------------------ Rotate ------------------
def rotate_pages():
    file = select_pdf_files(multiple=False, title="Select PDF to Rotate")
    if not file:
        return
    rotation = simpledialog.askinteger("Rotation", "Enter rotation (90, 180, 270):")
    if rotation not in [90, 180, 270]:
        print("[ERROR] Invalid rotation value.")
        return
    output_path = save_pdf_file("Save Rotated PDF As")
    if not output_path:
        return

    reader = PdfReader(file)
    writer = PdfWriter()
    for page in reader.pages:
        page.rotate(rotation)
        writer.add_page(page)
    with open(output_path, "wb") as out_file:
        writer.write(out_file)
    print(f"[OK] Rotated all pages by {rotation}° → {output_path}")

# ------------------ Menu ------------------
def main():
    while True:
        print("\nPDF Tool Menu:")
        print("1. Merge PDFs")
        print("2. Split into Single Pages")
        print("3. Split into Chunks")
        print("4. Extract Pages")
        print("5. Rotate Pages")
        print("0. Exit")

        choice = input("Enter choice: ")
        if choice == "1":
            merge_pdfs()
        elif choice == "2":
            split_single_pages()
        elif choice == "3":
            split_chunks()
        elif choice == "4":
            extract_pages()
        elif choice == "5":
            rotate_pages()
        elif choice == "0":
            break
        else:
            print("[ERROR] Invalid choice.")

if __name__ == "__main__":
    main()
