import os
from os import listdir, path
from os.path import join
import re
import csv
import json
from paddleocr import PaddleOCR, draw_ocr

# Paddleocr supports Chinese, English, French, German, Korean and Japanese.
# You can set the parameter `lang` as `ch`, `en`, `french`, `german`, `korean`, `japan`
# to switch the language model in order.
ocr = PaddleOCR(debug=False, use_angle_cls=True, lang='en',
                use_gpu=True)  # need to run only once to download and load model into memory


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

    # Thêm thông tin từ info_detail vào tệp JSON
    data = jsonData

    # Lưu vào tệp JSON
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

    # result = result[0]
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

    saveToJsonFirtPage(os.path.join("output", filePDF.replace(".pdf", ".json")), jsonResult)

#
# pathExtract = "firstpageimage"
# for f in listdir(pathExtract):
#     ocrImgFirst(join(pathExtract, f), "1.pdf")
#     break
