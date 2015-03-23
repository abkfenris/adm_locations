from setuptools import setup

setup(
    name='csv_locate',
    version='0.1',
    py_modules=['csv_to_json'],
    install_requires=[
        'click',
        'colorama',
        'geocoder',
        'geojson',
        'jinja2',
    ],
    entry_points='''
        [console_scripts]
        csv_locate=csv_to_json:convert
    ''',
)
