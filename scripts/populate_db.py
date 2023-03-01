import os
import sys
import django
import csv
from collections import defaultdict

sys.path.append("/home/irina/Keeper/")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Keeper.settings')
django.setup()

from passkeeper.models import *

data_file = '/home/irina/Keeper/scripts/populate_db.csv'
passwords = defaultdict(list)
categories = set()


with open(data_file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    header = csv_reader.__next__()
    for row in csv_reader:        

        categories.add(row[5])
        passwords[row[0]] = row[1:6]


Category.objects.all().delete()
PasItem.objects.all().delete()



categories_rows = {}
passwords_rows = {}

for categr in categories:
    row = Category.objects.create(itemcategory = categr)
    row.save()
    categories_rows[categr] = row
    print(categories_rows[categr])
    print(row)
print(categories_rows)

for password_id, data in passwords.items():
    print (password_id)
    print(data[3])
    print(data[4])
    row = PasItem.objects.create(password_id=password_id, username=data[0],
                              password=data[1], url=data[2],
                              comment=data[3], 
                              pass_category=categories_rows[data[4]]
                              )
    row.save()
    passwords_rows[password_id] = row