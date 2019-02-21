from django.test import TestCase

# Create your tests here.
import json
from WenShuModel.models import Wenshu
def add_data(inputpath):
    fin=open(inputpath,'r',encoding='utf8')
    line=fin.readline()
    while line:
        line_temp=line.replace("\n","")
        d=json.loads(line_temp)
        wenshu_id=d['id']
        accu = d['accu']
        law='#'.join(d['law'])
        lda_vector="#".join(d['lda_vector'])
        one_text=Wenshu(wenshu_id=wenshu_id,accu=accu,law=law,topic_vector=lda_vector)
        one_text.save()
        line=fin.readline()
    fin.close()