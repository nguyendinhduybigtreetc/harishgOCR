import os

import fitz  # PyMuPDF
from PyPDF2 import PdfReader
import gpu_box
import gpu_ocr

zoom = 2  # zoom factor
mat = fitz.Matrix(zoom, zoom)


def convert_pdf_to_images(input_folder, output_folder, tmp_folder, first_folder_path, progress):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    pdf_files = [file for file in os.listdir(input_folder) if file.endswith(".pdf")]

    for index, pdf_file in enumerate(pdf_files):
        pdf_path = os.path.join(input_folder, pdf_file)

        f = open(pdf_path, "rb")
        pdf_reader = PdfReader(f)
        num_pages = len(pdf_reader.pages)
        f.close()
        pdf_document = fitz.open(pdf_path)
        # num_pages = pdf_document.page_count()
        page = pdf_document.load_page(0)
        image = page.get_pixmap(matrix=mat, dpi=150)

        image_path = os.path.join(first_folder_path, f"{pdf_file}_page_1.png")
        image.save(image_path)

        gpu_ocr.ocrImgFirst(image_path, pdf_file)
        os.remove(image_path)
        for page_number in range(2, num_pages - 1):
            page = pdf_document.load_page(page_number)
            image = page.get_pixmap(matrix=mat, dpi=150)

            image_path = os.path.join(tmp_folder, f"{pdf_file}_page_{page_number + 1}.png")
            print(image_path)
            image.save(image_path)

            # images = box.boxCardNameSplit(image_path)
            """
            
            
            os.remove(image_path)
            count = 1
            for img in images:
                if img.width > 350 and img.height > 120:
                    img_path = os.path.join(output_folder, f"{pdf_file}_page_{page_number + 1}_card_{count}.png")
                    img.save(img_path, 'png')
                count += 1
            """

            gpu_box.cropbox()
            gpu_ocr.ocrcardname(pdf_file, page_number)
            gpu_ocr.ocrcardnameDelete(pdf_file, page_number)
            progress(float((index+1) / len(pdf_files)), desc="scan: " + pdf_file)
            os.remove(image_path)
            # break

        while True:
            if pdf_document.is_closed:
                break
            else:
                pdf_document.close()

        os.unlink(os.path.join("fileupload", pdf_file))


def pdfToImage(progress):
    input_folder_path = "fileupload"
    output_folder_path = "cardimage"
    tmp_folder_path = "tmppdf"
    first_folder_path = "firstpageimage"

    convert_pdf_to_images(input_folder_path, output_folder_path, tmp_folder_path, first_folder_path, progress)

