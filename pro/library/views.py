import csv
from rest_framework import generics, viewsets
from .serializers import ReaderDetail, BookDetail
from .models import Reader, Book
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import status

import logging
logger = logging.getLogger('log')



@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'readers': reverse('readers-list', request=request, format=format),
        'books': reverse('books-list', request=request, format=format),
    })



class ReaderList(generics.ListCreateAPIView):
    serializer_class = ReaderDetail
    queryset = Reader.objects.all()


class ReaderUpdate(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReaderDetail
    queryset = Reader.objects.all()

    def delete(self, request, *args, **kwargs):
        booksList = Book.objects.filter(reader=kwargs.get('pk'))
        booksListSer = BookDetail(booksList,many=True,context={'request': request})
        if len(booksListSer.data):
            data = {"detail":"not delete. that object is associated with others",
                    'result': booksListSer.data}
            return Response(data,status=status.HTTP_423_LOCKED)
        return self.destroy(request, *args, **kwargs)

class BookList(generics.ListCreateAPIView):
    serializer_class = BookDetail

    def get_queryset(self):
        id = self.request.query_params.get('reader')
        if id:
            return Book.objects.filter(reader=id)
        else:
            return Book.objects.all()


class BookUpdate(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookDetail
    queryset = Book.objects.all()


def toCsv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="export.csv"'

    csv.register_dialect('custom', delimiter=';')
    writer = csv.writer(response,dialect='custom')

    writer.writerow([ 'bid','author','name','rid','reader'])

    for row in Book.objects.all():
        rowList = []
        for  field in Book._meta.fields:
            fieldObj = getattr(row, field.name)
            if type(fieldObj).__name__=='Reader':
                rowList.append(fieldObj.pk)
                rowList.append(fieldObj.name)
            else:
                rowList.append(fieldObj)
        writer.writerow(rowList)

    return response
