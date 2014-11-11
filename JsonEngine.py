#!/usr/local/bin/python
# -*- coding: utf-8 -*-

'''
Created on 2014��10��30��

@author: Administrator
'''

def _findJsonPath(jresp, path):
    '''
    Return value of one item through path list or return empty list if path chain can't be matched within jresp.
    Searching is only matched when all path in the path chain can be found one after another in jresp, latter one existing in next level of former.
    @param jresp: a dict or list which represents part of one json object
    @param path: a list which represents a path chain within a json object, first item in the list is the beginning of the chain and last is the end
    '''
    val = []
    if isinstance(jresp, list):
        for resp in jresp:
            if isinstance(resp, dict):
                if resp.has_key(path[0]):
                    if len(path) > 1:
                        val.extend(_findJsonPath(resp[path[0]], path[1:]))
                    else:
                        val.extend([resp[path[0]]])
                                
    if isinstance(jresp, dict):
        if jresp.has_key(path[0]):
            if len(path) > 1:
                val.extend(_findJsonPath(jresp[path[0]], path[1:]))
            else:
                val.extend([jresp[path[0]]])
        
    return val

def _validateJsonEqual(find, expect):
    '''
    Compare between value of find or each of its item and value of expect.
    '''
    
    try:
        exp = _encodeutf8(eval(expect))
    except Exception:
        exp = expect
    
    for f in find:
        if isinstance(f, dict) and isinstance(exp, dict):
            for kf, ke in zip(f.keys(), exp.keys()):
                if kf != ke:
                    return False
                if not _validateJsonEqual(f[kf], exp[ke]):
                    return False
        elif isinstance(f, list) and isinstance(exp, list):
            for f, e in zip(f, exp):
                if not _validateJsonEqual(f, e):
                    return False
        else:
            if f != exp:
                return False
    return True
    
def _encodeutf8(target):
    '''
    Process a file like json object, encode all unicode strings (such as Chinese) to utf-8 strings
    '''
    if isinstance(target, dict):
        d = {}
        for k, v in target.items():
            key = k.encode('utf-8') if isinstance(k, unicode) else k
            d[key] = _encodeutf8(v)
        return d
    elif isinstance(target, list):
        l = []
        for i in target:
            l.append(_encodeutf8(i))
        return l
    elif isinstance(target, unicode):
        s = target.encode('utf-8')
        return s
    else:
        return target
    
if __name__ == '__main__':
    #print _validateJsonEqual([u'ok'], 'ok')
    import XmlEngine
    xh = XmlEngine.XmlHandler('Testplan.xml')
    print xh.xml_to_dict3()
    print _encodeutf8(xh.xml_to_dict3())
    print '\xe9\xa5\xad\xe5\xba\x97' == '饭店'
