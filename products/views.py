from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Product, Tag, Price, Image, Material
from .permissions import IsAdmin
from .serializers import (
  ProductWriteSerializer, 
  TagSerializer, 
  PriceSerializer, 
  ImageSerializer, 
  MaterialSerializer, 
  ProductReadSerializer, 
  ProductReadAdminSerializer)

# Create your views here.
class ProductViewSet(viewsets.ModelViewSet):
  queryset = Product.objects.all()

  def get_serializer(self):
    if self.action in ("create", "update", "partial_update", "destroy"):
      return ProductWriteSerializer
    if self.request.user and self.request.user.is_superuser:
      return ProductReadAdminSerializer
    return ProductReadSerializer
  
  def get_permissions(self):
    if self.action in ("create",):
      self.permission_classes = (permissions.IsAuthenticated,)
    elif self.action in ("update", "partial_update", "destroy"):
      self.permission_classes = (IsAdmin,)
    else:
      self.permission_classes = (permissions.AllowAny,)
    return super().get_permissions()

class MaterialViewSet(viewsets.ModelViewSet):
  queryset = Material.objects.all()
  serializer_class = MaterialSerializer

class TagViewSet(viewsets.ModelViewSet):
  queryset = Tag.objects.all()
  serializer_class = TagSerializer

class PriceViewSet(viewsets.ModelViewSet):
  queryset = Price.objects.all()
  serializer_class = PriceSerializer

class ImageViewSet(viewsets.ModelViewSet):
  queryset = Image.objects.all()
  serializer_class = ImageSerializer