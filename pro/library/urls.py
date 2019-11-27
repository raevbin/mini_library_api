from django.urls import path
from .views import ReaderList, ReaderUpdate, BookList, BookUpdate
from .views import to_csv, api_root

urlpatterns = [
    path('', api_root),
    path('readers/', ReaderList.as_view(), name='readers-list'),
    path('readers/<int:pk>/', ReaderUpdate.as_view(), name='reader-detail'),
    path('books/', BookList.as_view(), name='books-list'),
    path('books/<int:pk>/', BookUpdate.as_view(), name='book-detail'),
    path('books/export.csv', to_csv)
]
