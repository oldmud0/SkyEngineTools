"""
Generates a table of devices supporting 60 fps in Sky, given:

- A CSV with columns `(name, rating)`
- A CSV with columns `(brand, marketing name, device, model)`, which you can
  find at https://storage.googleapis.com/play_public/supported_devices.csv

The output table is sorted by name, with the internal model in parentheses.
Unrecognized devices appear at the bottom.

Devices supporting 60 fps are assumed to be those with a device rating of
>=10,000.
"""

import argparse
import csv
import sqlite3
import codecs

parser = argparse.ArgumentParser(
    description='Generates a table of devices supporting 60 fps in Sky.'
)

parser.add_argument('rating_table', default='rating_table.csv',
                    help='file containing device ratings')
parser.add_argument('device_table', default='devices.csv',
                    help='file that maps device models to marketing names')

args = parser.parse_args()

con = sqlite3.connect(':memory:')
cur = con.cursor()

cur.execute('CREATE TABLE ratings (brand, model, rating REAL)')
with open(args.rating_table) as csvfile:
    rows = []
    for row in csv.DictReader(csvfile):
        name, rating = row['name'], row['rating']
        try:
            delim = name.index(' ')
            brand, model = name[:delim], name[delim + 1:]
        except ValueError:
            brand, model = name, None
        rows.append((brand, model, rating))
cur.executemany('INSERT INTO ratings (brand, model, rating) VALUES (?, ?, ?)',
                rows)

cur.execute('CREATE TABLE devices (brand, mkt_name, device, model)')
with codecs.open(args.device_table, 'rb', 'utf-16') as csvfile:
    rows = [(row['Retail Branding'],
             ' '.join(row['Marketing Name'].split()),
             row['Device'],
             row['Model'])
            for row in csv.DictReader(csvfile)]
cur.executemany('INSERT INTO devices (brand, mkt_name, device, model) VALUES (?, ?, ?, ?)',
                rows)

cur.execute('''
SELECT
    ratings.brand, ratings.model, ratings.rating,
    devices.brand, devices.model, devices.mkt_name,
    devices.device
FROM ratings
    LEFT OUTER JOIN devices ON
        ratings.brand LIKE devices.brand
        AND ratings.model LIKE devices.model
WHERE rating >= 10000
ORDER BY mkt_name IS NULL, devices.brand, mkt_name;
''')
for row in cur.fetchall():
    brand_orig, model_orig, rating, brand, model, mkt_name, internal_name = row
    if brand is None:
        if model_orig is None:
            # Model may be None if it's a GPU
            name = brand_orig
        elif brand_orig in model_orig:
            name = model_orig
        else:
            name = f'{brand_orig} {model_orig}'
        print(f'{name}')
    else:
        if brand.lower() in mkt_name.lower():
            name = mkt_name
        else:
            name = f'{brand} {mkt_name}'

        if model.lower() in name.lower():
            model = internal_name
        print(f'{name:<30} ({model})')
