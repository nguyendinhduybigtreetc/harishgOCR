from time import sleep

import numpy as np
import gradio as gr
import os
import shutil

import file_name_utils
import pdf_extract
import zipfile
# import insert_database

def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Created folder: {folder_path}")
    else:
        print(f"Folder already exists: {folder_path}")

input_folder_path = "fileupload"
output_folder_path = "cardimage"
tmp_folder_path = "tmppdf"
first_folder_path = "firstpageimage"

create_folder_if_not_exists(input_folder_path)
create_folder_if_not_exists(output_folder_path)
create_folder_if_not_exists(tmp_folder_path)
create_folder_if_not_exists(first_folder_path)


def flip_text(x):
    return x[::-1]


def flip_image(x):
    return np.fliplr(x)

def zip_folder(folder_path, output_zip_name):
    with zipfile.ZipFile(output_zip_name, 'w') as zip_file:
        for folder_name, subfolders, file_names in os.walk(folder_path):
            for file_name in file_names:
                file_path = os.path.join(folder_name, file_name)
                zip_file.write(file_path, os.path.relpath(file_path, folder_path))

def delete_all_tmp():

    for dir in file_name_utils.LIST_FOLDER:
        for filename in os.listdir(dir):
            file_path = os.path.join(dir, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

def copy_cache_to_upload(files):
    for file in files:
        if os.path.isfile(file.name):
            shutil.copy(file.name, file_name_utils.UPLOAD_FOLDER)

def upload_file(files, progress=gr.Progress()):

    delete_all_tmp()

    copy_cache_to_upload(files)

    pdf_extract.pdfToImage(progress)
    sleep(2)
    ouput_dir = file_name_utils.OUTPUT_FOLDER  # Replace with the actual folder path you want to zip
    output_zip_file = file_name_utils.OUTPUT_ZIP  # Replace with the desired output zip file name

    zip_folder(ouput_dir, output_zip_file)
    sleep(2)
    results = [os.path.join(ouput_dir, filename) for filename in os.listdir(ouput_dir)]
    results.append(output_zip_file)
    print(results)
    return results

def upload_file_json(files):

    delete_all_tmp()

    copy_cache_to_upload(files)

    json_files = [file for file in os.listdir(file_name_utils.UPLOAD_FOLDER) if file.endswith(".json")]
    # for json_file in json_files:
    #     insert_database.insert_json(json_file)
    sleep(2)

    return "done!"

def upload_file_csv(files):

    delete_all_tmp()

    copy_cache_to_upload(files)

    csv_files = [file for file in os.listdir(file_name_utils.UPLOAD_FOLDER) if file.endswith(".csv")]
    # for csv_file in csv_files:
    #     insert_database.insert_csv(csv_file)
    sleep(2)

    return "done!"

with gr.Blocks() as documentOCR:
    gr.Markdown("Document OCR demo")
    with gr.Tab("File upload"):
        file_output = gr.File()
        upload_button = gr.UploadButton("Click to Upload a File", file_types=[".pdf"], file_count="multiple")
        upload_button.upload(upload_file, upload_button, file_output)
    with gr.Tab("Upload json to insert database"):
        upload_button = gr.UploadButton("Click to Upload a File", file_types=[".json"], file_count="multiple")
        outputs = gr.Label("")
        upload_button.upload(upload_file_json, upload_button, outputs)
    with gr.Tab("Upload csv to Update database"):
        upload_button = gr.UploadButton("Click to Upload a File", file_types=[".csv"], file_count="multiple")
        outputs = gr.Label("")
        upload_button.upload(upload_file_csv, upload_button, outputs)

    with gr.Accordion("Document OCR demo!"):
        gr.Markdown("1. Upload pdf to get json and csv")
        gr.Markdown("2. Upload json or csv to insert database")


documentOCR.queue().launch(share=False, server_name="0.0.0.0")