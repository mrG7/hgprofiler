# -*- coding: utf-8 -*-
import base64
import hashlib
import scrapy
from scrapy import log
from scrapy import Request
import urllib
import json

class ProfilerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    png_file = scrapy.Field()
    username = scrapy.Field()
    resource = scrapy.Field()
    category = scrapy.Field()

class ProfilerSpider(scrapy.Spider):
    name = "profiler_spider"

    def __init__(self, usernames, **kwargs):
        self.site_db = json.load(open("profiler_sites.json"))
        self.usernames = usernames.split(",")

    def start_requests(self):
        # create sites lookup table
        matched  = []
        for user in self.usernames:
            print('Looking up data for: %s' % user)
            for site in self.site_db["sites"]:
                url = site['u'] % urllib.quote(user)
                print('Checking: %s' % site['r'])
                try:
                    yield Request(url,
                                  meta={'dont_redirect': True,
                                        'site' : site,
                                        'user' : user})
                except KeyboardInterrupt:
                    raise KeyboardInterrupt
                except Exception as e:
                    print('%s: %s' % (url, e.__str__()))
                    continue

    def parse(self, response):
        # <script src.. xpath should trigger splash request
        site = response.request.meta['site']
        needed_resp_code = response.request.meta['site']['gRC']

        if 'original_status' in response.meta:
            status = response.meta['original_status']
        else:
            status = response.status

        if status == int(needed_resp_code):
            print('Codes matched %s %s' % (response.status, needed_resp_code))
            if site['gRT'] in response.meta['original_body'] or \
               site['gRT'] in response.meta['original_headers']:

                print('Probable match: %s' % response.request.meta['original_url'])
                png = base64.b64decode(response.request.meta['png'])
                sha1 = hashlib.sha1(png).hexdigest()

                with open('ui/static/images/thumbs/%s.png' % sha1, 'wb') as png_file:
                    png_file.write(png)

                item = ProfilerItem()
                item["username"] = response.request.meta['user']
                item["url"] = response.request.meta['original_url']
                item["png_file"] = '%s.png' % sha1
                item["resource"] = site['r']
                item["category"] = site['c']
                return item
