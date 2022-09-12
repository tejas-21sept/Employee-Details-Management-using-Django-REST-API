from rest_framework import serializers, status
from .models import User,Address,Experience,Qualifications,Projects

class AddressSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Address
        fields="__all__"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields="__all__"
        
class ExperienceSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Experience
        fields="__all__"

class QualificationsSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Qualifications
        fields="__all__"
        
class ProjectsSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Projects
        fields="__all__"