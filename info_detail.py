def contains_letters_and_digits(s):
    return any(c.isalpha() for c in s) and any(c.isdigit() for c in s)
def contains_keyword_using_in(string, keyword):
    return keyword in string

def extract_info_from_ocr(text):
    lines = text.split('\n')

    # Khởi tạo biến lưu trữ thông tin
    info = {
        'id': '',
        'name': '',
        'name2': '',
        'type_name2': '',
        'house_no': '',
        'age': '',
        'sex': ''
    }

    dependent_types = ["father's name", "mother's name", "husband's name", "wife's name", "other's name",
                       "fathers name", "mothers name", "husbands name", "wifes name", "others name"]

    i = 1
    if len(lines) > 3:
        if len(lines[0].strip()) > 7 and contains_letters_and_digits(lines[0].strip()):
            info['id'] = lines[0].strip()
        elif len(lines[1].strip()) > 7 and contains_letters_and_digits(lines[1].strip()):
            info['id'] = lines[1].strip()
            i = 2
        elif (len(lines[2].strip()) > 7 and
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

                info['name'] = value.strip()
            elif field in dependent_types:
                next_line = lines[i + 1].strip() if i + 1 < len(lines) else ''
                if ":" in next_line:
                    info['name2'] = value.strip()
                else:
                    while ":" not in next_line and next_line:
                        value += " " + next_line
                        i += 1
                        next_line = lines[i + 1].strip() if i + 1 < len(lines) else ''
                    info['name2'] = value.strip()


                info['type_name2'] = field.split("'s")[0]


            elif field == 'house number':
                info['house_no'] = "'" + value
            elif field == 'age':
                try:
                    info['age'] = value.split('Gender')[0].replace(':', '').strip()
                except:
                    print("Errrrrrrrrrrrrrrr")
                    print(value)
                try:
                    info['sex'] = value.split('Gender')[1].replace(':', '').strip()
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
        'sex': ''
    }

    i = 1
    if len(lines) > 3:
        if len(lines[0].strip()) > 7 and contains_letters_and_digits(lines[0].strip()):
            info['id'] = lines[0].strip()
        elif len(lines[1].strip()) > 7 and contains_letters_and_digits(lines[1].strip()):
            info['id'] = lines[1].strip()
            i = 2
        elif (len(lines[2].strip()) > 7 and
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

                info['name'] = value.strip()

        i += 1

    return info