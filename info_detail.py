import re


def contains_letters_and_digits(s):
    return any(c.isalpha() for c in s) and any(c.isdigit() for c in s)
def contains_keyword_using_in(string, keyword):
    return keyword in string


def is_dependent_type_in_list(input_string):
    dependent_types_list = ['fathersname', 'mothersname', 'husbandsname', 'wifesname', 'othersname', 'eathersname']
    cleaned_input = input_string.replace("'", "").lower().replace(" ", "")

    return cleaned_input in dependent_types_list

def remove_special_characters(input_string):
    regex_pattern = r'[!@#$%^&*()_+={}\[\]:;"\'|<>,.?/~`-]'

    cleaned_string = re.sub(regex_pattern, '', input_string)

    return cleaned_string
def extract_info_from_ocr(text):
    print(text)
    lines = text.split('\n')

    # Khởi tạo biến lưu trữ thông tin
    info = {
        'id': '',
        'name': '',
        'name2': '',
        'type_name2': '',
        'house_no': '',
        'age': '',
        'sex': '',
        'status': ''
    }
    gender_err = ""
    i = 1
    min_id_length = 9
    if len(lines) > 3:
        if len(lines[0].replace(" - ", "").replace("-", "").replace(" ", "").strip()) > min_id_length and contains_letters_and_digits(lines[0].strip()):
            info['id'] = lines[0].strip()
        elif len(lines[1].replace(" - ", "").replace("-", "").replace(" ", "").strip()) > min_id_length and contains_letters_and_digits(lines[1].strip()):
            info['id'] = lines[1].strip()
            i = 2
        elif (len(lines[2].strip().replace(" - ", "").replace("-", "").replace(" ", "")) > min_id_length and
              (not contains_keyword_using_in(lines[2].strip().lower(), "name"))
                and contains_letters_and_digits(lines[2].strip())):
            info['id'] = lines[2].strip()
            i = 2
        else:
            info['id'] = ""

    while i < len(lines):
        line = lines[i]

        if ":" in line:
            field, value = line.split(":", 1)
            field = field.strip().lower()
            value = value.strip()

            if field == 'name':
                next_line = lines[i + 1].strip() if i + 1 < len(lines) else ''
                while ":" not in next_line and next_line and not is_dependent_type_in_list(next_line):
                    value += " " + next_line
                    i += 1
                    next_line = lines[i + 1].strip() if i + 1 < len(lines) else ''
                value = remove_special_characters(value)
                info['name'] = value.strip()
            elif is_dependent_type_in_list(field):
                next_line = lines[i + 1].strip() if i + 1 < len(lines) else ''
                if ":" in next_line or "House" in next_line or "Number" in next_line:
                    value = remove_special_characters(value)
                    info['name2'] = value.strip()
                else:
                    while ":" not in next_line or not ("House" in next_line or "Number" in next_line):
                        value += " " + next_line
                        i += 1
                        next_line = lines[i + 1].strip() if i + 1 < len(lines) else ''
                    value = remove_special_characters(value)
                    info['name2'] = value.strip()

                type2 = field.split("'s")[0]
                type2 = type2.replace("'s name", "")
                type2 = type2.replace(" s name", "")
                type2 = type2.replace(" sname", "")
                type2 = type2.replace("s name", "")
                info['type_name2'] = type2.strip()


            elif field == 'house number':
                info['house_no'] = "'" + value.split("Gender")[0].strip().split("Age")[0]
                gender_err = value
            elif field == 'age':
                try:
                    info['age'] = value.split('Gender')[0].replace(':', '').replace('(', "").replace('C', "").replace('c', "").strip()
                except:
                    print("Errrrrrrrrrrrrrrr")
                    print(value)
                try:
                    info['sex'] = value.split('Gender')[1].replace(':', '').strip()
                except:
                    print("Errrrrrrrrrrrrrrr")
                    try:
                        gender = gender_err
                        if "Gender" in gender:
                            gender = gender.split('Gender')[1].replace(":", "").strip()
                            info['sex'] = gender
                        elif "gender" in gender:
                            gender = gender.split('gender')[1].replace(":", "").strip()
                            info['sex'] = gender
                    except:
                        print("Errrrrrrrrrrrrrrr")
                    print(value)

        i += 1

    return info

def extract_info_from_ocr_delete(text):
    lines = text.split('\n')

    info = {
        'id': '',
        'name': '',
        'name2': '',
        'type_name2': '',
        'house_no': '',
        'age': '',
        'sex': '',
        'status': "DELETE"
    }

    i = 1
    min_id_length = 9
    if len(lines) > 3:
        if len(lines[0].replace(" - ", "").replace("-", "").replace(" ",
                                                                    "").strip()) > min_id_length and contains_letters_and_digits(
                lines[0].strip()):
            info['id'] = lines[0].strip()
        elif len(lines[1].replace(" - ", "").replace("-", "").replace(" ",
                                                                      "").strip()) > min_id_length and contains_letters_and_digits(
                lines[1].strip()):
            info['id'] = lines[1].strip()
            i = 2
        elif (len(lines[2].strip().replace(" - ", "").replace("-", "").replace(" ", "")) > min_id_length and
              (not contains_keyword_using_in(lines[2].strip().lower(), "name"))
              and contains_letters_and_digits(lines[2].strip())):
            info['id'] = lines[2].strip()
            i = 2
        else:
            info['id'] = ""

    while i < len(lines):
        line = lines[i]

        if ":" in line:
            field, value = line.split(":", 1)
            field = field.strip().lower()
            value = value.strip()

            if field == 'name':
                next_line = lines[i + 1].strip() if i + 1 < len(lines) else ''
                while ":" not in next_line and next_line:
                    value += " " + next_line
                    i += 1
                    next_line = lines[i + 1].strip() if i + 1 < len(lines) else ''
                value = remove_special_characters(value)
                info['name'] = value.strip()

        i += 1

    return info