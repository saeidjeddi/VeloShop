from django.db.models.signals import post_delete
from django.dispatch import receiver

from products.models import ProductVideoModel, ProductImageModel, ProductAudioModel, ProductModel


@receiver(post_delete, sender=ProductModel)
def delete_product_image_file(sender, instance, **kwargs):

    if instance.image:
        instance.image.delete(save=False)


@receiver(post_delete, sender=ProductAudioModel)
def delete_product_audio_file(sender, instance, **kwargs):
    if instance.audio:
        instance.audio.delete(save=False)

@receiver(post_delete, sender=ProductVideoModel)
def delete_product_video_file(sender, instance, **kwargs):
    if instance.video:
        instance.video.delete(save=False)


@receiver(post_delete, sender=ProductImageModel)
def delete_product_images_file(sender, instance, **kwargs):
    if instance.image_slider:
        instance.image_slider.delete(save=False)