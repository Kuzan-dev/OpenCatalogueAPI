from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.files.storage import default_storage
from django.conf import settings
import os
from .models import Product, Image
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Product)
def move_product_images_post_save(sender, instance, **kwargs):
    print(f"Ejecutando move_product_images_post_save para el producto: {instance.id}")
    try:
        move_product_images(instance)
    except Exception as e:
        print(f"Error en move_product_images_post_save: {e}")
        logger.error(f"Error en move_product_images_post_save: {e}")

@receiver(m2m_changed, sender=Product.images.through)
def move_product_images_m2m_changed(sender, instance, action, **kwargs):
    if action == "post_add":
        print(f"Ejecutando move_product_images_m2m_changed para el producto: {instance.id}")
        try:
            move_product_images(instance)
        except Exception as e:
            print(f"Error en move_product_images_m2m_changed: {e}")
            logger.error(f"Error en move_product_images_m2m_changed: {e}")

def move_product_images(instance):
    images = instance.images.all()
    print(f"Imágenes asociadas con el producto {instance.id}: {[image.file.name for image in images]}")

    for image in images:
        old_path = image.file.name
        old_full_path = default_storage.path(old_path)
        print(f"Ruta completa del archivo: {old_full_path}")

        new_path = f"product/{instance.identifier}/{os.path.basename(old_path)}"
        new_full_path = default_storage.path(new_path)
        print(f"Moviendo archivo: {old_full_path} a {new_full_path}")

        if default_storage.exists(old_path):
            try:
                with open(old_full_path, 'rb') as file:
                    file_content = file.read()

                os.makedirs(os.path.dirname(new_full_path), exist_ok=True)

                with open(new_full_path, 'wb') as new_file:
                    new_file.write(file_content)

                os.remove(old_full_path)

                image.file.name = new_path
                image.save()
            except Exception as e:
                print(f"Error moviendo el archivo: {e}")
                logger.error(f"Error moviendo el archivo: {e}")
        else:
            print(f"Archivo no encontrado: {old_path}")
            logger.error(f"Archivo no encontrado: {old_path}")
