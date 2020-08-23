from django.db import models

# Create your models here.
#多对多
class Author(models.Model):

    name = models.CharField(max_length=20, verbose_name='作者')

    def __str__(self):
        return '作者： %s' %(self.name)

class Book(models.Model):

    title = models.CharField(max_length=30, verbose_name='书名')
    #创建多对多关联
    author = models.ManyToManyField(Author)

    def __str__(self):
        return '书名: %s'%(self.title)










