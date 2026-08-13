import cv2
import pytesseract
import source.utility.screen as screen

def int_only(x, y, w, h):
    config = '--psm 6 -c tessedit_char_whitelist=0123456789'
    roi = screen.get_screen_roi(x,y,w,h)
    text = pytesseract.image_to_string(roi,config=config)
    text = text.strip()
    if not text:
        return None

    return int(text)

def str_only(x, y, w, h):
    config = '--psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    roi = screen.get_screen_roi(x,y,w,h)
    text = pytesseract.image_to_string(roi,config=config)
    return text.strip()  

def int_only_roi(roi,x, y, w, h):
    config = '--psm 6 -c tessedit_char_whitelist=0123456789'
    cropped = roi[y:y + h, x:x + w]
    text = pytesseract.image_to_string(cropped,config=config)
    text = text.strip()
    if not text:
        return None

    return int(text)
def output_screen(data):
    return pytesseract.image_to_string(data)

