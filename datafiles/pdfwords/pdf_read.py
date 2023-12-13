from PyPDF2 import PdfReader, PdfWriter

def split(source_fn, page_from, page_to):
    with open(source_fn, "rb") as source_file:
        pdf_reader = PdfReader(source_file)
       
        for page in range(page_from, page_to):
            # pdf_writer.add_page(pdf_reader.pages[page])
            #pdf_writer.write('F:\pdfs\' + )
            pdf_writer = PdfWriter()
            pdf_writer.add_page(pdf_reader.pages[page])
            fileName = "F:\\pdfs\\" + str(page) + ".pdf"; 
            with open(fileName, "wb") as output_file:
                pdf_writer.write(output_file)
    # F:\pdfs
    #with open(target_fn, "wb") as output_file:
    #    pdf_writer.write(output_file)

split("F:\\aaa.pdf", 0, 14)
