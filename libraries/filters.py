from .models import Branch
import django_filters as filters

class BranchFilter(filters.FilterSet):
    category = filters.CharFilter(field_name='branch_books__book__category__name', lookup_expr='exact')
    author = filters.CharFilter(field_name='branch_books__book__author__name', lookup_expr='exact')


    class Meta:
        model = Branch
        fields = ['category','author']