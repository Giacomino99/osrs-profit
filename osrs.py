import requests
import json
import sys
import time
import os

HEADER = {'user-agent' : 'OSRS Profit Calculator, Giacomino#6416'}
API_URL = 'http://prices.runescape.wiki/api/v1/osrs'

def download_data(updateMap = False):
    latest_data = requests.get(API_URL+'/latest', headers = HEADER)
    with open('latest.json', 'w') as latest_file:
        json.dump(latest_data.json(), latest_file)

    if updateMap:
        mapping_data = requests.get(API_URL+'/mapping', headers = HEADER)
        with open('mapping.json', 'w') as mapping_file:
            json.dump(mapping_data.json(), mapping_file)

def main():
    download_data(updateMap = False)

if __name__ == '__main__':
    main()