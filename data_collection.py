import os
import sys
import subprocess
from time import sleep
from ahk import AHK
from PIL import Image, ImageGrab
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract' # Path to Tesseract

def ocr_screenshot(x1, y1, x2, y2): # Crop Image & Convert to String
    image = ImageGrab.grab().crop([x1, y1, x2, y2])
    name = pytesseract.image_to_string(image)
    name = "".join(filter(str.isalnum, name))
    image.save(f"screenshots/screenshot-{name}.jpg", "JPEG")
    return name

def timeout_check_color(x, y, color, timeout=15, time=0.25):
    time_check = timeout / time
    while not ahk.pixel_get_color(x, y) == color:
        sleep(time)
        if time_check <= 0:
            os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)
            sys.exit(1)
            return False
        time_check -= 1
    return True

# Constants
X = 3072
Y = 1920
SCROLL_COUNT = 21

ahk = AHK()

# Open Bluestacks if not already open
if ahk.find_window(title=b'BlueStacks'):
    print('BlueStacks Already Running')
    subprocess.run('kill_bluestacks.bat')
    sleep(2)

subprocess.run('run_bluestacks.bat') #Give birth to Bluestacks
print('Running BlueStacks')

sleep(2)

# Find Bluestacks and Maximize it
bluestacks = ahk.find_window(title=b'BlueStacks')
bluestacks.activate()
# bluestacks.maximize()
bluestacks.maximize()

timeout_check_color(1550, 170, '0x20233A')

bluestacks.click(175, 165) #Click on 'My Games'
sleep(0.50)
bluestacks.click(365, 390) #Open GrubHub

sleep(3)

timeout_check_color(700, 800, '0x000000')

sleep(1)

# Scroll Up & Refresh
ahk.mouse_move(X / 2, Y / 2)
for i in range(7):
    ahk.mouse_wheel('up')
    sleep(0.25)

sleep(1.5)

# Scroll Down Slightly to Accomodate Art Design @ Top
ahk.mouse_move(X / 2, Y / 2)
ahk.mouse_drag(x = 0, y = -200, speed=15, relative=True)
sleep(0.5)

# Move one item down
def move_one_item(num_items=1):
    for i in range(num_items):
        ahk.mouse_move(X / 2, Y / 2)
        ahk.mouse_drag(x=0, y=-137, speed=15, relative=True)
        sleep(0.50)

if ahk.image_search(r'C:\Users\jonat\PycharmProjects\VT_GrubHub\Images\your_favorites.png', color_variation=1):
    print('I SEE IT')

else:
    print('I DONT SEE IT :\'(')

# Begin Collecting Vood
for c in range(SCROLL_COUNT):
    sleep(0.5)
    ahk.click(X / 2, 260) # Click on Restuaurant
    # ahk.mouse_drag(X / 2, 260)

    timeout_check_color(1775, 210, '0x489FFF')

    print(ocr_screenshot(1065, 330, 1700, 365))

    sleep(0.25)
    ahk.click(1095, 150) #Back out of Restaurant

    sleep(0.5)
    ahk.click(1435, 150) #Refresh

    sleep(1.25)
    move_one_item()

for c in range(12):
    sleep(1.5)
    ahk.mouse_move(X / 2, 260 + (c * 120))
    ahk.click(X / 2, 260 + (c * 120))  # Click on Restuaurant

    timeout_check_color(1775, 210, '0x489FFF')

    print(ocr_screenshot(1065, 330, 1700, 365))

    sleep(0.25)
    ahk.click(1095, 150)  # Back out of Restaurant

    sleep(0.5)
    ahk.click(1435, 150)  # Refresh

sleep(1.5)
ahk.mouse_move(1536, 1685)
ahk.click(1536, 1685)  # Click on Restuaurant

timeout_check_color(1775, 210, '0x489FFF')

print(ocr_screenshot(1065, 330, 1700, 365))

sleep(0.25)
ahk.click(1095, 150)  # Back out of Restaurant

print('W O W')

sleep(2)
subprocess.run(r'kill_bluestacks.bat') #Assassinate Bluestacks




