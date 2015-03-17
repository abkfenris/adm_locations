#!/usr/bin/env python
import click
import csv
import geocoder
import geojson
import os
import time
import webbrowser
from jinja2 import Environment, PackageLoader

def make_point(name, status, town, state):
    g = geocoder.bing(town + ', ' + state)
    point = geojson.Point((g.lng, g.lat))
    feature = geojson.Feature(geometry=point, properties={'name': name,
                                                          'status': status,
                                                          'location': town + ', ' + state})
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
    click.echo('')

    with click.progressbar(reader, length=countrows, label='Finding locations') as bar:
        for row in bar:
            name = row[5]
            status = row[10]
            town = row[6]
            state = row[7]
            try:
                features.append(make_point(name, status, town, state))
            except ValueError:
                failures.append(name)
            time.sleep(.2)

    if len(failures) > 0:
        click.echo('')
        click.echo(click.style('Failed to retrieve locations for:', fg='red'))
        for fail in failures:
            click.echo('  ' + fail)
        click.echo('')

    # create a geojson feature collection
    fc = geojson.FeatureCollection(features)

    if not os.path.exists('proof_locate'):
        os.makedirs('proof_locate')

    # write geojson string straight into the index file
    env = Environment(loader=PackageLoader('csv_to_json', 'templates'))
    index = env.get_template('index.html')
    with click.open_file('proof_locate/index.html', 'w') as f:
        index.stream(j_geojson=fc).dump(f)
    google = env.get_template('Google.js')
    with click.open_file('proof_locate/Google.js', 'w') as f:
        google.stream().dump(f)

    click.launch('proof_locate/index.html')
    click.echo("If a browser didn't open open index.html to view locations.")

if __name__ == '__main__':
    convert()
