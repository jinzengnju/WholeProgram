# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import render
from Model.modelFromCkpt import *

# 表单
def search_form(request):
    return render_to_response('index1.html')

# 接收请求数据

model,sess,lda,dictionary,vocab_dict=build_graph()

context={}
def search(request):
    print(request)
    message=request.GET.get("fact")
    if message!=None:
        res_temp=predict(model,sess,message,dictionary,lda,vocab_dict)
        res=[lawname[e] for e in res_temp]
        context['first'] = res[0]
        context['second'] = res[1]
        context['third'] = res[2]
        context['forth'] = res[3]
        context['fifth'] = res[4]
        context['last'] = res[5]
        context['7th']=res[6]
        context['8th']=res[7]
        context['9th']=res[8]
        context['10th']=res[9]
        context['11th']=res[10]
        context['12th']=res[11]
    else:
        context['first'] = '你提交了空表单'
        context['second'] = '你提交了空表单'
        context['third'] = '你提交了空表单'
        context['forth'] = '你提交了空表单'
        context['fifth'] = '你提交了空表单'
        context['last'] = '你提交了空表单'
        context['7th'] = '你提交了空表单'
        context['8th'] = '你提交了空表单'
        context['9th'] = '你提交了空表单'
        context['10th'] = '你提交了空表单'
        context['11th'] = '你提交了空表单'
        context['12th'] = '你提交了空表单'
    return HttpResponse(json.dumps({
        "status": 1
    }))

def get_lawresult(request):
    return render(request, 'result_law.html', context)
    # def hello(request):
    #     context = {}
    #     context['hello'] = 'Hello World!'
    #     return render(request, 'hello.html', context)
    #应该修改为return render(request, 'result_law.html', context)