# -*- coding: utf-8 -*-
import Image,ImageDraw,ImageFont,ImageFilter
from svmutil import *
import random,pickle 
import math
model=0

def trans(x):
    #字母和数字转换
    if isinstance(x, int) or isinstance(x, float):
        return chr(ord('a')+int(x))
    else:
        return ord(x)-ord('a')
def xq(image,T=50,A=2,X=0):
    #x轴不变，y轴扭曲
    #T:cos函数周期
    #A:cos函数振幅
    #X:偏移像素数

    pix=image.load()
    
    pi=3.1415926
    tmp=2.0*pi/T
    width,height = image.size

    newimage = Image.new('L',(width,height),255)

    newpix=newimage.load()
    for x in range(width):  
        for y in range(height):
            if pix[x,y]==0:
                newy = y + math.sin((x-X)*tmp)*A
                if newy>=0 and newy<height:
                    newpix[x,newy]=0
    return newimage

def yq(image,T=100,A=2,X=0):
    #y轴不变，x轴扭曲
    #T:cos函数周期
    #A:cos函数振幅
    #X:偏移像素数

    pix=image.load()
    
    pi=3.1415926
    tmp=2.0*pi/T
    width,height = image.size

    newimage = Image.new('L',(width,height),255)

    newpix=newimage.load()
    for y in range(height):  
        for x in range(width):
            if pix[x,y]==0:
                newx = x + math.sin((y-X)*tmp)*A
                if newx>=0 and newx<width:
                    newpix[newx,y]=0
    return newimage
               
def cutpic(image,begin,end):
    #print "pos:",begin,end
    img=image.crop((begin+1,14,end,60))
    return img.resize((9,9),Image.ANTIALIAS)

def predata(filepath):
    #读取文本文件，返回libsvm格式的数据
    f=file(filepath,'r')
    y=[]
    x=[]
    pw=0
    pr=0
    for line in f:
        r=line.split(',')
        if len(r)!=2:
            print "Line error!"
            continue
        r[1]=r[1].replace('\r',"").replace('\n',"")
        count=len(r[1])
        if count==0:
            continue
        rval=pre("pic/pic"+str(r[0])+".jpg")
        if len(rval)!=count:
            pw=pw+1
            continue
        for c in range(0,count):
            pr=pr+1
            y.append(trans(r[1][c]))
            x.append(rval[c])
    f.close()
    print "Pic cut accuracy:",pr,"/",pw+pr,"(",str(float(pr)/(pw+pr)*100)[:5],"%)"
    return x,y
def pre(path):
    #读取图片、预处理，返回dict的list
    
    #二值化去噪中值滤波
    im=Image.open(path).convert('L').filter(ImageFilter.MedianFilter())
    width,height = im.size
    image = Image.new('L',(width,height),255)

    pix=im.load()
    newpix=image.load()
    for y in range(height):
        for x in range(width):
            if pix[x,y]<90:
                newpix[x,y]=0
            else:
                newpix[x,y]=255
    image=yq(image)
    #image.save(savepath)


    #统计直方图并切割图片
    zf=[0]*width
    result=[]
    for i in range(width):
        for j in range(60):
            if newpix[i,j]==0:
                zf[i]+=1
    lastpos=2
    last=0
    for i in range(2,width):
        if zf[i]==0 or i==width-1:
            if last!=0 and i-lastpos>4:
                smallimg=cutpic(image,lastpos,i)
                result.append(smallimg)
                #smallimg.save(str(i)+".bmp")
            lastpos=i
        last=zf[i]

    #print len(result)
    
    #返回图像列表
    rval=[]
    for i in result:
        w,h=i.size
        tmplist={}
        cou=1
        timg=i.load()
        for ww in range(w):
            for hh in range(h):
                tmplist[cou]=timg[ww,hh]
                cou+=1
        rval.append(tmplist)
    return rval


def train(traindata,testdata):
    #读取文本文件和图像文件并生成libsvm训练数据进行训练
    
    x,y=predata(traindata)
    #pickle.dump([x,y],open("data/alldata","w"))
    #[x,y]=pickle.load(open("data/alldata", "r"))
    xt,yt=predata(testdata)
    m = svm_train(y, x, '-c 10')
    svm_predict(yt,xt,m)

    #保存模型
    global model
    model=m
    svm_save_model("data/model",m)
    return m

def predict(filepath):
    #读取指定文件返回识别结果

    #读取模型
    global model
    if isinstance(model,int):
        model=svm_load_model("data/model")
    x=pre(filepath)
    p_labels=svm_predict([0]*len(x), x, model, "-q")[0]
    res="".join([trans(i) for i in p_labels])
    return res
    


#train("data/traindata.csv","data/testdata.csv")
#predict("pic/pic3.jpg")
#predict("pic/pic4.jpg")
