from django.db import models
from django.conf import settings

# Create your models here.

class Reader(models.Model):
    name = models.CharField(max_length=200, unique=True)
    def __str__(self):
        return self.name

class Book(models.Model):
    author = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    reader = models.ForeignKey(Reader,on_delete=models.DO_NOTHING, blank=True,
                                                                    null=True)

    def __str__(self):
        return '{0}-{1}'.format(self.author,self.name)
