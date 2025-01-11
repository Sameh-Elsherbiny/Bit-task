from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import Branch, Library

class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = '__all__'

class BranchSerializer(serializers.ModelSerializer):
    library_name = serializers.CharField(source='library.name', read_only=True)
    distance = serializers.SerializerMethodField()
    class Meta:
        model = Branch
        exclude = ['location']

    def get_distance(self, obj):
        distance = obj.location.distance(self.context.get('request').user.location)
        return distance
    
