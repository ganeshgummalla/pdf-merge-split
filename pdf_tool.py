import os
import tkinter as tk
from tkinter import filedialog, simpledialog
from pypdf import PdfReader, PdfWriter

# Hide Tkinter root window
root = tk.Tk()
root.withdraw()


# ---------------- File Dialogs ----------------

def select_pdf_files(multiple=True, title="Select PDF File(s)"):
    filetypes = [("PDF Files", "*.pdf")]

    if multiple:
        return list(
            filedialog.askopenfilenames(
                title=title,
                filetypes=filetypes
            )
        )
    else:
        return filedialog.askopenfilename(
            title=title,
            filetypes=filetypes
        )


def save_pdf_file(title="Save PDF As"):
    return filedialog.asksaveasfilename(
        title=title,
        defaultextension=".pdf",
        filetypes=[("PDF Files", "*.pdf")]
    )


# ---------------- Merge PDFs ----------------

def merge_pdfs():

    try:
        files = select_pdf_files(
            multiple=True,
            title="Select PDFs to Merge"
        )

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

        with open(output_path, "wb") as f:
            writer.write(f)

        print(f"[SUCCESS] {len(files)} PDFs merged successfully.")

    except FileNotFoundError:
        print("[ERROR] File not found.")

    except PermissionError:
        print("[ERROR] Permission denied.")

    except Exception as e:
        print(f"[ERROR] {e}")


# ---------------- Split Single Pages ----------------

def split_single_pages():

    try:

        file = select_pdf_files(
            multiple=False,
            title="Select PDF"
        )

        if not file:
            return

        output_folder = filedialog.askdirectory(
            title="Select Output Folder"
        )

        if not output_folder:
            return

        reader = PdfReader(file)

        for i, page in enumerate(reader.pages, start=1):

            writer = PdfWriter()

            writer.add_page(page)

            out_path = os.path.join(
                output_folder,
                f"page_{i}.pdf"
            )

            with open(out_path, "wb") as f:
                writer.write(f)

        print(
            f"[SUCCESS] Split into {len(reader.pages)} pages."
        )

    except FileNotFoundError:
        print("[ERROR] File not found.")

    except PermissionError:
        print("[ERROR] Permission denied.")

    except Exception as e:
        print(f"[ERROR] {e}")


# ---------------- Split into Chunks ----------------

def split_chunks():

    try:

        file = select_pdf_files(
            multiple=False,
            title="Select PDF"
        )

        if not file:
            return

        output_folder = filedialog.askdirectory(
            title="Select Output Folder"
        )

        if not output_folder:
            return

        chunk_size = simpledialog.askinteger(
            "Chunk Size",
            "Enter pages per chunk:"
        )

        if not chunk_size or chunk_size <= 0:
            print("[ERROR] Invalid chunk size.")
            return

        reader = PdfReader(file)

        total_pages = len(reader.pages)

        chunk = 1

        for start in range(0, total_pages, chunk_size):

            writer = PdfWriter()

            end = min(
                start + chunk_size,
                total_pages
            )

            for i in range(start, end):
                writer.add_page(reader.pages[i])

            out_path = os.path.join(
                output_folder,
                f"chunk_{chunk}.pdf"
            )

            with open(out_path, "wb") as f:
                writer.write(f)

            chunk += 1

        print("[SUCCESS] PDF split into chunks.")

    except FileNotFoundError:
        print("[ERROR] File not found.")

    except PermissionError:
        print("[ERROR] Permission denied.")

    except Exception as e:
        print(f"[ERROR] {e}")
# ---------------- Extract Pages ----------------

def extract_pages():

    try:

        file = select_pdf_files(
            multiple=False,
            title="Select PDF"
        )

        if not file:
            return

        reader = PdfReader(file)

        total_pages = len(reader.pages)

        start_page = simpledialog.askinteger(
            "Start Page",
            f"Enter start page (1-{total_pages})"
        )

        end_page = simpledialog.askinteger(
            "End Page",
            f"Enter end page ({start_page}-{total_pages})"
        )

        if start_page is None or end_page is None:
            return

        if start_page < 1 or end_page > total_pages or start_page > end_page:
            print("[ERROR] Invalid page range.")
            return

        output_path = save_pdf_file(
            "Save Extracted PDF As"
        )

        if not output_path:
            return

        writer = PdfWriter()

        for i in range(start_page - 1, end_page):
            writer.add_page(reader.pages[i])

        with open(output_path, "wb") as f:
            writer.write(f)

        print(
            f"[SUCCESS] Pages {start_page}-{end_page} extracted."
        )

    except FileNotFoundError:
        print("[ERROR] File not found.")

    except PermissionError:
        print("[ERROR] Permission denied.")

    except Exception as e:
        print(f"[ERROR] {e}")


# ---------------- Rotate Pages ----------------

