from django.urls import path
from .views import *


urlpatterns = [
    path('', api_root),
    path('readers/', ReaderList.as_view(), name = 'readers-list' ),
    path('readers/<int:pk>/', ReaderUpdate.as_view(), name = 'reader-detail'),
    path('books/', BookList.as_view(), name = 'books-list' ),
    path('books/<int:pk>/', BookUpdate.as_view(), name = 'book-detail'),
    path('books/export.csv', toCsv)
]
