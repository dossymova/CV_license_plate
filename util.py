import easyocr

reader = easyocr.Reader(['en'], gpu=True)

dict_char_to_int = {'O': '0',
                    'I': '1',
                    'J': '3',
                    'A': '4',
                    'G': '6',
                    'S': '5'}

dict_int_to_char = {'0': 'O',
                    '1': 'I',
                    '3': 'J',
                    '4': 'A',
                    '6': 'G',
                    '5': 'S'}

def dcti(text: str):
    res = ""
    for i in text:
        if i in dict_char_to_int:
            res += dict_char_to_int[i]
        else: res += i
    return res

def ditc(text: str):
    res = ""
    for i in text:
        if i in dict_int_to_char:
            res += dict_int_to_char[i]
        else: res += i
    return res

def check_format_text(text: str):
    _text = text.replace(",", "").replace("|", "").replace(".", "")
    if len(_text) == 10:
        return 'rect'
    return None

def read_license_plate(license_plate_crop):
    detections = reader.readtext(license_plate_crop)
    text = [None, None, None, None]
    res = ''
    score = 0
    for detection in detections:
        bbox, _text, score = detection
        _text = str(_text)
        _text = _text.upper().replace(' ', '')
        res += _text.upper()
        if _text.lower() == 'kz':
            text[0] = _text.upper()
    
    if text[0] == 'KZ':
        if not res[5:7].isnumeric():
            res = res.replace('KZ', '')
            text[1] = dcti(res[:3])
            text[2] = ditc(res[3:6])
            text[3] = dcti(res[6:])
        else:
            res = res.replace('KZ', '')
            text[1] = dcti(res[:3])
            text[3] = dcti(res[3:5])
            text[2] = ditc(res[5:])
        return text, score
    return None, None

def get_car(license_plate, vehicle_track_ids):
    x1, y1, x2, y2, score, class_id = license_plate

    found = False
    for j in range(len(vehicle_track_ids)):
        xcar1, ycar1, xcar2, ycar2, car_id = vehicle_track_ids[j]
        if x1 > xcar1 and y1 > ycar1 and x2 < xcar2 and y2 < ycar2:
            car_index = j
            found = True
            break
    
    if found:
        return vehicle_track_ids[car_index]

    return -1, -1, -1, -1, -1