from rest_framework import viewsets, permissions
from .models import (
    BreederProfile, VeterinarianProfile, BuyerProfile, 
    Consultation, PigListing, Transaction, BlogPost, Comment, Message
)
from .serializers import (
    BreederProfileSerializer, VeterinarianProfileSerializer, BuyerProfileSerializer, 
    ConsultationSerializer, PigListingSerializer, TransactionSerializer, 
    BlogPostSerializer, CommentSerializer, MessageSerializer
)


class BreederProfileViewSet(viewsets.ModelViewSet):
    queryset = BreederProfile.objects.all()
    serializer_class = BreederProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


class VeterinarianProfileViewSet(viewsets.ModelViewSet):
    queryset = VeterinarianProfile.objects.all()
    serializer_class = VeterinarianProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


class BuyerProfileViewSet(viewsets.ModelViewSet):
    queryset = BuyerProfile.objects.all()
    serializer_class = BuyerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


class ConsultationViewSet(viewsets.ModelViewSet):
    queryset = Consultation.objects.all()
    serializer_class = ConsultationSerializer
    permission_classes = [permissions.IsAuthenticated]


class PigListingViewSet(viewsets.ModelViewSet):
    queryset = PigListing.objects.all()
    serializer_class = PigListingSerializer
    permission_classes = [permissions.IsAuthenticated]


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]


class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAuthenticated]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
