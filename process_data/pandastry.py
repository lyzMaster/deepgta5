# import pandas as pd
#
# name = "liangyuzh3"
# raw_data = [[0,1,0,0,0,0,1]]
# data = {"name":name, "data":raw_data}
# table = pd.DataFrame('/Users/lyz/Desktop/data.csv')
# table.insert(2,"name",data)

import csv
with open('/Users/lyz/Desktop/data.csv', 'a', newline='') as csvfile:
    fieldnames = ['name', 'data']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    # writer.writeheader()
    writer.writerow({'name': '233', 'data': [0,0,0,0,1,1,1]})
