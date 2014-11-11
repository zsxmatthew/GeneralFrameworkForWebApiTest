#!/usr/local/bin/python
# -*- coding: utf-8 -*-

'''
Created on 2014��10��17��

@author: Wang Mian
'''

from xml.etree import ElementTree

class XmlHandler():
    def __init__(self, xmlfile):
        self.xmlfile = xmlfile
        #content = ''.join(open(xmlfile, 'rb').read().splitlines())
        self.tree = ElementTree.parse(xmlfile)
        #self.root = ElementTree.XML(content, ElementTree.XMLParser(encoding='UTF-8'))
        self.root = self.tree.getroot()
        #self.tree = ElementTree.ElementTree(self.root)
        
    def find_child_of_tag(self, parent_tag=None, child_tag=None):
        '''
        Find all children elements with particular tag under the parent elements whose tags are specified.
        A list of results will be returned.
        @param parent_tag: tag of of parent elements whose children elements will be checked, parent element will be root if omitted.
        @param child_tag: tag of children elements with which children elements will be searched, all children elements will be returned if omitted.
        '''
        if parent_tag is None:
            roots = [self.root, ]
        else:
            roots = self.root.findall(parent_tag)
        
        children = []
        for root in roots:
            if child_tag:
                children.extend([child for child in root if child.tag == child_tag])
            else:
                children.extend([child for child in root])
        
        return children
    
    def _find_child_of_elem(self, parent_elem=None, child_tag=None):
        '''
        Find all children elements with particular tag under a parent element.
        A list of results will be returned.
        @param parent_elem: the parent element whose children elements will be checked, parent element will be root if omitted.
        @param child_tag: tag of children elements with which children elements will be searched, all children elements will be returned if omitted.
        '''
        if parent_elem is None:
            root = self.root
        else:
            root = parent_elem

        return [child for child in root if child.tag == child_tag] if child_tag else [child for child in root]
        
    def xml_to_dict(self):
        return self._elem_to_dict(self.root)
    
    def _elem_to_dict(self, elem):
        d = {}
        d['tag'] = elem.tag
        if elem.text:
            d['text'] = elem.text
        if elem.tail:
            d['tail'] = elem.tail
        if elem.attrib:
            d['attrib'] = elem.attrib
        if list(elem):
            d['children'] = []
            for e in list(elem):
                d['children'].append(self._elem_to_dict(e))
        return d
    
    def xml_to_dict2(self):
        return self._elem_to_dict2(self.root)
    
    def _elem_to_dict2(self, elem):
        d = dict(tag=elem.tag)
        if elem.text:
            d['text'] = elem.text
        if elem.tail:
            d['tail'] = elem.tail
        if elem.attrib:
            d['attrib'] = elem.attrib
        if list(elem):
            d['children'] = map(self._elem_to_dict2, list(elem))
        return d
    
    def xml_to_dict3(self):
        return self._elem_to_dict3(self.root)
    
    def _elem_to_dict3(self, elem):
        '''
        Transform an element and its sub-elements into a dictionary, attribute names and tags of children will be keys of a parent element.
        Value of a dictionary item for an element with unique tag is a dictionary.
        If many elements in a same level have a same tag, they will be made into a single item in the dictionary of their parent element, whose key will be their tag, and value will
        be a list whose each item is a dictionary which represents one of these elements.
        '''
        d = {}
        d[elem.tag.strip()] = {}
        d[elem.tag.strip()].update(elem.attrib)
        for k, v in d[elem.tag].items():
            k = k.strip()
            v = v.strip()
        _tagd = self._children_tag_to_dict(elem)
        for tag in _tagd.keys():
            #print 'parent: %s, child: %s, number of child %s: %d'%(elem.tag, tag, tag, _tagd[tag])
            #print [child.tag for child in self._find_child_of_elem(elem, tag)]
            if _tagd[tag] > 1: #those elements in the same level and having a same tag will be transformed to an item whose key is the tag and value is a list, each item of this list is a dictionary
                #print 'd[%s][%s] = '%(elem.tag, tag) + str([self._elem_to_dict3(e)[tag] for e in self._find_child_of_elem(elem, tag)]) + '\n'
                d[elem.tag][tag] = [self._elem_to_dict3(e)[tag] for e in self._find_child_of_elem(elem, tag)]
            else: #those elements with unique tag will be transformed to an item whose key is the tag and value is a dictionary
                #print 'd[%s] = '%elem.tag + str(self._elem_to_dict3(self._find_child_of_elem(elem, tag)[0])) + '\n'
                d[elem.tag].update(self._elem_to_dict3(self._find_child_of_elem(elem, tag)[0]))
        return d
    
    def _children_tag_to_dict(self, elem=None):
        '''
        Generate a dictionary for an element, keys represent tags of direct children elements, and value for a key is number of elements with same tag. 
        '''
        if elem is None:
            elem = self.root
        _tagd = {}
        for child in elem:
            if child.tag not in _tagd.keys():
                _tagd[child.tag] = 1
            else:
                _tagd[child.tag] += 1
        return _tagd        
    
    def write_to_file(self, target_file=None):
        #content = ElementTree.tostring(self.root, 'utf-8')
        self.tree.write(self.xmlfile if target_file else target_file, 'utf-8')
    
    def _element_to_string(self, elem):
        return ElementTree.tostring(elem, 'utf-8').strip()
    
    def elements_to_string(self, tag):
        return [self._element_to_string(elem) for elem in self.root.iter(tag)]
    
    def extract_xmlns_from_dict(self):
        ns_count = len(self._extract_xmlns_from_dict(self.xml_to_dict()))
        return dict(zip(self._extract_xmlns_from_dict(self.xml_to_dict()), ['ns%d'%i for i in range(0, ns_count)]))
    
    def _extract_xmlns_from_dict(self, d):
        xmlns_set = set([])
        if d.has_key('tag') and d['tag'].find('}') > -1:
            xmlns = d['tag'].split('}')[0].strip('{}')
            xmlns_set.add(xmlns)
        if d.has_key('children'):
            for child in d['children']:
                xmlns_set.update(self._extract_xmlns_from_dict(child))
        return xmlns_set
    
    '''
    def ns_replace_tag(self, nsdict):
        
        how to process namespace?
        how to process text?

        elemlist = [elem for elem in self.root.iter() if len(elem.tag.split(':')) > 0]
        keylist = [elem.tag.split(':')[0] for elem in self.root.iter() if len(elem.tag.split(':')) > 0]
        elemdict = dict(zip(elemlist, keylist))
        for key, elem in elemdict:
            if key in nsdict:
                elem.tag = '%s:%s'%(nsdict[key], elem.tag.split(':'))
    '''

if __name__ == '__main__':
    #xh = XmlHandler('purchaseInformation_nomnc.xml')
    xh = XmlHandler('Testplan.xml')
    root = xh.root
    #print xh.xml_to_dict()
    #print xh.xml_to_dict2()
    xh.write_to_file('sample.xml')
    #print xh._element_to_string(root)
    #d = xml_json.dict_to_json(xh.xml_to_dict())
    #print d
    d = xh.extract_xmlns_from_dict()
    #print d
    
    xh = XmlHandler('Testplan.xml')
    #print xh.find_child('testcase', 'api')
    print xh.xml_to_dict3()
    
    #print xh._children_tag_to_dict()
    #print xh.find_child_of_tag(child_tag='testcase')