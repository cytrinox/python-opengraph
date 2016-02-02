# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import re

import requests
from bs4 import BeautifulSoup


class OpenGraph(object):

    def __init__(self, url=None, html=None, useragent=None):
        self._data = {}
        self._useragent = useragent
        content = html or self._fetch(url)
        self._parse(content)

    def __contains__(self, item):
        return item in self._data

    def __getattr__(self, name):
        if not self.__contains__(name):
            raise AttributeError(
                'Open Graph object has no attribute "{}"'.format(name))
        else:
            return self._data[name]

    def __repr__(self):
        return self._data.__str__()

    def __str__(self):
        return self.__repr__()

    def _fetch(self, url):
        headers = {}
        if self._useragent:
            headers = {
                'user-agent': self._useragent
            }
        response = requests.get(url, headers=headers)
        return response.text

    def _parse(self, html):
        doc = BeautifulSoup(html, 'html.parser')
        ogs = doc.html.head.findAll(property=re.compile(r'^og'))

        for og in ogs:
            if og.has_attr('content'):
                self._data[og['property'][3:]] = og['content']

