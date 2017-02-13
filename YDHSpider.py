# -*- coding:utf-8 -*-
import requests


ydh_area_url = 'http://res.dinghuo123.com/data/area.json'


class YdhSpider:

    def __init__(self, url=ydh_area_url):
        self.url = url
        self.session = requests.session()

    def grab_area_data(self):
        r = self.session.get(self.url)
        return r.json()

    def get_area_dict(self):
        areas = self.grab_area_data()
        data = {}
        for country in areas:
            if country['name'] == u'其他区域':
                continue
            data.update({country['name']: {}})
            for province in country['provinces']:
                data[country['name']].update({province['name']: {}})
                for city in province['citys']:
                    data[country['name']][province['name']].update({city['name']: []})
                    for district in city['districts']:
                        data[country['name']][province['name']][city['name']].append(district['name'])
        return data


def main():
    spider = YdhSpider()
    areas = spider.grab_area_data()
    for country in areas:
        if country['name'] == u'其他区域':
            continue
        print country['name']
        for province in country['provinces']:
            print '    ' + province['name']
            for city in province['citys']:
                print '        ' + city['name']
                for district in city['districts']:
                    print '            ' + district['name']


def main2():
    spider = YdhSpider()
    areas = spider.get_area_dict()
    print areas

if __name__ == '__main__':
    # main2()
    main()


