from django.db import models

# Create your models here.
#file:mysite3/bookstore

#定义一个类
class Book(models.Model):
    title = models.CharField(max_length=30,null=False,unique=True,verbose_name='书名')
    pub = models.CharField(max_length=50,null=True,verbose_name='出版社')
    price = models.DecimalField(decimal_places=2,max_digits=7,null=True,default='9999',verbose_name='定价')
    market_price = models.DecimalField(decimal_places=2,max_digits=7,default='9999',verbose_name='零售价')

class Aook(models.Model):
    title = models.CharField(max_length=30,null=False,unique=True,verbose_name='书名')
    pub = models.CharField(max_length=50,null=True,verbose_name='出版社')
    price = models.DecimalField(decimal_places=2,max_digits=7,null=True,default='9999',verbose_name='定价')
    market_price = models.DecimalField(decimal_places=2,max_digits=7,default='9999',verbose_name='零售价')
class Author(models.Model):
    # 定义一个姓名字段
    name = models.CharField(max_length=30,db_index=True,
                             verbose_name='姓名')#对应varchar(30)
    # 定义一个年龄字段
    age = models.IntegerField(default=1,
                            verbose_name='年龄')#对应Decimal(7,2)
    # 定义一个邮箱字段
    email = models.EmailField(max_length=100,
                              blank=True,
                              verbose_name='邮箱')