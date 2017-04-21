#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pycurl
import certifi
import json
from StringIO import StringIO
from urllib import urlencode
from json.encoder import JSONEncoder
from pyasn1.compat.octets import null
from dircache import cache

class houzzApi():
    def __init__(self, token, user_name, app_name):
        self.token = token
        self.user_name = user_name
        self.app_name = app_name
        self.api_url = 'https://api.houzz.com/api?'

    def getApi(self, url):
        buffer = StringIO()
        c = pycurl.Curl()
        c.setopt(c.CAINFO, certifi.where())
        c.setopt(c.URL, url)

        header = ['X-HOUZZ-API-SSL-TOKEN: ' + self.token, 'X-HOUZZ-API-USER-NAME: ' + self.user_name,
                  'X-HOUZZ-API-APP-NAME: ' + self.app_name]
        c.setopt(c.HTTPHEADER, header)
        c.setopt(c.WRITEDATA, buffer)
        c.perform()
        c.close()

        return buffer.getvalue()

    def getListings(self, Start=0, Status='Active', NumberOfItems='100', Format='json'):
        'Get Listings'
        url = self.api_url + 'format=%s&method=getListings&Status=%s&NumberOfItems=%s&Start=%s' % (Format, Status, NumberOfItems, Start)
        body = self.getApi(url)
        try:
            return json.loads(body)
        except ValueError:
            return body

    def getOrders(self, from_date=None, to_date=None, status='All', start=0, limit=1000, Format='xml'):
        'Get Orders'
        url = self.api_url + 'format=%s&method=getOrders&Status=%s&Start=%d&NumberOfItems=%d' % (Format, status, start, limit)
        if from_date is not None and to_date is not None:
            url += '&From=%s&To=%s' % (from_date, to_date)

        body = self.getApi(url)
        return body