def rotate_pages():

    try:

        file = select_pdf_files(
            multiple=False,
            title="Select PDF"
        )

        if not file:
            return

        rotation = simpledialog.askinteger(
            "Rotation",
            "Enter rotation (90,180,270):"
        )

        if rotation not in [90, 180, 270]:
            print("[ERROR] Invalid rotation.")
            return

        output_path = save_pdf_file(
            "Save Rotated PDF As"
        )

        if not output_path:
            return

        reader = PdfReader(file)

        writer = PdfWriter()

        for page in reader.pages:
            page.rotate(rotation)
            writer.add_page(page)

        with open(output_path, "wb") as f:
            writer.write(f)

        print(
            f"[SUCCESS] PDF rotated by {rotation}°."
        )

    except FileNotFoundError:
        print("[ERROR] File not found.")

    except PermissionError:
        print("[ERROR] Permission denied.")

    except Exception as e:
        print(f"[ERROR] {e}")


# ---------------- Delete Pages ----------------

def delete_pages():

    try:

        file = select_pdf_files(
            multiple=False,
            title="Select PDF"
        )

        if not file:
            return

        reader = PdfReader(file)

        total_pages = len(reader.pages)

        pages = simpledialog.askstring(
            "Delete Pages",
            "Enter page numbers separated by commas\nExample: 2,5,7"
        )

        if not pages:
            return

        delete_pages = []

        try:
            delete_pages = [
                int(x.strip()) - 1
                for x in pages.split(",")
            ]
        except:
            print("[ERROR] Invalid page numbers.")
            return

        writer = PdfWriter()

        for i in range(total_pages):

            if i not in delete_pages:
                writer.add_page(reader.pages[i])

        output_path = save_pdf_file(
            "Save PDF As"
        )

        if not output_path:
            return

        with open(output_path, "wb") as f:
            writer.write(f)

        print("[SUCCESS] Selected pages deleted.")

    except Exception as e:
        print(f"[ERROR] {e}")


# ---------------- PDF Information ----------------

def pdf_info():

    try:

        file = select_pdf_files(
            multiple=False,
            title="Select PDF"
        )

        if not file:
            return

        reader = PdfReader(file)

        print("\n----------- PDF INFO -----------")
        print("File :", os.path.basename(file))
        print("Location :", file)
        print("Pages :", len(reader.pages))

        metadata = reader.metadata

        if metadata:

            print("\nMetadata")

            for key, value in metadata.items():
                print(f"{key} : {value}")

        else:
            print("\nNo metadata found.")

        print("-------------------------------")

    except Exception as e:
        print(f"[ERROR] {e}")

# ---------------- Encrypt PDF ----------------

def encrypt_pdf():

    try:

        file = select_pdf_files(
            multiple=False,
            title="Select PDF to Encrypt"
        )

        if not file:
            return

        password = simpledialog.askstring(
            "Password",
            "Enter password for PDF:"
        )

        if not password:
            print("[ERROR] Password cannot be empty.")
            return

        output_path = save_pdf_file(
            "Save Encrypted PDF As"
        )

        if not output_path:
            return

        reader = PdfReader(file)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        writer.encrypt(password)

        with open(output_path, "wb") as f:
            writer.write(f)

        print("[SUCCESS] PDF encrypted successfully.")

    except FileNotFoundError:
        print("[ERROR] File not found.")

    except PermissionError:
        print("[ERROR] Permission denied.")

    except Exception as e:
        print(f"[ERROR] {e}")


# ---------------- Decrypt PDF ----------------

def decrypt_pdf():

    try:

        file = select_pdf_files(
            multiple=False,
            title="Select Encrypted PDF"
        )

        if not file:
            return

        password = simpledialog.askstring(
            "Password",
            "Enter PDF password:"
        )

        if password is None:
            return

        reader = PdfReader(file)

        if reader.is_encrypted:

            if reader.decrypt(password) == 0:
                print("[ERROR] Incorrect password.")
                return

        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        output_path = save_pdf_file(
            "Save Decrypted PDF As"
        )

        if not output_path:
            return

        with open(output_path, "wb") as f:
            writer.write(f)

        print("[SUCCESS] PDF decrypted successfully.")

    except Exception as e:
        print(f"[ERROR] {e}")


# ---------------- Menu ----------------

def main():

    while True:

        print("\n" + "=" * 40)
        print("         PDF TOOL")
        print("=" * 40)
        print("1. Merge PDFs")
        print("2. Split into Single Pages")
        print("3. Split into Chunks")
        print("4. Extract Pages")
        print("5. Rotate Pages")
        print("6. Delete Pages")
        print("7. PDF Information")
        print("8. Encrypt PDF")
        print("9. Decrypt PDF")
        print("0. Exit")
        print("=" * 40)

        choice = input("Enter your choice: ").strip()

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

        elif choice == "6":
            delete_pages()

        elif choice == "7":
            pdf_info()

        elif choice == "8":
            encrypt_pdf()

        elif choice == "9":
            decrypt_pdf()

        elif choice == "0":
            print("Exiting PDF Tool...")
            break

        else:
            print("[ERROR] Invalid choice. Please try again.")


# ---------------- Run Program ----------------

if __name__ == "__main__":
    main()
