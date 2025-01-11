from django.urls import path
from .views import BranchList

urlpatterns = [
    path('branches/', BranchList.as_view(), name='branch-list'),
]