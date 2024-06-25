from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from botocore.exceptions import ClientError
from .models import Image
from .serializers import ImageSerializer, ImageListSerializer
from .tasks import add_thumbs
import logging

class ImageListView(generics.ListAPIView):
    serializer_class = ImageListSerializer

    def get_queryset(self):
        project_id = self.kwargs.get('project_id')
        return Image.objects.filter(project_id = project_id)

class ImageUpload(APIView):
    def post(self, request):
        serializer = ImageSerializer(data = request.data)  
        if serializer.is_valid():
            data = serializer.validated_data
            try:
                image = serializer.save()
                add_thumbs.delay(image.id)
                return Response({'upload_link': image.original.url}, status = status.HTTP_201_CREATED)
            except ClientError as e:
                logging.error(e)
        return Response(status = status.HTTP_400_BAD_REQUEST)


###################################
# from django.shortcuts import render
# def test(request):
#     return render(request, 'test.html')