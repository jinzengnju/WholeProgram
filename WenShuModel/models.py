from django.db import models

# Create your models here.
from django.db import models
class Wenshu(models.Model):
    # 文书id为主键，并且会自增
    # 文书案由
    # 文书法条
    # 文书lda向量
    class Meta:
        db_table='wenshu_table'
    wenshu_id=models.CharField(max_length=20)
    accu=models.CharField(max_length=200)
    law=models.TextField()
    topic_vector=models.TextField()

class Wenshu_Id_Filename(models.Model):
    class Meta:
        db_table = 'id_filename'
    wenshu_id = models.CharField(max_length=20)
    wenshu_filename=models.CharField(max_length=200)