# -*- coding:utf-8 -*-
import requests


class JDSpider:

    def __init__(self, cookies, user_agent):
        self.session = requests.session()
        self.cookies = cookies
        self.user_agent = user_agent
        self.headers = {'Cookie': self.cookies, 'User-Agent': self.user_agent}
        self.area = {}

    def get_provinces(self):
        url = 'https://easybuy.jd.com//address/getProvinces.action'
        r = self.session.get(url, headers=self.headers)
        provinces = r.json()
        for province_id, province_name in provinces.items():
            self.area.update({province_name: {}})
        return provinces

    def get_citys(self, province_id, province_name):
        url = 'https://easybuy.jd.com//address/getCitys.action'
        data = {'provinceId': int(province_id)}
        r = self.session.post(url, data=data, headers=self.headers)
        citys = r.json()
        for city_id, city_name in citys.items():
            self.area[province_name].update({city_name: []})
        return citys

    def get_countys(self, province_name, city_id, city_name):
        county_url = 'https://easybuy.jd.com//address/getCountys.action'
        data = {'cityId': int(city_id)}
        r_county = self.session.post(county_url, data=data, headers=self.headers)
        try:
            countys = r_county.json()
            for county_id, county_name in countys.items():
                self.area[province_name][city_name].append(county_name)
            return countys
        except Exception:
            print Exception

    def get_area_dict(self):
        provinces = self.get_provinces()
        for province_id, province_name in provinces.items():
            citys = self.get_citys(province_id, province_name)
            for city_id, city_name in citys.items():
                self.get_countys(province_name, city_id, city_name)
        return self.area


def main():
    cookies = ''
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'

    jd_spider = JDSpider(cookies, user_agent)
    areas = jd_spider.get_area_dict()
    provinces = sorted(areas.keys())
    for province in provinces:
        print province + ': '
        citys = sorted(areas[province].keys())
        for city in citys:
            print '  ' + city + ': '
            countys = sorted(areas[province][city])
            if countys:
                print '    -'
            for county in countys:
                print '      ' + county

if __name__ == '__main__':
    main()
