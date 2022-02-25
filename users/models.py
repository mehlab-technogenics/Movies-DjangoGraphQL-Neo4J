from django.db import models
import uuid
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    email = models.EmailField(max_length=254)
    created= models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.name)