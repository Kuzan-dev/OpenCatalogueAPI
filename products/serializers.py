from rest_framework import serializers
from .models import Image, Product, Price, Tag, Material
import json

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['id', 'name']
class PriceSerializer(serializers.ModelSerializer):
    material = MaterialSerializer() # Permite aniadir un objeto de tipo Material
    class Meta:
        model = Price
        fields = ['id', 'description', 'price', 'material']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['file']

class ProductWriteSerializer(serializers.ModelSerializer):
    images = serializers.ListField(child=serializers.FileField(), write_only=True, required=False)

    #si trabajaramos con json usariamos: tags = TagSerializer(many=True)
    tags = serializers.CharField(write_only=True, required=False) 
    #Si trabajaramos con json usariamos: prices = PriceSerializer(many=True)
    prices = serializers.CharField(write_only=True, required=False)
    
    class Meta:
      model = Product
      fields = ['id', 'name', 'link', 'description', 'images', 'identifier', 'rating', 'delivery', 'stock', 'available', 'tags', 'prices']

    def create(self, validated_data):
      images_data = validated_data.pop('images', [])
      tags_data = validated_data.pop('tags', [])
      prices_data = validated_data.pop('prices', [])

      # Convertir las cadenas de texto JSON a listas
      tags_data = json.loads(tags_data) if tags_data else []
      prices_data = json.loads(prices_data) if prices_data else []
      
      # Creo el producto
      product = Product.objects.create(**validated_data)

      # Agrego los precios
      for price in prices_data:
        # Extraigo el material
        material_data = price.pop('material')
        # Creo el material si no existe (get_or_create : Busca, si no lo encuentra lo crea)
        material, created = Material.objects.get_or_create(name=material_data['name'])
        # Creo una instancia de Price usando el material(creado o encontrado) y los datos del precio
        price = Price.objects.create(material=material, **price)
        # Agrego el precio al producto
        product.prices.add(price)

      # Agrego los tags
      for tag_data in tags_data:
        tag_name = tag_data['name']
        tag , created = Tag.objects.get_or_create(name=tag_name)
        product.tags.add(tag)
      
      # Agrego las imagenes
      for image in images_data:
        image_instance = Image.objects.create(file=image)
        product.images.add(image_instance)
        
      return product

    def update(self, instance, validated_data):
      images_data = validated_data.pop('images', [])
      tags_data = validated_data.pop('tags', [])
      prices_data = validated_data.pop('prices', [])

      # Convertir las cadenas de texto JSON a listas
      tags_data = json.loads(tags_data) if tags_data else []
      prices_data = json.loads(prices_data) if prices_data else []

      # Actualizo el producto
      instance = super().update(instance, validated_data)
        
      # Elimino las imagenes anteriores
      instance.images.clear()
        
      # Agrego las nuevas imagenes
      for image in images_data:
        image_instance = Image.objects.create(file=image)
        instance.images.add(image_instance)  

      # Elimino los tags
      instance.tags.clear()

      # Agrego los tags	nuevos
      for tag_data in tags_data:
        tag_name = tag_data['name']
        tag_instance, created = Tag.objects.get_or_create(name=tag_name)
        instance.tags.add(tag_instance)
      
      # Elimino los precios
      instance.prices.clear()

      # Agrego los precios nuevos
      for price_data in prices_data:
        # Extraigo el material
        material_data = price_data.pop('material')
        # Creo el material si no existe (get_or_create : Busca, si no lo encuentra lo crea)
        material, created = Material.objects.get_or_create(name=material_data['name'])
        # Creo una instancia de Price usando el material (creado o encontrado) y los datos del precio
        price_instance = Price.objects.create(material=material, **price_data)
        # Agrego el precio al producto
        instance.prices.add(price_instance)
      
      return instance