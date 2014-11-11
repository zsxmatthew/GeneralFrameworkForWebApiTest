#!/usr/local/bin/python
# -*- coding: utf-8 -*-

'''
Created on 2014年10月21日

@author: Administrator
'''

import XmlEngine
import RequestEngine
import unittest
import re
import json
import JsonEngine

class Webapitest(object):
    
    def __init__(self, test_config):
        self.case_group, self.api_group, self.expectation_group = self.parseTestConfig(test_config)
        #print self.api_group
        #print self.expectation_group
        
    def parseTestConfig(self, test_config):
        '''
        Parse test plan file to extract test cases.
        Return lists of test cases, api information and expected results.
        @param test_config: test plan file path, the file can only be a xml or a csv.
        '''
        ext = test_config.split('.')[-1]
        assert ext in ['csv', 'xml'], 'Invalid test_config file type, only .csv and .xml are supported.'
        
        case_group = []
        api_group = []
        expectation_group = []
        if ext == 'csv':
            pass
        else:
            xh = XmlEngine.XmlHandler(test_config)
            case_group = [elem for elem in xh.xml_to_dict3()['testplan']['testcase']]
            api_group = [xh._elem_to_dict3(elem)['api'] for elem in xh.find_child_of_tag('testcase', 'api')]
            expectation_group = [xh._elem_to_dict3(elem)['result'] for elem in xh.find_child_of_tag('testcase', 'result')]

            return case_group, api_group, expectation_group
    
    def runTestCase(self):
        for api, exp in zip(self.api_group, self.expectation_group):
            info, response, status = self._runTestCase(api)
            assert status == 200, 'Request failed.'
            self._validateResult(info.get('Content-Type').strip(), response, exp)
    
    def _runTestCase(self, api):
        '''
        Send a single request, and return the response.
        '''
        pattern_header = '^header_.+$'
        pattern_param = '^param_.+$'
        _api_info = {'url' : None, 'http_proxy': None, 'https_proxy': None, 'method': 'POST', 'headers': {}, 'params' : {}}
        
        for key, val in api.items():
            if key == 'url':
                _api_info['url'] = val.encode('utf-8') if val.strip() != '' else None
            elif key == 'http_proxy':
                _api_info['http_proxy'] = val if val.strip() != '' else None
            elif key == 'https_proxy':
                _api_info['https_proxy'] = val if val.strip() != '' else None
            elif key == 'method':
                _api_info['method'] = val if val.strip() != '' else None
            elif re.search(pattern_header, key) is not None:
                if val.strip() != '':
                    _api_info['headers'][key.split('_')[1]] = val
            elif re.search(pattern_param, key) is not None:
                if val.strip() != '':
                    _api_info['params'][key.split('_')[1]] = val.encode('utf-8')
        
        rt = RequestEngine.RequestHandler(_api_info['url'], _api_info['params'], _api_info['headers'], _api_info['method'], _api_info['http_proxy'], _api_info['https_proxy'])
        #print rt.host
        #print rt.data
        return rt.open_request()
    
    def _validateResult(self, type, response, expectation):
        #if type == 'application/json;charset=UTF-8':
        if True:
            print 'response: ' + repr(response)
            jresp = json.loads(response)
            #print 'jresp: ' + repr(jresp)
            for _, v in expectation.items():
                _type = v['type']
                _path = [key.strip() for key in v['expect'].split(':')[:-1]]
                _val = v['expect'].split(':')[-1].strip()
                
                if _type == 'class': #specified field is of one specified class
                    pass
                elif _type == 'valueEqual': #specified field has one specified value which could be list or dict
                    find = JsonEngine._findJsonPath(jresp, _path)
                    self.assertTrue(JsonEngine._validateJsonEqual(find, _val))
                elif _type == 'jsonEqual': #whole response equals to one specified json object
                    pass
                elif _type == 'valueIn':
                    pass
        else:
            pass

if __name__ == '__main__':
    t = Webapitest('Testplan.xml')
    t.runTestCase()