#!/usr/bin/env python
import click
import csv
import geocoder
import geojson
import os
import time
import webbrowser
from jinja2 import Environment, FileSystemLoader

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
    print 'Opening csv and getting locations'
    features = []
    failures = []

    # open the csv and create features for each person
    reader = csv.reader(f)
    countrows = 0
    for row in reader:
        countrows += 1

    f.seek(0)
    print 'This should take about', str(countrows*.2), 'seconds to retrieve locations.'

    for row in reader:
        name = row[5]
        status = row[0]
        town = row[6]
        state = row[7]
        try:
            features.append(make_point(name, status, town, state))
        except ValueError:
            failures.append(name)
        # pause so we don't get banned by Google for updating too often
        time.sleep(.2)

    if len(failures) > 0:
        print 'failed on:'
        for fail in failures:
            print fail

    # create a geojson feature collection
    fc = geojson.FeatureCollection(features)

    # write geojson string straight into the index file
    env = Environment(loader=FileSystemLoader('templates'))
    index = env.get_template('index.html')
    with open('index.html', 'wb') as f:
        index.stream(j_geojson=fc).dump('index.html')

    os.system('open index.html')
    print 'Now open index.html to view locations'

if __name__ == '__main__':
    convert()
