from rest_framework import serializers
from .models import *  # Assuming your models are in this module

# Career Serializer
class CareerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Careers
        fields = '__all__'  # Serialize all fields from the Careers model

# Client Serializer (Using ModelSerializer or HyperlinkedModelSerializer)
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'  # Or specify the fields you want to serialize explicitly

# Alternatively, using HyperlinkedModelSerializer for Client

# Mail Serializer (For sending emails)
class MailSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    subject = serializers.CharField(max_length=255)
    message = serializers.CharField()

# Careers Mail Serializer (For job applications)

class CareersMailSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField(required=True)
    JobName=serializers.CharField(max_length=255, required=True)
    resume = serializers.FileField(required=True)
    message=serializers.CharField(max_length=255, required=True)