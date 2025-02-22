from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    BreederProfile, VeterinarianProfile, BuyerProfile, 
    Consultation, PigListing, Transaction, BlogPost, Comment, Message
)

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'phone_number', 'address', 'profile_picture']


class BreederProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = BreederProfile
        fields = '__all__'


class VeterinarianProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = VeterinarianProfile
        fields = '__all__'


class BuyerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = BuyerProfile
        fields = '__all__'


class ConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultation
        fields = '__all__'


class PigListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PigListing
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
