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
                self.area[province_name][city_name].append(countys)
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

    cookies = 'o2Control=lastvisit=20; __jdv=122270672|direct|-|none|-|1486215445109; o2-webp=true; user-key=23bbd652-ffce-4d32-bd7a-99d840067728; cn=9; mt_xid=V2_52007VwATWltYV1kcTxlsBDUGGlRaDVRGShxOCRliUBsHQVAGD0hVHw9VMwFGAF5dUloeeRpdBWEfE1FBWFBLHkkSXQRsABpiX2hSah9IHVoDYwoSW21bWlo%3D; ipLoc-djd=19-1607-3155-0; ipLocation=%u5E7F%u4E1C; areaId=19; userInfo2016=1; _jrda=1; __jda=122270672.2097142271.1477320513.1486915214.1486990399.90; __jdb=122270672.10.2097142271|90.1486990399; __jdc=122270672; _jrdb=1486993040281; 3AB9D23F7A4B3C9B=6FGKGL3TDAKO5VMF4MQTKNJIEEVORZ22LW5I57ELPKVYJDJS5FVESJAW2QTG3SUS4ZVN35UZDLKLOPHPBXZAL4GEIE; __jdu=2097142271; TrackID=113XRNOLFRBTLpknkb7YkA1dP0YM5l_5vCKHF5tmOeErw2yLQ9BxtCcBBWVuIFzWPV46qysQVxk3qdKUU9q-Jhbp44OpeGiiqbtLTaZvBQWu_twwmAkE7PzGZ1KF6qJnd; pinId=N4bqDVVZn0aRA3Ujm7iq4w; pin=kaijiexue; unick=JeffXue; thor=004E93CEBF3F6E2DD0511218D2710EF1228AC55B104F66F07DBBF75358E43F7EEEF8E3E9C46022B55188D8A69D0AF42176F0ED40E5C6870A04FEAAC16143E3F6877123CBACF60DA37873BB548A561BB959D72086CBCD083477A099DE1F053F88A8246B1DDA526977E7FE500E3331B636A950B5973F92FF464AF2B850C6DF7F21808238D130C16B1E09648F499BC209CA; _tp=JCEwBYG%2BlKhYu%2B1V4lOZEw%3D%3D; logining=1; _pst=kaijiexue; ceshi3.com=-iyAr6ZSGhUpyKPSvyCYOVZ9fhc4rozGSlYyRcUtX6E'
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'

    jd_spider = JDSpider(cookies, user_agent)
    jd_spider.get_provinces()
    jd_spider.get_citys()

if __name__ == '__main__':
    main()
