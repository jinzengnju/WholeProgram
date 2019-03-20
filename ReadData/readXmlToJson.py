# -*- coding: UTF-8 -*-
import os
from lxml import etree
import json
import jieba
import re
from Model.modelFromCkpt import get_topicVector,LdaModel,Dictionary

def getStopWords(path):
    fin=open(path,'r',encoding='utf8')
    stopwords=[]
    line=fin.readline()
    while line:
        line = line.replace("\n", "")
        if line in stopwords:
            line=fin.readline()
            continue
        stopwords.append(line)
        line=fin.readline()
    fin.close()
    return stopwords

def remove_stopwords(path,str):
    stopwords=getStopWords(path)
    text = re.sub('[^(\\u4e00-\\u9fa5)]', '', str)
    text = re.sub('(?i)[^a-zA-Z0-9\u4E00-\u9FA5]', '', text)
    res = jieba.cut(text)
    words=[]
    for e in res:
        if len(e)<2:
            continue
        if e in stopwords:
            continue
        words.append(e)
    return words

def readOneXml(filename):
    xml_file=etree.parse(filename)
    node1=xml_file.xpath("/writ/QW/AJJBQK/CMSSD")
    cmssd=""
    if node1:
        for e in node1:
            cmssd+=e.get("value")
    else:
        cmssd=xml_file.xpath("/writ/QW/AJJBQK")[0].get("value")
    node2=xml_file.xpath("/writ/QW/SSJL/AY")
    ay=node2[0].get("value")
    law=[]
    node3=xml_file.xpath("/writ/QW/CPFXGC/CUS_FLFT_FZ_RY/CUS_FLFT_RY")
    for node in node3:
        law_temp = node.get("value")
        try:
            if("诉讼" in law_temp):
                continue
            if("款" in law_temp):
                law_temp=law_temp[0:law_temp.index("款")]
                law_temp=law_temp[0:law_temp.rindex("第")]
            if("项" in law_temp):
                law_temp = law_temp[0:law_temp.index("项")]
                law_temp = law_temp[0:law_temp.rindex("第")]
            law.append(law_temp)
        except ValueError:
            law.append(law_temp)
            continue

    # words=remove_stopwords("D:/fengyi/normalData/stopwords.txt",cmssd)
    # print(words)
    # print("查明事实段：")
    # print(cmssd)
    # print()
    # print("案由：")
    # print(ay)
    # print()
    # print("引用法律法条：")
    # print(law)
    return cmssd,ay,law

def readOneDir(dir_value,foutWith2,foutWith4):
    dir=os.path.join(root_path,dir_value)
    for file in os.listdir(dir):
        one_textWith4={}
        one_textWith2={}
        file_name=os.path.join(dir,file)
        id=''.join([dir_value,file])[0:-4]
        print("dealing file %s"%id)
        cmssd,ay,law=readOneXml(file_name)
        if not (ay in accu_whole):
            accu_whole.append(ay)
        for e in law:
            if not (e in law_whole):
                law_whole.append(e)
        cmssd_list=[]
        cmssd_list.append(cmssd)
        topic_vector=get_topicVector(dictionary,cmssd_list,lda)[0].tolist()
        one_textWith4["id"]=id
        one_textWith4["fact"]=cmssd
        one_textWith4["accu"]=ay
        one_textWith4["law"]=law
        one_textWith4["lda_vector"]=topic_vector
        one_textWith2["fact"]=cmssd
        one_textWith2["accu"]=ay
        one_textWith2["law"]=law
        json.dump(one_textWith2,foutWith2,ensure_ascii=False)
        json.dump(one_textWith4,foutWith4,ensure_ascii=False)
        foutWith2.write('\n')
        foutWith4.write('\n')
    foutWith4.flush()
    foutWith2.flush()

law_whole=[]
accu_whole=[]
root_path="D:/fengyi/冯奕数据"
lda = LdaModel.load("D:/LDA/model")
dictionary = Dictionary.load("D:/LDA/dict")
lda.__setattr__("minimum_probability", 0)

if __name__=='__main__':
    # dirs = ['a', 'b', 'c', 'd', 'e', 'f']
    # # dirs = ['temp', 'temp1', 'temp2']
    # foutWith2=open("D:/fengyi/sheetWith2.json",'w',encoding='utf8')
    # foutWith4=open("D:/fengyi/sheetWith4.json",'w',encoding='utf8')
    # for dir in dirs:
    #     readOneDir(dir,foutWith2,foutWith4)
    # foutWith2.close()
    # foutWith4.close()
    # f_law=open("D:/fengyi/law_and_accu/law.txt",'w',encoding='utf8')
    # f_accu=open("D:/fengyi/law_and_accu/accu.txt",'w',encoding='utf8')
    # for e in law_whole:
    #     f_law.write(e)
    #     f_law.write('\n')
    # f_law.close()
    # for e in accu_whole:
    #     f_accu.write(e)
    #     f_accu.write('\n')
    # f_accu.close()
    readOneXml("D:/fengyi/冯奕数据/temp/11389.xml")
