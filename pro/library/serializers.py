from rest_framework import serializers
from pro.settings import VERSION_API
from .models import Book, Reader
import logging
logger = logging.getLogger('log')



if VERSION_API==1:
    CurrentModel = serializers.ModelSerializer
else:
    CurrentModel = serializers.HyperlinkedModelSerializer

class ReaderDetail(CurrentModel):

    class Meta:
        model = Reader
        fields = '__all__'

class BookDetail(CurrentModel):

    class Meta:
        model = Book
        fields = '__all__'
