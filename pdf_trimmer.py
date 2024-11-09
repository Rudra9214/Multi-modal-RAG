from PyPDF2 import PdfReader, PdfWriter

 

def delete_pages_after_6(pdf_file_path):

    # Create PdfReader and PdfWriter objects

    reader = PdfReader(pdf_file_path)

    writer = PdfWriter()

 

    # Check the total number of pages in the PDF

    total_pages = len(reader.pages)

 

    # If there are more than 6 pages, delete pages starting from 7th page

    if total_pages > 6:

        # Append the first 6 pages to the writer object (keeping them)

        for i in range(6):

            writer.add_page(reader.pages[i])

       

        # Write the result to a new PDF (overwriting original)

        with open(pdf_file_path, "wb") as output_file:

            writer.write(output_file)

        print(f"Pages after the 6th page have been deleted. Total pages now: 6")

    else:

        print(f"PDF has {total_pages} pages, which is 6 or fewer. No pages were deleted.")

 

# Path to your PDF file

pdf_file_path = 'sample06.pdf'

delete_pages_after_6(pdf_file_path)
