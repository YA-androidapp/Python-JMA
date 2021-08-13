#!/usr/bin/python3
# -*- coding: utf-8 -*-
from collections import OrderedDict
from datetime import datetime
import json
import os
import requests
import sys

from const import JMA_ICONS, JMA_ICON_BASEURL, JMA_TELOPS

JSON_URL = 'https://www.jma.go.jp/bosai/forecast/data/forecast/010000.json'
RESULT_FILE_PATH = 'result.txt'


def preparation():
    if os.path.isfile(RESULT_FILE_PATH):
        print('REMOVE')
        os.remove(RESULT_FILE_PATH)
    else:
        print('NOT FOUND')


def main():
    # ua = 'Mozilla'
    # headers = {'User-Agent': ua}
    # params = {'city': '010000'}
    # r_ua = requests.get(url, headers=headers, params=params)

    response = requests.get(JSON_URL)
    # print(response.url)
    # print(response.text)
    # print(response.headers)
    # print(response.encoding)
    # print(response.content)

    if response.status_code != 200:
        sys.exit()

    data = json.loads(response.text, object_pairs_hook=OrderedDict)

    with open(RESULT_FILE_PATH, encoding='utf-8', mode='a') as f:

        for area in data:
            area_name = area['name']
            print('[', area_name, ']')

            codes = []
            icons = []
            names_wc = []
            names_te = []
            temps = []

            for ts in area['week']['timeSeries']:
                ts_name = ts['areas']['area']['name']
                print('  [', ts_name, ']')

                times = [n for n in ts['timeDefines']]

                if 'weatherCodes' in ts['areas']:
                    for i,v in enumerate(ts['areas']['weatherCodes']):
                        print(times[i], ':', JMA_TELOPS[v], end=' ')
                        codes.append(
                            JMA_TELOPS[v]
                        )
                        icons.append(
                            JMA_ICON_BASEURL + JMA_ICONS[v].get('day')
                        )
                        names_wc.append(ts_name)
                    print('')
                if 'tempsMax' in ts['areas']:
                    for i,v in enumerate(ts['areas']['tempsMax']):
                        print(ts['areas']['tempsMax'][i], '/', ts['areas']['tempsMin'][i], end=' ')
                        temp_max = ts['areas']['tempsMax'][i] if ts['areas']['tempsMax'][i] != '' else '-'
                        temp_min = ts['areas']['tempsMin'][i] if ts['areas']['tempsMin'][i] != '' else '-'
                        temps.append(
                            temp_max + '/' + temp_min
                        )
                        names_te.append(ts_name)
                    print('')

            if len(codes) > 0 and len(temps) > 0:
                for i in range(len(times)):
                    f.write(
                        area_name +
                        '\t' +
                        names_wc[i] +
                        '\t' +
                        names_te[i] +
                        '\t' +
                        datetime.strftime(
                            datetime.strptime(
                                times[i],
                                '%Y-%m-%dT%H:%M:%S%z'
                            ),
                            '%m/%d'
                        )+
                        '\t' +
                        codes[i]+
                        '\t' +
                        temps[i]+
                        '\t' +
                        icons[i]+
                        '\n'
                    )

                codes = []
                icons = []
                names = []
                temps = []


if __name__ == '__main__':
    preparation()
    main()
