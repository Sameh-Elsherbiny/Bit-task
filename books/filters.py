from .models import Book , Author
import django_filters as filters

class BookFilter(filters.FilterSet):
    author = filters.CharFilter(field_name='author__name', lookup_expr='icontains')
    category = filters.CharFilter(field_name='category__name', lookup_expr='icontains')
    class Meta:
        model = Book
        fields = ['author', 'category']

class AuthorFilter(filters.FilterSet):
    library = filters.CharFilter(field_name='books__book_branches__branch__library__name', lookup_expr='exact')
    category = filters.CharFilter(field_name='books__category__name', lookup_expr='exact')

    
    class Meta:
        model = Author
        fields = ['library', 'category']

class SimpleAuthorFilter(filters.FilterSet):
    library = filters.CharFilter(method='filter_by_library')
    category = filters.CharFilter(method='filter_by_category')

    class Meta:
        model = Author
        fields = ['library', 'category']

    def filter_by_library(self, queryset, name, value):
        return queryset.filter(books__book_branches__branch__library__name=value)

    def filter_by_category(self, queryset, name, value):
        return queryset.filter(books__category__name=value)





