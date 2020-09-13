import gspread
import sys
import os

restaurants = []
with open(f'{os.getcwd()}/restaurants.txt', 'r') as file:
    for restaurant in file:
        restaurants.append(restaurant.replace('\n', ''))

gc = gspread.service_account(filename=f'{os.getcwd()}/client_secret.json') # Authenticate Client
gc = gc.open('grubhub-data') # Select grubhub-data file sheet
log = gc.sheet1 # Choose first sheet (log)

# Add First Row
# restaurants.insert(0, 'Time')
# restaurants.insert(0, 'Date of Week')
# restaurants.insert(0, 'Full Date')
# 
# log.append_row(restaurants)
