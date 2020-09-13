import os
import subprocess
from time import sleep
import datetime as dt
from ahk import AHK

ahk = AHK()

def get_time():
    return dt.datetime.now()

# Get Current Interval
def get_time_interval():
    t = dt.datetime.now()
    return (int(t.strftime('%M')) // 15) * 15


def collect_data():
    if not ahk.find_window(title=b'BlueStacks'):
        subprocess.Popen('collect_data.bat')

def collection_loop(check_interval=180):
    print('Beginning collection loop')
    current_time = get_time_interval()
    collect_data()

    while True:
        sleep(check_interval)

        if  get_time_interval() != current_time:
            print(f'[{get_time()}] Checking Interval - Ready: Beginning Collection')
            collect_data()
        else:
            print(f'Checking Interval - Not Ready')

collection_loop()
