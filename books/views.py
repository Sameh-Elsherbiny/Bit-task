from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Book, Author, BorrowedBook
from rest_framework.response import Response
from django.db.models import Count, Q
from .serializers import (
    BookSerializer,
    AuthorSerializer,
    AuthorDetailSerializer,
    BorrowedBookSerializer,
)
from .filters import BookFilter, AuthorFilter, SimpleAuthorFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.core.cache import cache


class AuthorList(generics.ListAPIView):
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = SimpleAuthorFilter
    queryset = Author.objects.all()

    def get_queryset(self):
        library = self.request.query_params.get("library")
        category = self.request.query_params.get("category")

        cache_key = f"author_list"
        cached_queryset = cache.get(cache_key)
        if cached_queryset:
            queryset = cached_queryset
        else:
            queryset = super().get_queryset()
            cache.set(cache_key, queryset, 60 * 60 * 24 * 30)

        book_filter = Q()
        if library:
            book_filter &= Q(books__book_branches__branch__library__name=library)
        if category:
            book_filter &= Q(books__category__name=category)

        queryset = queryset.annotate(book_count=Count("books", filter=book_filter))
        return queryset


class BookList(generics.ListAPIView):
    queryset = Book.objects.select_related("author", "category").all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = BookFilter

    def get_queryset(self):
        cache_key = f"book_list"
        cached_queryset = cache.get(cache_key)
        if cached_queryset:
            queryset = cached_queryset
        else:
            queryset = super().get_queryset()
            cache.set(cache_key, queryset, 60 * 60 * 24 * 30)
        return queryset


class AuthorDetailsList(generics.ListAPIView):
    serializer_class = AuthorDetailSerializer
    permission_classes = [IsAuthenticated]
    queryset = Author.objects.prefetch_related("books__category")
    filter_backends = [DjangoFilterBackend]
    filterset_class = AuthorFilter

    def get_queryset(self):
        cache_key = f"author_details_list"
        cached_queryset = cache.get(cache_key)
        if cached_queryset:
            queryset = cached_queryset
        else:
            queryset = super().get_queryset()
            cache.set(cache_key, queryset, 60 * 60 * 24 * 30)
        return queryset


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
