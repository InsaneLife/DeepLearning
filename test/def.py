#coding=utf-8
import urllib2
import simplejson

def GDapi(url):
    url=url.replace(' ', '')
    url=url.encode("utf-8")
    response = urllib2.urlopen(url)
    html = response.read()
    dictinfo = simplejson.loads(html)
    addr=u"其他地区"
    if dictinfo.has_key('list')!=True:
     return 'null'
    elif len(dictinfo["list"])>1:
        for each in dictinfo["list"]:
            if u"阿坝"  in each["name"] or u"宜宾"  in each["name"] or u"成都"  in each["name"]:
                addr=each["district"]
    else:
        if dictinfo["list"][0]["district"]=='':
            return 'null'
        addr=dictinfo["list"][0]["district"]
    return addr
url=u'http://restapi.amap.com/geocode/simple?resType=json&encode=utf-8&poinum=1&retvalue=1&address=土 门 乡'
test=GDapi(url)
print test