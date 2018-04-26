import csv

with open('C:\\gta5_console\\keys_data\\keys_data.csv', 'a', newline='') as csvfile:
    fieldnames = ['position', 'data']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writerow({'name': 'Baked', 'data': 'Beans'})

