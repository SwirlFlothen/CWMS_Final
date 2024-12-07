from django.db import models
from django.db import models
from django.contrib.auth.models import User



# Create your models here.
# User Profile for additional data
class UserProfile(models.Model):
    USER_TYPE_CHOICES = [
        ('Constructor', 'Constructor'),
        ('Customer', 'Customer'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

# Service Cards
class Service(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='service_images/')

# Projects
class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=50, choices=[('Running', 'Running'), ('Completed', 'Completed')])
    image = models.ImageField(upload_to='project_images/', blank=True, null=True)

# Waste Material
class WasteMaterial(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='waste_materials')
    name = models.CharField(max_length=100)
    quantity = models.FloatField()
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='waste_images/', blank=True, null=True)
