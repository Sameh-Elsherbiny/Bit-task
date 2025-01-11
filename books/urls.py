from django.urls import path
from .views import AuthorList, BookList , AuthorDetailsList , BorrowedBookList, BookBorrowedUpdate

urlpatterns = [
    path('authors/', AuthorList.as_view(), name='author-list'),
    path('books/', BookList.as_view(), name='book-list'),
    path('author-details/', AuthorDetailsList.as_view(), name='author-details-list'),
    path('borrowed-books/', BorrowedBookList.as_view(), name='borrowed-books-list'),
    path('borrowed-books/<int:pk>/', BookBorrowedUpdate.as_view(), name='borrowed-books-update'),
    
]