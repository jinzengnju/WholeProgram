# -*- coding: utf-8 -*-

from MyGraduate.search import lda,dictionary
from ReadData.NormalJson import get_normal_accu
from Model.modelFromCkpt import get_topicVector
from WenShuModel.models import Wenshu,Wenshu_Id_Filename
from django.http import HttpResponse
from django.shortcuts import render
import numpy as np
from lxml import etree
import json
import random
accu_normal=get_normal_accu("D:/fengyi/law_and_accu/accu.txt")
class Recommendfact:
    str_root_path="D:/fengyi/冯奕数据"
    context_wenshu = {}#id映射到ws_filename
    context_content={}
    htmlid_to_wenshuid = {}#id映射到wenshuid
    @staticmethod
    def getEditDistance(str1, str2):
        len_str1 = len(str1) + 1
        len_str2 = len(str2) + 1
        # create matrix
        matrix = [0 for n in range(len_str1 * len_str2)]
        # init x axis
        for i in range(len_str1):
            matrix[i] = i
        # init y axis
        for j in range(0, len(matrix), len_str1):
            if j % len_str1 == 0:
                matrix[j] = j // len_str1

        for i in range(1, len_str1):
            for j in range(1, len_str2):
                if str1[i - 1] == str2[j - 1]:
                    cost = 0
                else:
                    cost = 1
                matrix[j * len_str1 + i] = min(matrix[(j - 1) * len_str1 + i] + 1,
                                               matrix[j * len_str1 + (i - 1)] + 1,
                                               matrix[(j - 1) * len_str1 + (i - 1)] + cost)
        return matrix[-1]
    @staticmethod
    def cross_entropy(input_vector,db_vector_t):
        db_vector=np.array(db_vector_t)
        return -np.sum(input_vector*np.log(db_vector))

    @staticmethod
    def get_id_ws_filename(similarities_result):
        cnt = 1
        for e in similarities_result:
            wenshu_id = e[0]
            Recommendfact.htmlid_to_wenshuid[str(cnt) + "th"] = wenshu_id
            ws_filename = Wenshu_Id_Filename.objects.filter(wenshu_id=wenshu_id)
            Recommendfact.context_wenshu[str(cnt) + "th"] = ws_filename[0].wenshu_filename
            cnt += 1
        return

    @staticmethod
    def readoneXml(filename):
        xml_file = etree.parse(filename)
        node1 = xml_file.xpath("/writ/QW/AJJBQK/CMSSD")
        cmssd = ""
        if node1:
            for e in node1:
                cmssd += e.get("value")
        else:
            cmssd = xml_file.xpath("/writ/QW/AJJBQK")[0].get("value")
        node2 = xml_file.xpath("/writ/QW/SSJL/AY")
        ay = node2[0].get("value")
        law = []
        node3 = xml_file.xpath("/writ/QW/CPFXGC/CUS_FLFT_FZ_RY/CUS_FLFT_RY")
        for node in node3:
            law_temp = node.get("value")
            law.append(law_temp)
        law_str = '；'.join(law)
        node4 = xml_file.xpath("/writ/QW/CPFXGC")
        judge_context = ""
        if node4:
            judge_context = node4[0].get('value')
        else:
            judge_context = "没有找到判决结果"
        return cmssd, ay, judge_context, law_str


def search_wenshu(request):
    message = request.GET.get("fact")
    accu_temp=request.GET.get("accu")
    accu=""
    if accu_temp in accu_normal:
        accu=accu_temp
    else:
        edit_distance = []
        for e in accu_normal:
            distance = Recommendfact.getEditDistance(accu_temp, e)
            edit_distance.append(distance)
        index = edit_distance.index(min(edit_distance))
        accu = accu_normal[index]

    fact = []
    fact.append(message)
    topic_vector = get_topicVector(dictionary, fact, lda)[0]
    db_result=Wenshu.objects.filter(accu=accu)#限制了返回的数据
    length=db_result.count()
    rand_ids=random.sample(range(1,length),50)
    similarities={}
    for index in rand_ids:
        var=db_result[index]
        temp_string=var.topic_vector
        wenshu_id=var.wenshu_id
        temp_vector=[float(e) for e in temp_string.split('#')]
        simi=Recommendfact.cross_entropy(topic_vector,temp_vector)
        similarities[wenshu_id]=simi
    similarities_result=sorted(similarities.items(),key=lambda  x:x[1],reverse=True)
    Recommendfact.get_id_ws_filename(similarities_result)
    # context_wenshu['first'] = similarities_result[0][0]    #a1065
    # context_wenshu['second'] = similarities_result[1][0]
    # context_wenshu['third'] = similarities_result[2][0]
    # context_wenshu['forth'] = similarities_result[3][0]
    # context_wenshu['fifth'] = similarities_result[4][0]
    # context_wenshu['last'] = similarities_result[5][0]
    # context_wenshu['7th'] = similarities_result[6][0]
    # context_wenshu['8th'] = similarities_result[7][0]
    # context_wenshu['9th'] = similarities_result[8][0]
    # context_wenshu['10th'] = similarities_result[9][0]
    # context_wenshu['11th'] = similarities_result[10][0]
    # context_wenshu['12th'] = similarities_result[11][0]
    return HttpResponse(json.dumps({
        "status": 1
    }))




def get_factresult(request):
    return render(request, 'result_fact.html', Recommendfact.context_wenshu)

import os

def get_content(request):
    htmlid = request.GET.get("id")
    wenshuid=Recommendfact.htmlid_to_wenshuid[htmlid]
    print("文书的文件名id为：%s***********************"%wenshuid)
    filename=os.path.join(Recommendfact.str_root_path,wenshuid[0]+'/'+wenshuid[1:]+'.xml')
    cmssd, ay, judge_context, law_str=Recommendfact.readoneXml(filename)
    Recommendfact.context_content['title']=Recommendfact.context_wenshu[htmlid]
    Recommendfact.context_content['content']="查明事实："+cmssd
    Recommendfact.context_content['ay']="所属案由："+ay
    Recommendfact.context_content['CaiPanJieGuo']="判决结果："+judge_context
    Recommendfact.context_content['law']="引用法条："+law_str
    return HttpResponse(json.dumps({
        "status": 1
    }))

def show_content(request):
    return render(request,"content.html",Recommendfact.context_content)



