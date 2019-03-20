from django.shortcuts import render

# Create your views here.
import json
from WenShuModel.models import Wenshu,Wenshu_Id_Filename
from django.http import HttpResponse
from lxml import etree
import os
import re

def add_data(inputpath):
    fin=open("D:/fengyi/normalData/sheetWith4.json",'r',encoding='utf8')
    line=fin.readline()
    count=0
    while line:
        count+=1
        print("第%d行"%count)
        line_temp=line.replace("\n","")
        d=json.loads(line_temp)
        wenshu_id=d['id']
        accu = d['accu']
        law='#'.join(d['law'])
        lda_vector=str("#".join(str(e) for e in d['lda_vector']))
        one_text=Wenshu(wenshu_id=wenshu_id,accu=accu,law=law,topic_vector=lda_vector)
        one_text.save()
        line=fin.readline()
    fin.close()
    print("完成")
    return HttpResponse("<p>数据添加成功</p>")

def readOneXml(filename):
    xml_file = etree.parse(filename)
    node1 = xml_file.xpath("/writ/QW/WS")
    ws_filename=node1[0].get('value')
    text = re.sub('(?i)[^a-zA-Z0-9\u4E00-\u9FA5]', '', ws_filename)
    return text

def readOneDir(dir_value):
    root_path = "D:/fengyi/冯奕数据"
    dir=os.path.join(root_path,dir_value)
    for file in os.listdir(dir):
        file_name=os.path.join(dir,file)
        print(file_name)
        wenshu_id=''.join([dir_value,file])[0:-4]
        ws_filename=readOneXml(file_name)
        try:
            one_text = Wenshu_Id_Filename(wenshu_id=wenshu_id, wenshu_filename=ws_filename)
            one_text.save()
        except AttributeError:
            continue

def write_filenameTo_db(request):
    dirs = ['a', 'b', 'c', 'd', 'e', 'f']
    for dir_value in dirs:
        readOneDir(dir_value)
    return HttpResponse("<p>数据添加成功</p>")

# if __name__=='__main__':
#     write_filenameTo_db()
    # return HttpResponse("<p>数据添加成功</p>")

