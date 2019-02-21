# -*- coding: UTF-8 -*-
import json

def get_normal_law(path):
    fin=open(path,'r',encoding='utf8')
    law_whole=[]
    line=fin.readline()
    while line:
        line_temp=line.replace("\n","")
        law_whole.append(line_temp)
        line=fin.readline()
    return law_whole

def get_normal_accu(path):
    fin = open(path, 'r', encoding='utf8')
    accu_whole = []
    line = fin.readline()
    while line:
        line_temp = line.replace("\n", "")
        accu_whole.append(line_temp)
        line = fin.readline()
    return accu_whole

def getNormaldata_sheet2(inputpath,outputpath):
    fin=open(inputpath,'r',encoding='utf8')
    fout=open(outputpath,'w',encoding='utf8')
    line=fin.readline()
    while line:
        print("下一行")
        one_text={}
        line_temp=line.replace("\n","")
        d=json.loads(line_temp)
        one_text['fact']=d['fact']
        law_one_text=[]
        for e in d['law']:
            if e in law_whole:
                law_one_text.append(e)
        one_text['law']=law_one_text
        json.dump(one_text,fout,ensure_ascii=False)
        fout.write('\n')
        line=fin.readline()
    fin.close()
    fout.flush()
    fout.close()

def filt_accu():
    fin=open("D:/fengyi/law_and_accu/accu.txt",'r',encoding='utf8')
    fout=open("D:/fengyi/law_and_accu/accu_last.txt",'w',encoding='utf8')
    line=fin.readline()
    accu=[]
    while line:
        line_temp=line.replace("\n","")
        if line_temp not in accu:
            accu.append(line_temp)
        line=fin.readline()
    for e in accu:
        fout.write(e)
        fout.write('\n')
    fin.close()
    fout.flush()
    fout.close()


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


def getNormaldata_sheet4(inputpath,outputpath):
    fin=open(inputpath,'r',encoding='utf8')
    fout=open(outputpath,'w',encoding='utf8')
    line=fin.readline()
    while line:
        print("下一个")
        one_text={}
        line_temp=line.replace("\n","")
        d=json.loads(line_temp)
        one_text['fact'] = d['fact']
        one_text['id']=d['id']
        one_text['lda_vector']=d['lda_vector']
        law_one_text = []
        for e in d['law']:
            if e in law_whole:
                law_one_text.append(e)
        one_text['law'] = law_one_text

        if d['accu'] in accu_whole:
            one_text['accu']=d['accu']
        else:
            edit_distance=[]
            for e in accu_whole:
                distance=getEditDistance(d['accu'],e)
                edit_distance.append(distance)
            index=edit_distance.index(min(edit_distance))
            one_text['accu']=accu_whole[index]
        json.dump(one_text, fout, ensure_ascii=False)
        fout.write('\n')
        line=fin.readline()
    fin.close()
    fout.flush()
    fout.close()


law_whole=get_normal_law("D:/fengyi/law_and_accu/law.txt")
accu_whole=get_normal_accu("D:/fengyi/law_and_accu/accu.txt")

if __name__=='__main__':
    #getNormaldata_sheet2("D:/fengyi/sheetWith2.json","D:/fengyi/normalData/sheetWith2.json")
    getNormaldata_sheet4("D:/fengyi/sheetWith4.json","D:/fengyi/normalData/sheetWith4.json")