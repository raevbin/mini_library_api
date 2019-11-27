import csv
import logging

from rest_framework import generics, viewsets
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import status

from .serializers import ReaderDetail, BookDetail
from .models import Reader, Book


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
        books_list = Book.objects.filter(reader=kwargs.get('pk'))
        books_list_ser = BookDetail(books_list, many=True,
                                    context={'request': request})
        if len(books_list_ser.data):
            data = {
                "detail": "not delete. that object is associated with others",
                'result': books_list_ser.data
                }
            return Response(data, status=status.HTTP_423_LOCKED)
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


def to_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="export.csv"'

    csv.register_dialect('custom', delimiter=';')
    writer = csv.writer(response, dialect='custom')

    writer.writerow(['bid', 'author', 'name', 'rid', 'reader'])

    for row in Book.objects.all():
        row_list = []
        for field in Book._meta.fields:
            field_obj = getattr(row, field.name)
            if type(field_obj).__name__ == 'Reader':
                row_list.append(field_obj.pk)
                row_list.append(field_obj.name)
            else:
                row_list.append(field_obj)
        writer.writerow(row_list)

    return response
