from django.db import models
from django.contrib.auth.models import User
# from PIL import Image
from Django_practice.yandex_s3_storage import ClientDocsStorage


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics', storage=ClientDocsStorage())

    def __str__(self):
        return f'{self.user.username}'


    # Image resizing is not working now, because of aws s3 bucket storage
    # should be fixed with aws lambda function somehow
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #
    #     img = Image.open(self.image.path)
    #
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)
