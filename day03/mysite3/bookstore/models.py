from django.db import models

# Create your models here.
class Book(models.Model):
    #创建类属性，每一个类属性 就是数据表中的一个字段【列】 varchar（30）
    title = models.CharField(max_length=30, verbose_name='书名')
    # 00000.00
    price = models.DecimalField('定价', max_digits=7, decimal_places=2, default=0.0)
    #新添加字段 desc
    desc = models.CharField(max_length=200, default='This is a good book!')

