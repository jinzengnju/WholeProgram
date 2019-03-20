# -*- coding: UTF-8 -*-
import re
def write_whole_law(inputpath,outputpath):
    fin = open(inputpath, 'r', encoding='utf8')
    law_whole = []
    line = fin.readline()
    i=0
    while line:
        line_temp = line.replace("\n", "")
        if ("诉讼" in line_temp):
            line = fin.readline()
            continue
        line_temp=remove_special_char(line_temp)
        if line_temp not in law_whole:
            law_whole.append(line_temp)
        else:
            i+=1
            print(line_temp)
        line = fin.readline()
    fout=open(outputpath,'w',encoding='utf8')
    for e in law_whole:
        fout.write(e)
        fout.write('\n')
    fout.flush()
    fout.close()
    return law_whole

def remove_special_char(str):
    text = re.sub('[^(\\u4e00-\\u9fa5)]', '', str)
    text = re.sub('(?i)[^a-zA-Z0-9\u4E00-\u9FA5]', '', text)
    return text

def get_stopwords(inputpath,outputpath):
    fin=open(inputpath,'r',encoding='utf8')
    line=fin.readline()
    stopwords=[]
    while line:
        line=line.replace("\n","")
        line=fin.readline()


if __name__=='__main__':
    write_whole_law("D:/fengyi/law_fengyi/9722.txt","D:/fengyi/law_and_accu/9722.txt")
