import os
import sys
import subprocess
from time import sleep
from ahk import AHK
from PIL import Image, ImageGrab
import os
import pytesseract
import pyautogui
import gspread

# Constants
X = 3072
Y = 1920
SCROLL_COUNT = 21

ahk = AHK()
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract' # Path to Tesseract

# print(ahk.image_search(r"C:/Users/jonat/PycharmProjects/VT_GrubHub/Images/testImage.png"))
# print(pyautogui.locateOnScreen(r"C:/Users/jonat/PycharmProjects/VT_GrubHub/Images/testImage.png"))

# sys.exit(0)


# takes a screenshot cropped to the specified area and returns the text tesseract finds

def get_restaurant_names(path=f'{os.getcwd()}/restaurants.txt'):
    names = []
    file = open(path, 'r')
    for line in file:
        names.append([line.replace('\n', '')])
    file.close()
    return names

def ocr_screenshot(x1, y1, x2, y2):
    image = ImageGrab.grab().crop([x1, y1, x2, y2])
    name = pytesseract.image_to_string(image)
    name = "".join(filter(str.isalnum, name))
    image.save(f"screenshots/screenshot-{name}.jpg", "JPEG")
    return name


# waits until a pixel turns the specified color
# restarts program after however many seconds timeout specifies
def wait_for_color(x, y, color, timeout=15, interval=0.25):
    loops_until_timeout = timeout / interval
    while not ahk.pixel_get_color(x, y) == color:
        sleep(interval)
        if loops_until_timeout <= 0:
            bluestacks.kill(1)
            sys.exit(1)
        loops_until_timeout -= 1


# waits for a specified image to appear
# restarts program after however many seconds timeout specifies
def wait_for_image(img_name, timeout=15, interval=.25):
    loops_until_timeout = timeout / interval
    while ahk.image_search(f'{os.getcwd()}/Images/{img_name}.png') is None:
        print('none')
        sleep(interval)
        if loops_until_timeout <= 0:
            # TODO: fix memory leak
            print("Timed out. Restarting")
            # os.system(r'python "C:\Users\jonat\PycharmProjects\VT_GrubHub\data_collection.py"')
            sys.exit(1)
        loops_until_timeout -= 1
    print('found')


# clicks on a specified image
def click_on_image(img_name):
    x, y = ahk.image_search(f'{os.getcwd()}/Images/{img_name}.png')
    if x is None:
        return False
    ahk.move_mouse(x + 2, y + 2)
    ahk.click(x + 2, y + 2)
    return True

# Move one item down
def move_one_item(num_items=1):
    for i in range(num_items):
        ahk.mouse_move(X / 2, Y / 2)
        ahk.mouse_drag(x=0, y=-137, speed=15, relative=True)
        sleep(0.50)


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
bluestacks.maximize()

print('waiting for mygames')
wait_for_image('myGames')

print('clicking on mygames')
click_on_image('myGames')

print('waiting for grubhub')
wait_for_image('grubhub')

# Scroll Up & Refresh
ahk.mouse_move(X / 2, Y / 2)
for i in range(7):
    ahk.mouse_wheel('up')
    sleep(0.25)

sleep(2)

# Scroll Down Slightly to Accomodate Art Design @ Top
ahk.mouse_move(X / 2, Y / 2)
ahk.mouse_drag(x = 0, y = -200, speed=15, relative=True)

sleep(2)

# Begin Collecting Vood


a = dt.datetime.now()
time = a.strftime("%c")

remaining_rests = get_restaurant_names()
r_list = get_restaurant_names()

new_row = [time]

while remaining_rests:
    for i, rest in enumerate(remaining_rests):
        if click_on_image(rest):
            # collect data
            table_data["name"].append(rest)
            table_data["amount_waiting"].append(1)
            

            # insert data into data
            table_data[rest] = "helo"
            del restaurants[i]

sleep(1.5)
ahk.mouse_move(1536, 1685)
ahk.click(1536, 1685)  # Click on Restuaurant

wait_for_color(1775, 210, '0x489FFF')

print(ocr_screenshot(1065, 330, 1700, 365))

sleep(0.25)
ahk.click(1095, 150)  # Back out of Restaurant

print('W O W')

sleep(2)
subprocess.run(r'kill_bluestacks.bat') #Assassinate Bluestacks




