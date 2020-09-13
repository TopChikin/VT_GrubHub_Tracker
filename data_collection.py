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
import re

# Constants
X = 3072
Y = 1920

ahk = AHK()
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'  # Path to Tesseract

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
    # name = "".join(filter(str.isalnum, name))
    # image.save(f"screenshots/screenshot-{name}.jpg", "JPEG")
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
    while pyautogui.locateCenterOnScreen(path, confidence=0.9) is None:
        print(f"Couldn't find {img_name}")
        sleep(interval)
        if loops_until_timeout <= 0:
            # TODO: fix memory leak
            print("Timed out. Restarting")
            # os.system(r'python "C:\Users\jonat\PycharmProjects\VT_GrubHub\data_collection.py"')
            sys.exit(1)
        loops_until_timeout -= 1
    print('found')


# clicks on a specified image
def click_on_image(img_name, region=(0, 0, X, Y)):
    path = f'{os.getcwd()}/Images/{img_name}.png'
    pos = pyautogui.locateCenterOnScreen(path, confidence=0.9, region=region)
    if pos is None:
        return False
    x, y = pos
    ahk.mouse_move(x, y)
    sleep(0.25)
    ahk.click(x, y)
    return True


# Move One Item Down
def move_one_item(num_items=1):
    for i in range(num_items):
        ahk.mouse_move(X / 2, Y / 2)
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
sleep(1)
bluestacks.activate()
bluestacks.maximize()
sleep(1)
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

wait_for_image('vtCampus')

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

remaining_rests = get_restaurant_names()

wait_time_data = {}
amount_data = {}

print(remaining_rests)

while remaining_rests:
    completed_items = []
    for rest in remaining_rests:
        if click_on_image(rest, region=(1040, 80, 2040-1040, 1830-80)):
            # collect data
            wait_for_color(1500, 260, '0x60B3FF')
            text = ocr_screenshot(1045, 560, 2000, 610)
            print(f'found data - {rest} - {text}')

            # filter data and insert into data dictionaries
            wait_time_match = re.search(r"([0-9]+)[\s]?min",text)
            if wait_time_match is not None:
                wait_time = int(wait_time_match.group(1))
                wait_time_data[rest] = wait_time
            else:
                wait_time_data[rest] = 'N/A'

            amount_waiting_match = re.search(r'([0-9]+)[\s]?in', text)
            if amount_waiting_match is not None:
                amount_waiting = int(amount_waiting_match.group(1))
                amount_data[rest] = amount_waiting
            else:
                amount_data[rest] = 'N/A'

            click_on_image('back')
            sleep(0.25)
            click_on_image('vtCampus_White') # TODO Fix "Where the...? Our locator thing couldn't find any restaurants for you. Please try again"
            sleep(0.5)

            completed_items.append(rest)
        else:
            print(f'couldn\'t find - {rest}')

    for item in completed_items:
        remaining_rests.remove(item)
    if len(completed_items)==0:
        print('yo wtf i found nothing')
        # print(f'there were {len(completed_items)} items left at the end of data collection')
        # break
    print()
    move_one_item(1)

# Set First 3 Rows to Time
t = dt.datetime.now()
min = str((int(t.strftime('%M')) // 15) * 15)
if min == '0':
    min = '00'
new_line_row = [t.strftime('%m-%d-%Y'), t.strftime('%T'), t.strftime('%a'), t.strftime('%H:') + min]
new_waiting_row = [t.strftime('%m-%d-%Y'), t.strftime('%T'), t.strftime('%a'), t.strftime('%H:') + min]

# Add Restaurant Data to new_row
r_list = get_restaurant_names()
for restaurant in r_list:
    new_line_row.append(amount_data[restaurant])

for restaurant in r_list:
    new_waiting_row.append(wait_time_data[restaurant])

print(new_line_row)

# Connect to Google Sheets API
gc = gspread.service_account(filename=f'{os.getcwd()}/client_secret.json') # Authenticate Client
gc = gc.open('grubhub-data') # Select grubhub-data file sheet
amount_in_line_log = gc.get_worksheet(0) # Get amount in line log
waiting_time_log = gc.get_worksheet(1) # Get waiting time log

amount_in_line_log.append_row(new_line_row)
waiting_time_log.append_row(new_waiting_row)

# sys.exit(0)
subprocess.run(r'kill_bluestacks.bat') #Assassinate Bluestacks