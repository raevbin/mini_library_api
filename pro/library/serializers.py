import logging

from rest_framework import serializers
from .models import Book, Reader

logger = logging.getLogger('log')


class ReaderDetail(serializers.ModelSerializer):

    class Meta:
        model = Reader
        fields = ['url', 'id', 'name']


class BookDetail(serializers.ModelSerializer):
    reader_name = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['url', 'id', 'author', 'name', 'reader', 'reader_name']

    def get_reader_name(self, obj):
        if obj.reader:
            return obj.reader.name
        else:
            return None
