import os

from paddleocr import PaddleOCR
from os import listdir, path
from os.path import join
import re
import csv
import json

import file_name_utils
import info_detail

# Paddleocr supports Chinese, English, French, German, Korean and Japanese.
# You can set the parameter `lang` as `ch`, `en`, `french`, `german`, `korean`, `japan`
# to switch the language model in order.
ocr = PaddleOCR(debug=False, use_angle_cls=True, lang='en',
                use_gpu=True) # need to run only once to download and load model into memory


def save_to_csv_and_json(info_detail, page, path, file_name_csv, file_name_json):

    csv_header = ["page", "id", "name", "name2", "type_name2", "house_no", "age", "sex", "status"]

    csv_file_path = os.path.join(path, file_name_csv)
    json_file_path = os.path.join(path, file_name_json)

    with open(csv_file_path, "a", newline="") as csvfile:
        csv_writer = csv.DictWriter(csvfile, fieldnames=csv_header)

        if csvfile.tell() == 0:
            csv_writer.writeheader()

        csv_writer.writerow({"page": page + 1, **info_detail})

    # Đọc tệp JSON (nếu đã tồn tại)
    try:
        with open(json_file_path, "r") as jsonfile:
            data = json.load(jsonfile)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {"electorate": []}

    # Thêm thông tin từ info_detail vào tệp JSON
    data["electorate"].append(info_detail)

    # Lưu vào tệp JSON
    with open(json_file_path, "w") as jsonfile:
        json.dump(data, jsonfile, indent=4)

def txt_vald_append(text):
    valid_array = ["Photo is", "Available",
                   "photois", "available"]
    cleaned_input = text.replace("'", "").replace(" ", "").lower()
    if cleaned_input in valid_array:
        return False
    if text.strip() in valid_array:
        return False
    return True

def replace_txts(text):
    text = text.replace("House Number : \n", "House Number : ").replace("Age : \n", "Age : ").replace("\n Gender", "Gender").replace("Gender : \n", "Gender : ")
    text = text.replace("House Number :\n", "House Number : ").replace("Age:\n", "Age : ").replace("\nGender", " Gender").replace("Gender :\n", "Gender : ")
    text = text.replace("House Number: \n", "House Number: ").replace("Age: \n", "Age: ").replace("Gender :\n", "Gender :")
    text = text.replace("House Number:\n", "House Number : ").replace("Age:\n", "Age : ").replace("Gender:\n", "Gender :")
    text = text.replace("House Number\n", "House Number : ").replace("Age\n", "Age : ").replace("Gender\n", "Gender :")
    return text

def format_age_gender(input_string):
    regex_pattern = r'Age(\d+)Gender'

    formatted_string = re.sub(regex_pattern, r'Age : \1 Gender', input_string)

    return formatted_string

def ocrImg(img_path, pathOutput, pdf_file, page_number):
    page = page_number
    csv_file = pdf_file.replace('.pdf', ".csv")
    json_file = pdf_file.replace('.pdf', ".json")
    result = ocr.ocr(img_path, cls=True)

    text = ""

    txts = [line[1][0] for line in result]

    for txt in txts:
        if txt_vald_append(txt):
            if "Age" in txt and "Gender" in txt:
                text = format_age_gender(text)
                text = text + txt + "\n"
            else:
                text = text + txt + "\n"
    text = replace_txts(text)
    infoDetail = info_detail.extract_info_from_ocr(text)
    print(infoDetail)
    save_to_csv_and_json(infoDetail, page, pathOutput, csv_file, json_file)

def ocrImgDelete(img_path, pathOutput, pdf_file, page_number):
    page = page_number
    csv_file = pdf_file.replace('.pdf', ".csv")
    json_file = pdf_file.replace('.pdf', ".json")
    result = ocr.ocr(img_path, cls=True)

    text = ""

    txts = [line[1][0] for line in result]
    for txt in txts:
        if txt_vald_append(txt):
            text = text + txt + "\n"
    text = replace_txts(text)
    infoDetail = info_detail.extract_info_from_ocr_delete(text)
    print(infoDetail)
    save_to_csv_and_json(infoDetail, page, pathOutput, csv_file, json_file)

def create_directory_if_not_exists(path):
    try:
        os.makedirs(path)
        print(f"Folder {path} is created.")
    except FileExistsError:
        print(f"Folder {path} is exists.")

def ocrcardname(pdf_file, page_number):
    pathExtract = "cardimage/detect/crops/cardname"
    pathOutput = "output"
    if os.path.exists(pathExtract):
        for f in listdir(pathExtract):
            create_directory_if_not_exists(pathOutput)
            print(join(pathExtract, f))
            ocrImg(join(pathExtract, f), pathOutput, pdf_file, page_number)

def ocrcardnameDelete(pdf_file, page_number):
    pathExtract = "cardimage/detect/crops/carddelete"
    pathOutput = "output"
    if os.path.exists(pathExtract):
        for f in listdir(pathExtract):
            create_directory_if_not_exists(pathOutput)
            print(join(pathExtract, f))
            ocrImgDelete(join(pathExtract, f), pathOutput, pdf_file, page_number)

def find_index_ignore_case(lst, item):
    lower_item = item.lower()  # Convert the item to lowercase
    indexes = [i for i, x in enumerate(lst) if lower_item in x.lower()]
    return indexes[0]

