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
# genes = defaultdict(list)
# sequencing = set()
# ec = set()
# products = defaultdict(dict)
passwords = defaultdict(list)
categories = set()


with open(data_file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    header = csv_reader.__next__()
    for row in csv_reader:        
        #ec.add(row[8])
        #sequencing.add((row[4], row[5]))
        #genes[row[0]] = row[1:4]+row[6:9]
        categories.add(row[5])
        passwords[row[0]] = row[1:6]


Category.objects.all().delete()
PasItem.objects.all().delete()

# ec_rows = {}
# sequencing_rows = {}
# gene_rows = {}

categories_rows = {}
passwords_rows = {}

# for entry in ec:
#     row = EC.objects.create(ec_name=entry)
#     row.save()
#     ec_rows[entry] = row

# for seq_centre in sequencing:
#     row = Sequencing.objects.create(sequencing_factory=seq_centre[0], factory_location=seq_centre[1])
#     row.save()
#     sequencing_rows[seq_centre[0]] = row

# for gene_id, data in genes.items():
#     row = Gene.objects.create(gene_id=gene_id, entity=data[0],
#                               start=data[1], stop=data[2],
#                               sense=data[3], start_codon=data[4],
#                               sequencing=sequencing_rows['Sanger'],
#                               ec=ec_rows[data[5]])
#     row.save()
#     gene_rows[gene_id] = row
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