# -*- coding:utf-8 -*-
import json
import requests

taobao_area_url = 'https://g.alicdn.com//vip/address/6.0.5/index-min.js'


class MapModel:

    def __init__(self, map_list):
        self.id = map_list[0]
        self.name = map_list[1][0]
        self.parent_id = map_list[2]


class TaoBaoSpider:

    def __init__(self, url=taobao_area_url):
        self.url = url
        self.session = requests.session()

    def grab_area_data(self):
        r = self.session.get(self.url)
        return r.text

    def get_area_dict(self):
        areas_text = self.grab_area_data()
        areas = {}

        provinces = eval(areas_text.split('"A-G":')[1].split('"H-K"')[0])[0] + eval(areas_text.split('"H-K":')[1].split('"L-S"')[0])[0] + eval(areas_text.split('"L-S":')[1].split('"T-Z"')[0])[0] + eval(areas_text.split('"T-Z":')[1].split('}')[0])
        for item_list in provinces:
            province = MapModel(item_list)
            areas.update({province.id: {'name': province.name, 'city': {}}})

        city_and_county = eval('[[' + areas_text.split('var e=[[')[1].split(';')[0])
        city_to_province = {}
        for item_list in city_and_county:
            item = MapModel(item_list)
            if item.parent_id in areas.keys():
                province_id = item.parent_id
                areas[province_id]['city'].update({item.id: {'name': item.name, 'county': []}})
                city_to_province.update({item.id: province_id})

        for item_list in city_and_county:
            item = MapModel(item_list)
            if item.parent_id not in areas.keys():
                city_id = item.parent_id
                areas[city_to_province[city_id]]['city'][city_id]['county'].append(item.name)

        # 港澳
        # areas_text.split('var e=[[')[1].split(';')[0]

        # 台湾
        # areas_text.split('var e=[[')[2].split(';')[0]

        # 马来西亚
        # areas_text.split('var e=[[')[3].split(';')[0]

        # 海外其他
        # areas_text.split('var e=[[')[4].split(';')[0]

        return areas


def main():
    spider = TaoBaoSpider()
    areas = spider.get_area_dict()

    new_areas = {}
    for province_id, province in areas.items():
        new_city = {}
        for city_id, city in province['city'].items():
            new_city.update({city['name']: city['county']})
        new_areas.update({province['name']: new_city})

    provinces = sorted(new_areas.keys())
    for province in provinces:
        print province + ': '
        citys = sorted(new_areas[province].keys())
        for city in citys:
            print '  ' + city + ': '
            countys = sorted(new_areas[province][city])
            if countys:
                print '    -'
            for county in countys:
                print '      ' + county


if __name__ == '__main__':
    main()
