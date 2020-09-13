import os
import subprocess
import gspread
from time import sleep
import datetime as dt
from ahk import AHK

t = dt.datetime.now()
ahk = AHK()

gc = gspread.service_account(filename=f'{os.getcwd()}\\client_secret.json')  # Authenticate Client
gc = gc.open('grubhub-data')  # Select grubhub-data file sheet
amount_in_line = gc.get_worksheet(0)


# From Google Sheets API, get last TIME that we collected data in terms of the time interval

def get_last_time_interval():
    # Get Last Cell of Column D and Shorten Value to Last 2 Digits (00, 15, 30, 45)
    return int(amount_in_line.cell(len(amount_in_line.get_all_values()), 4).value[-2:])


# From Google Sheets API, get last DATE that we collected data
def get_last_date():
    return str(amount_in_line.cell(len(amount_in_line.get_all_values()), 1).value)


# Get Date
def get_date():
    return t.strftime(r'%m-%d-%Y')


# Get Current Time
def get_time():
    return t.strftime(r'%m-%d-%Y_%T')


# Get Current Interval
def get_time_interval():
    return int((int(t.strftime('%M')) // 15) * 15)


# Begin Data Collection Process
def collect_data():
    if not ahk.find_window(title=b'BlueStacks'):
        subprocess.Popen('collect_data.bat')


# Loop to Collect Data
def collection_loop(check_interval=(3 * 60)):

    last_time = get_last_time_interval()  # Get Last Time Interval to Check

    while True:
        if get_last_date() != get_date():  # If Last Date and Current Date are not the same
            print(f'[{get_time()}] Date Mismatch - Collecting Data')
            collect_data()
            last_time = get_time_interval()
        elif get_time_interval() != last_time:  # If Last Time Interval is not equal to current Time Interval
            print(f'[{get_time()}] Checking Interval - Ready: Beginning Collection')
            collect_data()
            last_time = get_time_interval()
        else:
            print(f'[{get_time()}] Checking Interval - Not Ready')

        sleep(check_interval)  # Wait Check Interval to Prevent Excessive Checking
        # sleep(1)


collection_loop()  # Run Collection L
