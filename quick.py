import gspread
import os

restaurants = []
with open(f'{os.getcwd()}/restaurants.txt', 'r'):
    for restaurant in restaurants:
        restaurants.append(restaurant.replace('\n', ''))

print(restaurants)

gc = gspread.service_account(filename=f'{os.getcwd()}/client_secret.json')
log = gc.open()