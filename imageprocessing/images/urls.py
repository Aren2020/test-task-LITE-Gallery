from django.urls import path, include
from . import views

app_name = 'images'

urlpatterns = [
    # path('', views.test),
    path('images/', views.ImageUpload.as_view(), name = 'upload'),
    path('projects/<int:project_id>/images/', views.ImageListView.as_view(), name = 'list'),
]