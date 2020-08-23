from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=30, unique=True, verbose_name= '书名')
    pub = models.CharField(max_length=50, verbose_name='出版社')
    price = models.DecimalField(max_digits=7,  decimal_places=2,verbose_name='定价', default=8888)
    market_price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='零售价', default=8888)
    #伪删除
    #isActive = models.BooleanField(default=True)


    def __str__(self):

        return 'title：%s pub:%s price:%s'%(self.title, self.pub, self.price)

    class Meta:
        db_table = 'book'
        verbose_name = '书籍'
        verbose_name_plural = verbose_name








class Author(models.Model):

    name = models.CharField(max_length=30, verbose_name='姓名')
    age = models.IntegerField(verbose_name='年龄')
    email = models.EmailField(verbose_name='邮箱')

    def __str__(self):
        return '作者： %s'%(self.name)



class User(models.Model):

    username = models.CharField(max_length=20, verbose_name='用户名')
    password = models.CharField(max_length=32, verbose_name='密码')














