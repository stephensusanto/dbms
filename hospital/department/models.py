from django.db import models
from base.models import BaseModel
from django.utils.text import slugify
# Create your models here.

class Department(BaseModel):
    name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Generate slug from the name field
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)