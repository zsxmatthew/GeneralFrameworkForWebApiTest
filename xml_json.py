"""

A convention for marshalling XML as JSON, based on elementtree, and
written in reaction to badgerfish (http://badgerfish.ning.com/).

An xml element is represented as a dictionary with the keys:

    * tag
    * attributes
    * text
    * tail
    * children

"""
# convert a XML element to Python dictionary 
def elem_to_dict(elem):
    """
    turns an elementtree-compatible object into a pesterfish dictionary
    (not json).
    
    """
    d=dict(tag=elem.tag)
    if elem.text:
        d['text']=elem.text
    if elem.attrib:
        d['attributes']=elem.attrib
    children=elem.getchildren()
    if children:
        d['children']=map(elem_to_dict, children)
    if elem.tail:
        d['tail']=elem.tail
    return d

ns_dict = {"http://payment.ovi.com/dcomms2sapi":"ns6",
           "http://account.nokia.com/schemas/rest/v1_0":"ns5",
           "http://payment.ovi.com/catalog":"ns4",
           "http://payment.ovi.com/ope":"ns3",
           "http://payment.ovi.com/nps":"ns2",
           "http://payment.ovi.com/iap":'ns7',
           "http://www.payment.ovi.com/dcommacapi":'ns8'}
 # namespace dictionary for xml files. key is {<namespaceURL>} and value is replacement ns<number>

# convert Python dictionary from elem_to_dict() to json dictionary
# note text and tail are not processed. (OPE request xml has no text or tail).
def dict_to_json(dic):
    d={}
    if dic.has_key('attributes'):
        d[ns_replace(dic['tag'])] = dict(('@'+item[0],item[1]) for item in dic['attributes'].items())
    if dic.has_key('text'):
        if d.has_key(ns_replace(dic['tag'])): # if key already exists (when attributes exists and processed previously
            val = d[ns_replace(dic['tag'])] # get value (dictionary) and update it with cd
            if dic['text'].strip():
                val.update({'$':dic['text']})  
            d[ns_replace(dic['tag'])] = val  # put everything back
        else:
            if dic['text'].strip():
                d[ns_replace(dic['tag'])] = {'$':dic['text']}            
    if dic.has_key('children'):
        if dic.has_key('attributes'): 
            pass  # for debugging purpse when element has both children and attributes
        cd = {}
        for child in dic['children']:
            if child:
                cd.update( dict_to_json(child))
        if d.has_key(ns_replace(dic['tag'])): # if key already exists (when attributes exists and processed previously
            val = d[ns_replace(dic['tag'])] # get value (dictionary) and update it with cd
            val.update(cd)  
            d[ns_replace(dic['tag'])] = val  # put everything back
        else: d[ns_replace(dic['tag'])] = cd
    return d

# function is used to replace tag with full namespace to simplifed one: ns<#>, also it would collect namespace string into ns_dict if not exists
def ns_replace(key):
    global ns_dict
    keysplit=key.split('}')
    keysplit[0] = keysplit[0] +'}'
    if ns_dict.has_key(keysplit[0].strip('{}')): return ns_dict[keysplit[0].strip('{}')]+':'+keysplit[1]
    else:
        ns_dict[keysplit[0]] = "ns%d"%(len(ns_dict)+1)
        return ns_dict[keysplit[0]]+':'+keysplit[1]
    
def createJsonRequest(dic):
    global ns_dict
    retdict = {}
    tempjson=dict_to_json(dic)
    retdict['@xmlns']= dict((item[1],item[0].strip('{ }')) for item in ns_dict.items())
    retdict.update(tempjson.values()[0])
    return {tempjson.keys()[0]:retdict}

    
    
