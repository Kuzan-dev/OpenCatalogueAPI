from rest_framework import serializers
from .models import Product, Price, Material, Tag, Image

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ("__all_")

class MaterialSerializer(serializers.ModelSerializer):
  class Meta:
    model = Material
    fields = ("__all__")

class PriceSerializer(serializers.ModelSerializer):
  material = MaterialSerializer()
  class Meta:
    model = Price
    fields = ("__all__")

class TagSerializer(serializers.ModelSerializer):
  class Meta:
    model = Tag
    fields = ("__all__")

class ProductReadSerializer(serializers.ModelSerializer):
  tags = TagSerializer(many=True, read_only=True)
  prices = PriceSerializer(many=True, read_only=True)
  images = ImageSerializer(many=True, read_only=True)

  class Meta:
    model = Product
    fields = ("__all__")

class ProductCustomerReadSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    prices = PriceSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        exclude = ['link']

class ProductWriteSerializer(serializers.ModelSerializer):
  tag = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)
  prices = serializers.PrimaryKeyRelatedField(queryset=Price.objects.all(), many=True)
  images = ImageSerializer(many=True, required=False)
  
  class Meta:
    model = Product
    fields = ("__all__")
  
  def create(self, validated_data):
    #Extraemos(.pop) las imagenes, tags y precios del diccionario
    images_data = validated_data.pop('images', [])
    tags_data = validated_data.pop('tags', [])
    prices_data = validated_data.pop('prices', [])

    #Creamos una nueva instancia del producto
    product = Product.objects.create(**validated_data)
    #Agregamos los tags y precios al producto
    product.tags.set(tags_data)
    product.prices.set(prices_data)

    #Iteramos sobre las imagenes y creamos nuevas instancias de Image
    for image_data in images_data:
      #Creamos una nueva instancia de Image asociada con el product
      Image.objects.create(product=product, **image_data)
    return product

  def update(self, instance, validated_data):
    #Extrayendo la informacion de las imagenes, tags y precios
    images_data = validated_data.pop('images', [])
    tags_data = validated_data.pop('tags', [])
    prices_data = validated_data.pop('prices', [])

    #Actualizamos la instancia del producto con la informacion de validated_data
    instance = super().update(instance, validated_data)
    #Actualizamos los tags y precios del producto
    instance.tags.set(tags_data)
    instance.prices.set(prices_data)

    #Iterando sobre las imagenes en images_data
    for image_data in images_data:
      #Buscamos si ya existe una instancia de Image con el producto y la imagen
      image_instance = Image.objects.filter(product=instance, file = image_data.get('file')).first()
      if image_instance:
        #Actualizamos la imagen si ya existe
        for attr, value in image_data.items():
          setattr(image_instance, attr, value)
        image_instance.save()
      else:
        #Creamos una nueva instancia de Image si no existe
        Image.objects.create(product=instance, **image_data)
    return instance