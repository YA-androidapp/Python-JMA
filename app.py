#!/usr/bin/python3
# -*- coding: utf-8 -*-
from collections import OrderedDict
from datetime import datetime
from flask import Flask, render_template, request, jsonify
import json
import os
import requests
import sys

from const import JMA_AREA, JMA_ICON_BASEURL, JMA_ICONS, JMA_JSON_BASEURL, JMA_TELOPS


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config["JSON_SORT_KEYS"] = False


def format_date(dt):
    return datetime.strftime(
        datetime.strptime(
            dt,
            '%Y-%m-%dT%H:%M:%S%z'
        ),
        '%m/%d'
    )


@app.route('/')
def main():
    results = ''

    for i, area_id in enumerate(JMA_AREA.keys()):
        results = results + get_pref(area_id, i)

    return render_template('index.html', results=results)


def get_pref(area_id, i):
    result = ''

    response = requests.get(JMA_JSON_BASEURL + area_id + '.json')

    if response.status_code != 200:
        return ''

    data = json.loads(response.text, object_pairs_hook=OrderedDict)

    times = []

    area_publishing_office = ''
    for area in data:
        for ts in area['timeSeries']:
            if len(ts['timeDefines']) == 7:
                if i == 0 and len(times) == 0:
                    times = [format_date(n) for n in ts['timeDefines']]
                    print('times', ' '.join(times), '\n')

                if 'publishingOffice' in area:
                    if area_publishing_office != area['publishingOffice']:
                        area_publishing_office = area['publishingOffice']
                        result = result + '<tr><th colspan=9 class="left">' + area_publishing_office + '</th></tr>'

                area_name_te = []
                area_name_wc = []
                temps_max = []
                temps_min = []
                weather_icons = []
                weather_telops = []

                for area in ts['areas']:
                    if 'weatherCodes' in area:
                        area_name_wc = area['area']['name']

                        weather_telops = [JMA_TELOPS[n] for n in area['weatherCodes']]
                        weather_icons = [JMA_ICON_BASEURL + JMA_ICONS[n]['day'] for n in area['weatherCodes']]

                        result = result + '<tr class="row-wc"><td class="left white-bg"></td><td>' + area_name_wc + '</td><td><img src="' + '"></td><td><img src="'.join(weather_icons) + '"></td></tr>'

                    if 'tempsMax' in area:
                        area_name_te = area['area']['name']

                        temps = ['<span class="temp-' + n + '">' + n + '</span>' if n != '' else '<span class="temp-null">-</span>' for n in area['tempsMax']]

                        result = result + '<tr class="row-te"><td class="left white-bg"></td><td>' + area_name_te + '</td><td class="centering">' + '</td><td class="centering">'.join(temps) + '</td></tr>'

    return result


if __name__ == '__main__':
    app.run(debug=True)
