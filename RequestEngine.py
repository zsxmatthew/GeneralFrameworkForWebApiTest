#!/usr/local/bin/python
# -*- coding: utf-8 -*-

'''
Created on

@author: Administrator
'''

import urllib, urllib2, httplib
import urlparse
import StringIO, gzip, zlib
import sys

class RequestHandler():
    '''
    classdocs
    '''

    def __init__(self, host, data=None, headers=None, method='POST', http_proxy=None, https_proxy=None):
        '''
        Constructor
        @param host: host url
        @param data: a dictionary of parameters in request or data to be sent with request
        @param headers: a dictionary of headers
        @param method: request method, could be one of GET, POST, PUT and DELETE
        @param proxy: string in proxy_address:port format  
        '''
        if data is None or len(data) == 0:
            self.host = host[:host.find('?')] if host.find('?') > -1 else host
            d = host[host.find('?')+1:] if host.find('?') > -1 else ''
            self.data = urllib.quote_plus(d, '%&/=')
        else:
            self.host = host
            self.data = urllib.urlencode(data)
        self.headers = headers if headers and isinstance(headers, dict) else {}
        self.method = method.upper() if method else 'POST'
        self.proxy = {}
        self.proxy.update(dict(http=http_proxy) if http_proxy else {})
        self.proxy.update(dict(https=https_proxy) if https_proxy else {})
        self.ph = urllib2.ProxyHandler(self.proxy) if len(self.proxy) > 0 else None
        self.opener = urllib2.build_opener(self.ph) if self.ph else urllib2.build_opener()
        
    def add_header(self, headers=None):
        '''
        Add another header to the request.
        Note that there cannot be more than one header with the same name, and later calls will overwrite previous calls in case the key collides.
        @param headers: a dictionary of new headers
        '''
        if headers and isinstance(headers, dict):
            for name, value in headers:
                self.headers[name] = value
                
    def create_request(self):
        '''
        Create an urllib2 request or httplib request as per request method.
        For GET and POST methods, url of the request should be host + '/' + action + '?' + params or host + '?' + params if action is omitted.
        '''
        assert self.method in ['GET', 'POST', 'PUT', 'DELETE'], 'Invalid request method'
        
        _request = urllib2.Request(self.host, self.data, self.headers)
        if self.method == 'PUT' or self.method == 'DELETE':
            if urlparse.urlparse(self.host).scheme == 'https':
                self.request = httplib.HTTPSConnection(urlparse.urlparse(_request.get_host()).netloc) #passing host without url scheme
                if self.proxy.has_key('https'):
                    self.request.set_tunnel(self.proxy['https'])
            else:
                self.request = httplib.HTTPConnection(urlparse.urlparse(_request.get_host()).netloc) #passing host without url scheme
                if self.proxy.has_key('http'):
                    self.request.set_tunnel(self.proxy['http'])
            self.selector = _request.get_selector()
        elif self.method == 'GET':
            self.url = self.host if self.host[-1] == '?' else self.host + '?'
            self.url += self.data if self.data else ''
            self.request = urllib2.Request(self.url, headers=self.headers)
        elif self.method == 'POST':
            self.request = urllib2.Request(self.host, self.data, self.headers)
            
    def open_request(self):
        '''
        Make http request.
        '''
        self.create_request()
        
        try:
            if self.method == 'PUT' or self.method == 'DELETE':
                self.request.request(self.method, self.selector, self.headers)
                self.response = self.request.getresponse()
                self.request.close()
                return self.response.msg, self._decode(self.response), self.response.status
            elif self.method == 'GET' or self.method == 'POST':
                self.response = self.opener.open(self.request)
                return self.response.info(), self._decode(self.response), self.response.getcode()
        except Exception, e:
            print 'ERROR %s: %s'%(self.method, e)

    def _decode(self, page):
        try:
            encoding = page.info().get("Content-Encoding")    
            if encoding in ('gzip', 'x-gzip', 'deflate'):
                content = page.read()
                if encoding == 'deflate':
                    data = StringIO.StringIO(zlib.decompress(content))
                else:
                    data = gzip.GzipFile('', 'rb', 9, StringIO.StringIO(content))
                page = data.read()
            else: page = page.read()
        except Exception:
            tu = sys.exc_info()
            page="Error Occured! \nException: %s =>%s \nFile: %s\n Line: %s\n"%(str(tu[0]).strip('<>'),str(tu[1]),tu[2].tb_frame.f_code.co_filename,tu[2].tb_lineno)            
        return page
            
if __name__ == '__main__':
    rt = []
    rt.append(RequestHandler('http://api.map.baidu.com/place/v2/search', method='GET'))
    rt.append(RequestHandler('http://api.map.baidu.com/place/v2/search', method='get'))
    rt.append(RequestHandler('http://api.map.baidu.com/place/v2/search?q=饭店&region=北京&output=json&ak=E4805d16520de693a3fe707cdc962045', method='get'))
    rt.append(RequestHandler('http://api.map.baidu.com/place/v2/search', data={'q':'饭店', 'region':'北京', 'output':'json', 'ak':'E4805d16520de693a3fe707cdc962045'}))
    rt.append(RequestHandler('http://api.map.baidu.com/place/v2/search?q=饭店&region=北京&output=json&ak=E4805d16520de693a3fe707cdc962045', method='put'))
    rt.append(RequestHandler('http://api.map.baidu.com/place/v2/search', data={'q':'饭店', 'region':'北京', 'output':'json', 'ak':'E4805d16520de693a3fe707cdc962045'}, method='delete'))
    rt.append(RequestHandler('https://api.map.baidu.com/place/v2/search', data={'q':'饭店', 'region':'北京', 'output':'json', 'ak':'E4805d16520de693a3fe707cdc962045'}, method='delete'))
    rt.append(RequestHandler('http://api.map.baidu.com/place/v2/search?&query=%E9%93%B6%E8%A1%8C&region=%E6%B5%8E%E5%8D%97&output=json&ak=E4805d16520de693a3fe707cdc962045'))
    
    '''
    for r in rt:
        r.open_request()
    '''
    
    _header, _msg, _status = rt[len(rt)-1].open_request()
    print 'response_header: ' + str(_header)
    #print 'response_body: ' + str(_msg)
    #print 'response_status: ' + str(_status)