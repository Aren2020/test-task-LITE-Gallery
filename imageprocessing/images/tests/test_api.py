from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch
from django.core.files.uploadedfile import SimpleUploadedFile
from images.models import Image
from images.serializers import ImageListSerializer

class ImageListViewTest(APITestCase):

    def setUp(self):
        self.project_id = 3
        self.image1 = Image.objects.create(
            project_id=self.project_id,
            original=SimpleUploadedFile(name='image1.jpg', content=b'fake image content', content_type='image/jpeg')
        )
        self.image2 = Image.objects.create(
            project_id=self.project_id,
            original=SimpleUploadedFile(name='image2.jpg', content=b'fake image content', content_type='image/jpeg')
        )
        self.other_image = Image.objects.create(
            project_id=2,
            original=SimpleUploadedFile(name='other_image.jpg', content=b'fake image content', content_type='image/jpeg')
        )
        self.url = reverse('images:list', kwargs={'project_id': self.project_id})

    def test_get_images(self):
        response = self.client.get(self.url)
        images = Image.objects.filter(project_id = self.project_id)
        serializer = ImageListSerializer(images, many = True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


# class ImageUploadTest(APITestCase):

#     def setUp(self):
#         self.url = reverse('images:upload')
#         self.valid_payload = {
#             'project_id': 1,
#             'filename': 'filename',
#             'original': SimpleUploadedFile(name='image.jpg', content=b'fake image content', content_type='image/jpeg')
#         }
#         self.invalid_payload = {
#             'project_id': 1,
#             'filename': 'filename',
#             'original': ''
#         }

#     @patch('images.views.add_thumbs.delay')  # Mock the add_thumbs.delay method
#     def test_upload_image_success(self, mock_add_thumbs):
#         response = self.client.post(self.url, data=self.valid_payload)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertTrue('upload_link' in response.data)
#         mock_add_thumbs.assert_called_once()  # Check that the mock method was called once

#     def test_upload_image_failure(self):
#         response = self.client.post(self.url, data=self.invalid_payload)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)