import pytesseract


def ocr_screenshot(x1, y1, x2, y2):
    image = ImageGrab.grab().crop([x1, y1, x2, y2])
    image.save("screen.jpg", "JPEG")
    return pytesseract.image_to_string(image)