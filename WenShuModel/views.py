from django.shortcuts import render

# Create your views here.
import json
from WenShuModel.models import Wenshu
from django.http import HttpResponse
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

