import cv2
import pytesseract
from source.utility import screen

def output_screen(data):
    return pytesseract.image_to_string(data)

def int_only(x, y, w, h):
    config = '--psm 6 -c tessedit_char_whitelist=0123456789'
    roi = screen.get_screen_roi(x,y,w,h)
    text = pytesseract.image_to_string(roi,config=config)
    return text.strip()  

def str_only(x, y, w, h):
    config = '--psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    roi = screen.get_screen_roi(x,y,w,h)
    text = pytesseract.image_to_string(roi,config=config)
    return text.strip()