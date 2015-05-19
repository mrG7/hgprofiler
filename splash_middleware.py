# -*- coding: utf-8 -*-
from __future__ import absolute_import

import base64
import json
import logging
import os

from urlparse import urljoin
from urllib import urlencode

from scrapy.http import Request


class SplashMiddleware(object):
    def process_response(self, request, response, spider):
        if 'splash_enabled' in request.meta:
            data = json.loads(response.body)
            request.meta['png'] = data['png']
            return response
        elif response.status == 200:
            meta = {
                'original_body': response.body_as_unicode(),
                'original_headers': response.headers,
                'original_status': response.status,
                'original_url': response.url,
                'site' : request.meta['site'],
                'splash_enabled': True,
                'user' : request.meta['user'],
            }
            url = 'http://localhost:8050/render.json?url=%s' \
                  '&png=1&width=800&height=600&wait=3' % request.url
            return Request(url, meta=meta)
        else:
            return response
