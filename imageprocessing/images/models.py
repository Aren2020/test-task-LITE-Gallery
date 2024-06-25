from django.db import models

class Image(models.Model):
    filename = models.CharField(max_length = 255)
    project_id = models.IntegerField()
    original = models.ImageField(upload_to = 'originals/')
    thumb = models.ImageField(upload_to = 'thumbs/', null = True, blank = True)
    big_thumb = models.ImageField(upload_to = 'big_thumbs/', null=True, blank = True)
    big_1920 = models.ImageField(upload_to = 'big_1920/', null = True, blank = True)
    d2500 = models.ImageField(upload_to = 'd2500/', null = True, blank = True)
    state = models.CharField(max_length = 20, default = 'init')

    def __str__(self):
        return f'{self.filename} {self.project_id}'