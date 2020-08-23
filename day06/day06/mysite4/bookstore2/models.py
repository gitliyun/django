from django.db import models
#一对一

# Create your models here.
class Author(models.Model):

    name = models.CharField(max_length=20, verbose_name='姓名')

class Wife(models.Model):

    name = models.CharField(max_length=20, verbose_name='姓名')
    author = models.OneToOneField(Author)








