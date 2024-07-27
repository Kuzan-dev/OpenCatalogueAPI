from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.files.storage import default_storage
from django.conf import settings
import os
from .models import Product, Image
import logging

logger = logging.getLogger(__name__)

def move_image(file, new_path):
    """
    Mueve una imagen al nuevo path especificado.
    """
    old_path = file.name
    old_full_path = default_storage.path(old_path)
    print(f"Ruta completa del archivo: {old_full_path}")

    # Define la nueva ruta completa
    new_full_path = default_storage.path(new_path)
    print(f"Moviendo archivo: {old_full_path} a {new_full_path}")

    # Si el archivo ya existe en la nueva ubicación, lo elimina
    if default_storage.exists(new_full_path):
        default_storage.delete(new_full_path)

    # Mueve el archivo
    if default_storage.exists(old_path):
        try:
            with default_storage.open(old_path, 'rb') as src:
                file_content = src.read()
            
            os.makedirs(os.path.dirname(new_full_path), exist_ok=True)
            
            with default_storage.open(new_path, 'wb') as dst:
                dst.write(file_content)
            
            default_storage.delete(old_path)
            print(f"Imagen movida a: {new_path}")
        except Exception as e:
            print(f"Error moviendo el archivo: {e}")
            logger.error(f"Error moviendo el archivo: {e}")
    else:
        print(f"Archivo no encontrado: {old_path}")
        logger.error(f"Archivo no encontrado: {old_path}")

@receiver(post_save, sender=Product)
def move_product_images_post_save(sender, instance, **kwargs):
    """
    Signal handler para el modelo Product.
    Se ejecuta después de guardar un producto.
    """
    print(f"Ejecutando move_product_images_post_save para el producto: {instance.id}")
    try:
        move_product_images(instance)
    except Exception as e:
        print(f"Error en move_product_images_post_save: {e}")
        logger.error(f"Error en move_product_images_post_save: {e}")

@receiver(m2m_changed, sender=Product.images.through)
def move_product_images_m2m_changed(sender, instance, action, **kwargs):
    """
    Signal handler para el modelo Product.
    Se ejecuta después de añadir o eliminar imágenes del producto.
    """
    if action == "post_add":
        print(f"Ejecutando move_product_images_m2m_changed para el producto: {instance.id}")
        try:
            move_product_images(instance)
        except Exception as e:
            print(f"Error en move_product_images_m2m_changed: {e}")
            logger.error(f"Error en move_product_images_m2m_changed: {e}")

def move_product_images(instance):
    """
    Mueve las imágenes asociadas a un producto.
    """
    images = instance.images.all()
    print(f"Imágenes asociadas con el producto {instance.id}: {[image.file.name for image in images]}")

    for image in images:
        # Define el nuevo path donde se moverá la imagen
        new_path = f"product_images/{instance.id}/{os.path.basename(image.file.name)}"
        move_image(image.file, new_path)