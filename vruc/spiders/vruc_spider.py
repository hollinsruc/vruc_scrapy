# !/usr/bin/env python
# -*- coding: utf-8 -*-
import scrapy
import os
from vruc.items import GradeItem
from vruc.utils.cookieUtils import getCookieValue
import urlparse

class vruc(scrapy.Spider):
    name = 'vruc'
    start_urls = ['http://v.ruc.edu.cn']
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Length': '112',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'uc.tiup.cn',
        'Origin': 'https://uc.tiup.cn',
        'Pragma': 'no-cache',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    def start_requests(self):
        return [scrapy.Request(self.start_urls[0], meta = {'cookiejar' : 1}, callback = self.parse, dont_filter = True)]

    def parse(self, response):
        url = 'https://uc.tiup.cn/account/login'
        username = raw_input("Please Input Your StudentID:")
        pwd = raw_input("Please Input Your password:")
        self.logger.info("Visited %s", response.url)
        # token from cookie
        token = getCookieValue('csrf_token', response.headers['Set-Cookie'])
        self.logger.info("token %s", token)

        return [scrapy.FormRequest(url = url,
            meta = {'cookiejar' : response.meta['cookiejar'], 'username': username},
            formdata={
                'csrf_token': token,
                'school_code': 'ruc',
                'username': username,
                'password': pwd,
                'remember_me': 'false'
            },
            callback=self.parse_grade,
            dont_filter = True
        )]

    def parse_vrucindex(self, response):
        return [scrapy.Request('http://v.ruc.edu.cn/me', meta = {'cookiejar' : response.meta['cookiejar']}, callback = self.savehtml, dont_filter = True)]
    
    def parse_grade(self, response):
    	username = response.meta['username']
        return [scrapy.Request('http://app.ruc.edu.cn/idc/education/report/xscjreport/XscjReportAction.do?method=printXscjReport&xh='+username, meta = {'cookiejar' : response.meta['cookiejar']}, callback = self.savegrade, dont_filter = True)]

    def savehtml(self, response):
        with open('%s%s%s' % (os.getcwd(), os.sep, 'logged.html'), 'wb') as f:
            f.write(response.body)
    def savegrade(self, response):
        trs = response.css('.deep_table>tr')
        for index,row in enumerate(trs):
            tds = row.xpath('td/text()').extract()
            if(len(tds) < 10):
                continue
            grade = GradeItem()
            grade['name'] = tds[0][:-1]
            grade['ctype'] = tds[2][:-1]
            grade['teacher'] = tds[1][:-1]
            grade['credit'] = tds[3][:-1]
            grade['point'] = tds[8][:-1]
            yield grade