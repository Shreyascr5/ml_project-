import pytesseract
import cv2
import pandas as pd

def parse_image(file_path):
    img = cv2.imread(file_path)
    text = pytesseract.image_to_string(img)

    return pd.DataFrame({
        "Extracted_Text": [text]
    })