from rest_framework import serializers
from .models import Image, Product

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['file']

class ProductSerializer(serializers.ModelSerializer):
    images = serializers.ListField(child=serializers.FileField(), write_only=True, required=False)

    class Meta:
      model = Product
      fields = ['id', 'name', 'link', 'description', 'images', 'identifier']

    def create(self, validated_data):
      images_data = validated_data.pop('images', [])
      product = Product.objects.create(**validated_data)
        
      for image in images_data:
        image_instance = Image.objects.create(file=image)
        product.images.add(image_instance)
        
      return product

    def update(self, instance, validated_data):
      images_data = validated_data.pop('images', [])
      instance = super().update(instance, validated_data)
        
      # Clear existing images
      instance.images.clear()
        
      # Add new images
      for image in images_data:
        image_instance = Image.objects.create(file=image)
        instance.images.add(image_instance)     
      
      return instance