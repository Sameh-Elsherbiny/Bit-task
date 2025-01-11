from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Branch
from .serializers import  BranchSerializer
from .filters import BranchFilter
from django_filters.rest_framework import DjangoFilterBackend


class BranchList(generics.ListAPIView):
    queryset = Branch.objects.all().select_related('library')
    serializer_class = BranchSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = BranchFilter


