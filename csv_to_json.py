#!/usr/bin/env python
import click
import csv
import geocoder
import geojson
import os
import time
import webbrowser
from jinja2 import Environment, PackageLoader

def make_point(name, data, address):
    g = geocoder.bing(address)
    point = geojson.Point((g.lng, g.lat))
    feature = geojson.Feature(geometry=point, properties={'name': name,
                                                          'data': data,
                                                          'location': address})
    return feature

@click.command()
@click.argument('f', type=click.File('rU'))
def convert(f):
    click.echo('Opening csv and getting locations.')
    features = []
    failures = []

    # open the csv and create features for each person
    reader = csv.reader(f)
    countrows = 0
    for row in reader:
        countrows += 1

    f.seek(0)

    row = reader.next()
    cols = []
    count = 0
    click.echo("Columns found in first row:")
    for col in row:
        cols.append(count)
        click.echo("  Column {count}: {col}".format(count=count, col=col))
        count += 1

    header = click.confirm('Is this a header row?', default=False)
    if header:
        row = reader.next()
        for col in cols:
            click.echo('  {col}: {value}'.format(col=col, value=row[col]))

    while True:
        name_col = click.prompt('Enter the column number for Name', type=int)
        if name_col in cols:
            cols.remove(name_col)
            break
        click.echo('Please choose a column number from:')
        for col in cols:
            click.echo('  {col}: {value}'.format(col=col, value=row[col]))

    # Now to figure out the address
    address_split = click.confirm('Is the address split into two columns?')
    if address_split:
        while True:
            address1_col = click.prompt('Enter the column number for the first part of the address', type=int)
            if address1_col in cols:
                cols.remove(address1_col)
                break
            click.echo('Please choose a column number from:')
            for col in cols:
                click.echo('  {col}: {value}'.format(col=col, value=row[col]))
        while True:
            address2_col = click.prompt('Enter the column number for the second part of the address', type=int)
            if address2_col in cols:
                cols.remove(address2_col)
                break
            click.echo('Please choose a column number from:')
            for col in cols:
                click.echo('  {col}: {value}'.format(col=col, value=row[col]))
    else:
        while True:
            address_col = click.prompt('Enter the column number for the address', type=int)
            if address_col in cols:
                cols.remove(address_col)
                break
            click.echo('Please choose a column number from:')
            for col in cols:
                click.echo('  {col}: {value}'.format(col=col, value=row[col]))




    # Go back to the top of the file
    f.seek(0)
    if header:
        row = reader.next()
    click.echo('')

    with click.progressbar(reader, length=countrows, label='Finding locations') as bar:
        for row in bar:
            name = row[name_col]
            data = {'test': 'data'}
            if address_split:
                address = row[address1_col] + ', ' + row[address2_col]
            else:
                address = row[address_col]
            try:
                features.append(make_point(name, data, address))
            except ValueError:
                failures.append(name)
            time.sleep(.2)

    if len(failures) > 0:
        click.echo('')
        click.echo(click.style('Failed to retrieve locations for:', fg='red'))
        for fail in failures:
            click.echo('  ' + fail)
        click.echo('')
        time.sleep(3)

    # create a geojson feature collection
    fc = geojson.FeatureCollection(features)

    if not os.path.exists('proof_locate'):
        os.makedirs('proof_locate')

    # write geojson string straight into the index file
    env = Environment(loader=PackageLoader('csv_to_json', 'templates'))
    index = env.get_template('index.html')
    with click.open_file('proof_locate/index.html', 'w') as f:
        index.stream(j_geojson=fc, failures=failures).dump(f)
    google = env.get_template('Google.js')
    with click.open_file('proof_locate/Google.js', 'w') as f:
        google.stream().dump(f)

    click.launch('proof_locate/index.html')
    click.echo("If a browser didn't open open index.html to view locations.")

if __name__ == '__main__':
    convert()