def saveToJsonFirtPage(json_file_path, jsonData):
    try:
        with open(json_file_path, "r") as jsonfile:
            data = json.load(jsonfile)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {"electorate": []}

    data = jsonData

    with open(json_file_path, "w") as jsonfile:
        json.dump(data, jsonfile, indent=4)

def ocrImgFirst(img_path, filePDF):
    jsonResult = {
        "constituence":
            {
                "name_assembly_c": "",
                "part_no": "",
                "name_parliamentary_c": "",
                "year_revision": "",
                "polling_station_name": "",
                "polling_station_type": "",
                "number_electors": "",
                "starting_no": "",
                "ending_no": "",
                "male": "",
                "female": "",
                "third": "",
                "state": "",
                "police_station": "",
                "revenue_division": "",
                "main_town": "",
                "district": "",
                "mandal": "",
                "pin_code": ""
            },
        "electorate": []
    }
    result = ocr.ocr(img_path, cls=True)

    txts = [line[1][0] for line in result]
    new_list = [item.lower().strip() for item in txts]
    try:
        # name_assembly_c
        jsonResult["constituence"]["name_assembly_c"] = str(txts[1]).split(":")[1].strip()
    except Exception as e:
        jsonResult["constituence"]["name_assembly_c"] = ""

    try:
        # part_no
        jsonResult["constituence"]["part_no"] = txts[new_list.index("part number") + 1]
    except Exception as e:
        jsonResult["constituence"]["part_no"] = ""

    try:
        # name_parliamentary_c
        jsonResult["constituence"]["name_parliamentary_c"] = txts[new_list.index("part number") + 3].split(":")[
            1].strip()
    except Exception as e:
        jsonResult["constituence"]["name_parliamentary_c"] = ""

    try:
        # year_revision
        jsonResult["constituence"]["year_revision"] = txts[new_list.index("year of revision") + 1]
    except Exception as e:
        jsonResult["constituence"]["year_revision"] = ""

    try:
        # polling_station_name
        pollingstation = ""
        for i in range(find_index_ignore_case(new_list, "male/female") + 1,
                       new_list.index("number of auxiliary polling")):
            print(txts[i])
            pollingstation = pollingstation + txts[i].strip().replace("\n", "") + " "
        jsonResult["constituence"]["polling_station_name"] = pollingstation
    except Exception as e:
        jsonResult["constituence"]["polling_station_name"] = ""

    try:
        # polling_station_type
        jsonResult["constituence"]["polling_station_type"] = txts[new_list.index("type of polling station") + 1]
    except Exception as e:
        jsonResult["constituence"]["polling_station_type"] = ""

    try:
        # number_electors
        jsonResult["constituence"]["number_electors"] = txts[new_list.index("total") + 6]
    except Exception as e:
        jsonResult["constituence"]["number_electors"] = ""

    try:
        # starting_no
        jsonResult["constituence"]["starting_no"] = txts[new_list.index("starting") + 9]
    except Exception as e:
        jsonResult["constituence"]["starting_no"] = ""

    try:
        # ending_no
        jsonResult["constituence"]["ending_no"] = txts[new_list.index("ending") + 9]
    except Exception as e:
        jsonResult["constituence"]["ending_no"] = ""

    try:
        # male
        jsonResult["constituence"]["male"] = txts[new_list.index("male") + 6]
    except Exception as e:
        jsonResult["constituence"]["male"] = ""

    try:
        # female
        jsonResult["constituence"]["female"] = txts[new_list.index("female") + 6]
    except Exception as e:
        jsonResult["constituence"]["female"] = ""

    try:
        # third
        jsonResult["constituence"]["third"] = txts[new_list.index("third gender") + 6]
    except Exception as e:
        jsonResult["constituence"]["third"] = ""

    # The following fields are not handled with exception since they are hardcoded:

    # state
    jsonResult["constituence"]["state"] = "S01 Andhra Pradesh"

    try:
        # police_station
        jsonResult["constituence"]["police_station"] = txts[new_list.index("police station") + 1].replace(":", "").strip()
    except Exception as e:
        jsonResult["constituence"]["police_station"] = ""

    try:
        # revenue_division
        jsonResult["constituence"]["revenue_division"] = txts[new_list.index("revenue division") + 1].replace(":", "").strip()
    except Exception as e:
        jsonResult["constituence"]["revenue_division"] = ""

    try:
        # main_town
        jsonResult["constituence"]["main_town"] = txts[new_list.index("main town/village") + 1].replace(":", "").strip()
    except Exception as e:
        jsonResult["constituence"]["main_town"] = ""

    try:
        # district
        jsonResult["constituence"]["district"] = txts[new_list.index("district") + 1].replace(":", "").strip()
    except Exception as e:
        jsonResult["constituence"]["district"] = ""

    try:
        # mandal
        jsonResult["constituence"]["mandal"] = txts[new_list.index("mandal") + 1].replace(":", "").strip()
    except Exception as e:
        jsonResult["constituence"]["mandal"] = ""

    try:
        # pin_code
        jsonResult["constituence"]["pin_code"] = txts[new_list.index("pin code") + 1].replace(":", "").strip()
    except Exception as e:
        jsonResult["constituence"]["pin_code"] = ""
    print(jsonResult)

    saveToJsonFirtPage(os.path.join(file_name_utils.OUTPUT_FOLDER, filePDF.replace(".pdf", ".json")), jsonResult)
