from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse

class Course(models.Model):
    sport = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    places = models.IntegerField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE) #if the user is deleted, we also want to delete course... ManyToOne
    bookings = models.ManyToManyField(User, related_name="courseBookings")

    def total_bookings(self):
        return -self.bookings.count()

    def __str__(self):
        return self.sport

    def get_absolute_url(self):
        return reverse('sportifyCourses')

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)