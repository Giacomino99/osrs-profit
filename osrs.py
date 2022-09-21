import requests
import json
import sys
import time
import os
from dataclasses import dataclass
from pprint import pprint
from terminaltables import AsciiTable, SingleTable

from tables import *

HEADER = {'user-agent' : 'OSRS Profit Calculator, Giacomino#6416'}
API_URL = 'http://prices.runescape.wiki/api/v1/osrs'
'''
name -> item info
id -> price info
'''
@dataclass
class Item:
    name: str
    id: int
    low_alch: int
    high_alch: int
    value: int
    limit: int
    members: bool
    examine: str

@dataclass
class Col:
    header: str = 'Header'
    fmt: callable = lambda x: x

class Table:

    def __init__(self, rows = [], cols = []):
        self.rows = rows
        self.cols = cols
        self.rows_max = 0
        for i in self.rows

    def add_row(self, row):
        self.rows.append(row)

    def add_col(self, col):
        self.cols.append(cols)

    def print_table(self):

@dataclass
class Price:
    id: int
    high: int
    low: int
    high_time: int
    low_time: int

@dataclass
class OSRS_Pricer:

    def __init__(self, mapping_file = 'mapping.json', latest_file = 'latest.json'):
        self.items = {}
        self.latest = {}
        self.mapping_file = mapping_file
        self.latest_file = latest_file

    def download_data(self, updateMap = False):
        '''Downloads data from the OSRS Wiki API
        Latest is the latest prices
        Mapping is the itemID -> itemName mappings'''
        
        latest_data = requests.get(API_URL+'/latest', headers = HEADER)
        with open(self.latest_file, 'w') as lf:
            json.dump(latest_data.json(), lf)

        if updateMap:
            mapping_data = requests.get(API_URL+'/mapping', headers = HEADER)
            with open(self.mapping_file, 'w') as mf:
                json.dump(mapping_data.json(), mf)

    def load_data(self):
        with open(self.mapping_file) as mf:
            item_map = json.load(mf)
            for i in item_map:
                self.items[i['name'].upper()] = Item(i['name'], 
                    i['id'], 
                    i['lowalch'] if 'lowalch' in i else -1, 
                    i['highalch'] if 'highalch' in i else -1, 
                    i['value'] if 'value' in i else -1, 
                    i['limit'] if 'limit' in i else -1, 
                    i['members'], 
                    i['examine'])

        with open(self.latest_file) as lf:
            latest_map = json.load(lf)['data']
            for i in latest_map:
                self.latest[int(i)] = Price(
                    int(i),
                    latest_map[i]['high'],
                    latest_map[i]['low'],
                    latest_map[i]['highTime'],
                    latest_map[i]['lowTime'])

    def get_price(self, item_names):
        if type(item_names) != type([]):
            item_names = [item_names] 

        prices = []
        for item_name in item_names:
            item_name = item_name.upper()
            if item_name in self.items:
                item_id = self.items[item_name].id
                prices.append(self.latest[item_id])
            else:
                prices.append(None)
        return prices

    def search_items(self, search_term, exclude = ''):
        out = []
        search_term = search_term.upper()
        exclude = exclude.upper()
        for i in self.items:
            item = self.items[i]
            if search_term in item.name.upper() and (exclude not in item.name.upper() or exclude == ''):
                out.append(item)

        return out

    def print_prices(self, items):
        print(*map(lambda x: f'{x[0]} - High: {x[1].high}, Low: {x[1].low}', zip(items, self.get_price(items))), sep = '\n')

def main():
    args = sys.argv

    pricer = OSRS_Pricer()
    # pricer.download_data()
    pricer.load_data()

    # print('-'*40)
    # pricer.print_prices(HERBS)
    # print('-'*40)
    # pricer.print_prices(GRIMY_HERBS)
    # print('-'*40)
    # pricer.print_prices(RUNES)
    # print('-'*40)
    hp = pricer.get_price(HERBS)
    ghp = pricer.get_price(GRIMY_HERBS)
    table_data = [['HERB', 'GRIMY PRICE', 'CLEAN PRICE', 'PROFIT']]
    for n, gh, h in zip(HERBS, ghp, hp):
        row = []
        row.append(n)
        row.append(gh.high)
        row.append(h.high)
        row.append(h.high - gh.high)
        table_data.append(row)

    table = SingleTable(table_data)
    print(table.table)


if __name__ == '__main__':
    main()