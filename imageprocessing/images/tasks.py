from celery import shared_task
from PIL import Image
from django.core.files.base import ContentFile
from io import BytesIO
from .models import Image as ImageModel
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def resize_image(original_image, size):
    """
    Resize the image to the specified size and return the resized image.
    """
    image = Image.open(original_image)
    image = image.resize(size, Image.ANTIALIAS)
    buffer = BytesIO()
    image.save(buffer, format='JPEG')
    return ContentFile(buffer.getvalue())

@shared_task
def add_thumbs(image_id):
    channel_layer = get_channel_layer()
    try:
        image_instance = ImageModel.objects.get(id=image_id)
        image_instance.state = 'processing'
        image_instance.save()

        # Send 'processing' status update
        async_to_sync(channel_layer.group_send)(
            f'project_{image_instance.project_id}',
            {
                'type': 'project_update',
                'status': 'processing',
            }
        )

        original_image = image_instance.original

        sizes = {
            'thumb': (150, 120),
            'big_thumb': (700, 700),
            'big_1920': (1920, 1080),
            'd2500': (2500, 2500),
        }

        for field, size in sizes.items():
            resized_image = resize_image(original_image, size)
            getattr(image_instance, field).save(f"{image_instance.filename}_{field}.jpg", resized_image)

        image_instance.state = 'done'
        image_instance.save()

        # Send 'done' status update
        async_to_sync(channel_layer.group_send)(
            f'project_{image_instance.project_id}',
            {
                'type': 'project_update',
                'status': 'done',
            }
        )

    except Exception as e:
        image_instance.state = 'error'
        image_instance.save()

        # Send 'error' status update
        async_to_sync(channel_layer.group_send)(
            f'project_{image_instance.project_id}',
            {
                'type': 'project_update',
                'status': 'error',
            }
        )
        raise e
