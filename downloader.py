# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
#__author__= 'ihciah@gmail.com'
#__author__= 'BaiduID-ihciah'
#__author__= 'http://www.ihcblog.com'
import os,sys,urllib2

def download(i):
    
    url="https://www.ecard.fudan.edu.cn/captcha/challenge"
    s=urllib2.urlopen(url).read()
    f=file('C:\\Users\\lenovo\\Desktop\\fdcard\\pic\\pic'+str(i)+'.jpg','wb')
    f.write(s)
    f.close()

for i in range(30000,30001):
    download(i)
    print i
