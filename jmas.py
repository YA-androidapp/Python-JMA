#!/usr/bin/python3
# -*- coding: utf-8 -*-
from collections import OrderedDict
from datetime import datetime
import json
import os
import requests
import sys

from const import JMA_AREA, JMA_ICON_BASEURL, JMA_ICONS, JMA_JSON_BASEURL, JMA_TELOPS


RESULT_FILE_PATH = 'result_pref.txt'


def format_date(dt):
    return datetime.strftime(
        datetime.strptime(
            dt,
            '%Y-%m-%dT%H:%M:%S%z'
        ),
        '%m/%d'
    )


def preparation():
    if os.path.isfile(RESULT_FILE_PATH):
        os.remove(RESULT_FILE_PATH)


def main():
    # with open(RESULT_FILE_PATH, encoding='utf-8', mode='a') as f:
    for i, area_id in enumerate(JMA_AREA.keys()):
        # print('area_id', area_id, JMA_AREA[area_id])
        get_pref(area_id, i)
        # f.write(area_id)


def get_pref(area_id, i):
    response = requests.get(JMA_JSON_BASEURL + area_id + '.json')

    if response.status_code != 200:
        sys.exit()

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
                        print('area_publishing_office', area_publishing_office)

                area_name_te = []
                area_name_wc = []
                temps_max = []
                temps_min = []
                weather_icons = []
                weather_telops = []

                for area in ts['areas']:
                    if 'weatherCodes' in area:
                        area_name_wc = area['area']['name']
                        print('area_name_wc', area_name_wc)

                        weather_telops = [JMA_TELOPS[n] for n in area['weatherCodes']]
                        print('weather_telops', ' '.join(weather_telops))

                        weather_icons = [JMA_ICON_BASEURL + JMA_ICONS[n]['day'] for n in area['weatherCodes']]
                        print('weather_icons', ' '.join(weather_icons))

                    if 'tempsMax' in area:
                        area_name_te = area['area']['name']
                        print('area_name_te', area_name_te)

                        temps_max = [n if n != '' else '-' for n in area['tempsMax']]
                        print('temps_max', ' '.join(temps_max))

                    if 'tempsMin' in area:
                        temps_min = [n if n != '' else '-' for n in area['tempsMin']]
                        print('temps_min', ' '.join(temps_min))

                    print('')


if __name__ == '__main__':
    preparation()
    main()
