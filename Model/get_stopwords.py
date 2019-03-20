#!/usr/bin/python
# -*- coding:UTF-8 -*-
def get_stopwords():
    print("加载停用词...............")
    fin=open("D:/fengyi/normalData/stopwords.txt",'r',encoding='utf8')
    stopwords_temp=[]
    line=fin.readline()
    while line:
        line=line.replace("\n","")
        if line in stopwords_temp:
            line=fin.readline()
            continue
        line=fin.readline()
    return stopwords_temp
stopwords=get_stopwords()