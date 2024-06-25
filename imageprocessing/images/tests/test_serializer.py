from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from images.models import Image
from images.serializers import ImageSerializer, ImageListSerializer

class ImageSerializerTest(TestCase):

    def setUp(self):
        self.image_attributes = {
            'filename': 'test_image.jpg',
            'project_id': 1,
            'original': SimpleUploadedFile(name='original.jpg', content=b'', content_type='image/jpeg'),
            'thumb': SimpleUploadedFile(name='thumb.jpg', content=b'', content_type='image/jpeg'),
            'big_thumb': SimpleUploadedFile(name='big_thumb.jpg', content=b'', content_type='image/jpeg'),
            'big_1920': SimpleUploadedFile(name='big_1920.jpg', content=b'', content_type='image/jpeg'),
            'd2500': SimpleUploadedFile(name='d2500.jpg', content=b'', content_type='image/jpeg'),
            'state': 'init'
        }

        self.image = Image.objects.create(**self.image_attributes)
        self.serializer = ImageSerializer(instance=self.image)
        self.list_serializer = ImageListSerializer(instance=self.image)

    def test_fields_image(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['filename', 'project_id', 'original']))

    def test_fields_image_list(self):
        data = self.list_serializer.data
        self.assertEqual(set(data.keys()), set([
            'filename', 'project_id', 'original', 'thumb', 
            'big_thumb', 'big_1920', 'd2500', 'state'
        ]))

    def test_image_field_content(self):
        data = self.serializer.data
        for field in ['filename', 'project_id', 'original']:
            self.assertEqual(data[field], self.image_attributes[field])

    def test_image_list_field_content(self):
        data = self.list_serializer.data
        for field in ['filename', 'project_id', 'original', 'thumb', 'big_thumb', 'big_1920', 'd2500', 'state']:
            self.assertEqual(data[field], self.image_attributes[field])

    def test_image_invalid_data(self):
        invalid_data = {
            'filename': '',
            'project_id': 'not-a-number',
            'original': ''
        }
        serializer = ImageSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['filename', 'project_id', 'original']))

    def test_image_list_invalid_data(self):
        invalid_data = {
            'filename': '',
            'project_id': 'not-a-number',
            'original': '',
            'thumb': 'invalid-path',
            'big_thumb': 'invalid-path',
            'big_1920': 'invalid-path',
            'd2500': 'invalid-path',
            'state': ''
        }
        serializer = ImageListSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['filename', 'project_id', 'original', 'thumb', 'big_thumb', 'big_1920', 'd2500', 'state']))
