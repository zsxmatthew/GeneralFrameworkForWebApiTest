#!/usr/local/bin/python
# -*- coding: utf-8 -*-

'''
Created on

@author: Administrator
'''

if __name__ == '__main__':
    '''
    headers = {'header1':'value1', 'header2':'value2', 'header3':'value3'}
    print 'header1' in headers
    print 'header3' not in headers
    print headers['header1'][-2]
    str1 = 'host'
    str2 = 'param'
    print str1 + str2
    
    headers1 = dict(('@'+key, value) for key, value in headers.items())
    print headers1
    
    xmlns_list = ['header1', 'header2', 'header3']
    xmlns_set = set(xmlns_list)
    xmlns_set.add('header4')
    xmlns_set.add('header1')
    xmlns_set.add('header2')
    print xmlns_set
    
    import sys
    __version__ = sys.version[:3]
    print __version__
    
    proxies = ['152.168.1.2:62', '152.168.1.2', ':62', ':']
    for proxy in proxies:
        print len(proxy.split(':'))
    
    '''
    
    import re
    import XmlEngine
    import RequestEngine
    import json
    import objgraph
    import logging
    
    logging.debug('something')
    
    _typeprog = re.compile('^([^/:]+):')
    _testprog = re.compile('[^/:]+')
    _testprog1 = re.compile('^:')
    #print _typeprog.match('http://joe:password@proxy.example.com').group(0)
    #print _typeprog.match('http://joe:password@proxy.example.com').group(1)
    #print _testprog.match('http://joe:password@proxy.example.com').group(0)
    #print _testprog1.match('http://joe:password@proxy.example.com').group(0)
    #print _testprog1.match('http://joe:password@proxy.example.com').group(1)
    '''
    for i in range(0, _testprog.match('http://joe:password@proxy.example.com').lastindex):
        print _testprog.match('http://joe:password@proxy.example.com').group(i)
    '''
    
    d = {'1':{'1.1':'a', '1.2':'b'}, '2':['2.1a', '2.2b']}
    
    
    
    d = {'testplan':{'date':'$createdate', 'title':'testsettitle', 'testcase':[{'feature':'$feature', 'api':{}, 'result':[{}, {}]}, {'api': {}, 'result':[{}]}]}}
    
    l1 = [1, 2, 3]
    l2 = [4, 5, 6]
    
    '''
    for e1, e2 in zip(l1, l2):
        print e1 + e2
    '''
    
    '''
    r = RequestEngine.RequestHandler('http://api.map.baidu.com/place/v2/search?&query=%E9%93%B6%E8%A1%8C&region=%E6%B5%8E%E5%8D%97&output=json&ak=y5Ru3oCGCxrWu5O2UIdK1ZmS')
    _1, _2, _3 = r.open_request()
    print _1
    print _2
    print _3
    #print _2
    #print _3
    j2 = json.loads(_2)
    #j2 = json.loads(_2)
    #j3 = json.loads(_3)
    print j2
    #print j2
    #print j3
    print isinstance(j2, dict)
    #print isinstance(j2, dict)
    #print isinstance(j3, dict)
    
    print j2['status']
    print isinstance(j2['status'], int)
    print j2['message']
    print isinstance(j2['message'], str)
    '''
    host = 'http://api.map.baidu.com/place/v2/search?&q=饭店&region=北京&output=json&ak=y5Ru3oCGCxrWu5O2UIdK1ZmS'
    r1 = RequestEngine.RequestHandler(host, method='get')
    #print r1.host
    #print r1.data
    _4, _5, _6 = r1.open_request()
    #print _5
    
    s = u'http://api.map.baidu.com/place/v2/search?&q=\u996d\u5e97&region=\u5317\u4eac&output=json&ak=y5Ru3oCGCxrWu5O2UIdK1ZmS'
    
    s1 = u'(010)68412211'
    
    s2 = '(010)68412211'
    
    s3 = u'\u6d77'
    
    s4 = '海'
    
    #print s3.encode('utf-8') == s4
    
    #print s1.encode('utf-8') == s2
    
    '''
    import urllib
    
    s5 = u'{"a" : "apple", "b" : "banana", "g" : "grape", "o" : "orange"}'
    s5 = eval(s5)
    print isinstance(s5, dict)
    
    
    s6 = u'[{"a" : "apple", "b" : "banana", "g" : "grape", "o" : "orange"}, {}]'
    s6 = eval(s6)
    print isinstance(s6, list)
    print s6[0]['a']
    
    s7 = u'[{"a" : "apple", "b" : "banana", "g" : "grape", "o" : "orange"}, {}'
    s7 = eval(s7)
    '''
    
    import XmlEngine
    
    xh = XmlEngine.XmlHandler('Testplan.xml')
    d = xh.xml_to_dict3()
    
    
    #s = urllib.urlencode('q=饭店&region=北京&output=json&ak=y5Ru3oCGCxrWu5O2UIdK1ZmS')
    #print s
    
    
    '''
    import urllib
    import urllib2
    
    url = ['http://api.map.baidu.com/place/v2/search?&q=饭店&region=北京&output=json&ak=y5Ru3oCGCxrWu5O2UIdK1ZmS', 'http://api.map.baidu.com/place/v2/search']
    data = [{}, {'q':'饭店', 'region':'北京', 'output':'json', 'ak':'y5Ru3oCGCxrWu5O2UIdK1ZmS'}]
    ql = [urllib2.Request(u, urllib.urlencode(d)) for u, d in zip(url, data)]
    for q in ql:
        print q.get_selector()
    '''