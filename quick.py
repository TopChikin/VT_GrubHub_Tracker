import gspread
import sys
import os

restaurants = []
with open(f'{os.getcwd()}/restaurants.txt', 'r') as file:
    for restaurant in file:
        restaurants.append(restaurant.replace('\n', ''))

gc = gspread.service_account(filename=f'{os.getcwd()}/client_secret.json') # Authenticate Client
gc = gc.open('grubhub-data') # Select grubhub-data file sheet
waiting_time_log = gc.get_worksheet(1)
amount_in_line = gc.get_worksheet(0)


# Add First Row
# restaurants.insert(0, 'Time')
# restaurants.insert(0, 'Date of Week')
# restaurants.insert(0, 'Full Time')
# restaurants.insert(0, 'Full Date')
#
# waiting_time_log.append_row(restaurants)
# amount_in_line.append_row(restaurants)
