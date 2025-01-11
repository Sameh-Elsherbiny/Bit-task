from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Book, Author, BorrowedBook
from rest_framework.response import Response
from django.db.models import Count, Q
from .serializers import BookSerializer, AuthorSerializer, AuthorDetailSerializer, BorrowedBookSerializer
from .filters import BookFilter, AuthorFilter , SimpleAuthorFilter
from django_filters.rest_framework import DjangoFilterBackend


class AuthorList(generics.ListAPIView):
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = SimpleAuthorFilter
    queryset = Author.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        library = self.request.query_params.get("library")
        category = self.request.query_params.get("category")

        book_filter = Q()
        if library:
            book_filter &= Q(books__book_branches__branch__library__name=library)
        if category:
            book_filter &= Q(books__category__name=category)

        return queryset.annotate(book_count=Count("books", filter=book_filter))


class BookList(generics.ListAPIView):
    queryset = Book.objects.select_related("author", "category").all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = BookFilter


class AuthorDetailsList(generics.ListAPIView):
    serializer_class = AuthorDetailSerializer
    permission_classes = [IsAuthenticated]  
    queryset = Author.objects.prefetch_related("books__category")
    # filter_backends = [DjangoFilterBackend]
    # filterset_class = AuthorFilter


class BorrowedBookList(generics.ListCreateAPIView):
    serializer_class = BorrowedBookSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):  # Schema generation fallback
            return BorrowedBook.objects.none()
        return self.request.user.borrowed_user.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BookBorrowedUpdate(generics.UpdateAPIView):
    serializer_class = BorrowedBookSerializer
    permission_classes = [IsAuthenticated]
    queryset = BorrowedBook.objects.all()
