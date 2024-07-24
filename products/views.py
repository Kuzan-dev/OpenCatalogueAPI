# views.py
from rest_framework import viewsets
from .models import Product, Image
from rest_framework.permissions import AllowAny
from .serializers import ProductSerializer, ImageSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer