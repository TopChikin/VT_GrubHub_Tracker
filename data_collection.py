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
import datetime as dt

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
        names.append(line.replace('\n', ''))
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
    path = f'{os.getcwd()}/Images/{img_name}.png'
    loops_until_timeout = timeout / interval
    while ahk.image_search(path) is None:
        print(f"couldn't find {img_name}")
        sleep(interval)
        if loops_until_timeout <= 0:
            # TODO: fix memory leak
            print("Timed out. Restarting")
            # os.system(r'python "C:\Users\jonat\PycharmProjects\VT_GrubHub\data_collection.py"')
            sys.exit(1)
        loops_until_timeout -= 1
    print('found')


# clicks on a specified image
def click_on_image(img_name, upper_bound=(0,0), lower_bound=(X,Y), region=(0, 0, X, Y)):
    path = f'{os.getcwd()}/Images/{img_name}.png'
    # print(path)
    pos = pyautogui.locateCenterOnScreen(path, confidence=0.9, region=region)
    # pos = ahk.image_search(path, color_variation=20, upper_bound=upper_bound, lower_bound=lower_bound)
    if pos is None:
        return False
    x, y = pos
    ahk.mouse_move(x, y)
    sleep(0.25)
    ahk.click(x, y)
    return True

def move_one_item(num_items=1):
    for i in range(num_items):
        ahk.mouse_move(X / 2, Y / 2)
# Move one item down
        ahk.mouse_drag(x=0, y=(-137 / Y) * Y, speed=15, relative=True)
        sleep(0.50)

# if ahk.find_window(title=b'VT_GrubHub - data_collection.py'):
#     print('minimizing pycharm')
#     ahk.find_window(title=b'VT_GrubHub - data_collection.py').minimize()

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
bluestacks.minimize()
bluestacks.maximize()

print('waiting for mygames')
wait_for_image('myGames')

print('clicking on mygames')
click_on_image('myGames')

print('waiting for grubhub')
wait_for_image('grubhub')

print('clicking on grubhub')
click_on_image('grubhub')

# wait_for_image('vtCampus')

sleep(3)

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

# Connect to Google Sheets API
gc = gspread.service_account(filename=f'{os.getcwd()}/client_secret.json') # Authenticate Client
gc = gc.open('grubhub-data') # Select grubhub-data file sheet
log = gc.sheet1 # Choose first sheet (log)

remaining_rests = get_restaurant_names()

rest_data = {}

print(remaining_rests)

while remaining_rests:
    completed_items = []
    for i, rest in enumerate(remaining_rests):
        if click_on_image(rest, region=(1040, 80, 2040-1040, 1830-80)):
            # collect data
            wait_for_color(1500, 260, '0x60B3FF')
            text = ocr_screenshot(1045, 560, 2000, 610)
            print(f'found data - {rest} - {text}')
            amount_waiting = text # scan data and put it into this var
            rest_data[rest] = amount_waiting

            click_on_image('back', upper_bound=(1040, 80), lower_bound=(2040, 1830))
            sleep(0.25)
            click_on_image('vtCampus_White', upper_bound=(1040, 80), lower_bound=(2040, 1830))
            sleep(0.5)

            completed_items.append(rest)
        else:
            print(f'couldn\'t find - {rest}')

    for item in completed_items:
        remaining_rests.remove(item)
    if len(completed_items)==0:
        print('yo wtf i found nothing')
    print()
    move_one_item(1)

# Set First 3 Rows to Time
t = dt.datetime.now()
new_row = [t.strftime("%a"), t.strftime("%Y-%m-%d"), t.strftime("%H:%M")]

# Add Restaurant Data to new_row
r_list = get_restaurant_names()
for restaurant in r_list:
    new_row.append(rest_data[restaurant])

print(new_row)

sys.exit(0)

subprocess.run(r'kill_bluestacks.bat') #Assassinate Bluestacks




