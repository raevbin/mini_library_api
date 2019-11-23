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
        fields = ['url','id','name']

class BookDetail(CurrentModel):
    reader_name = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['url','id','author','name','reader','reader_name']

    def get_reader_name(self,obj):
        if obj.reader:
            return obj.reader.name
        else:
            return None
