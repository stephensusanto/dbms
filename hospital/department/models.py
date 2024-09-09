from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Department(models.Model):
    class DeptTypeChoice(models.TextChoices):
        GENERAL = "General", _("General"),
        EMERGENCY = "Emergency", _("Emergency"),
        PEDIATRICS = "Pediatrics", _("Pediatrics"),
        SURGERY = "Surgery", _("Surgery"),
    
    id_dept = models.CharField(max_length=20, primary_key=True, )
    dept_type = models.CharField(max_length=20, choices=DeptTypeChoice, default=DeptTypeChoice.GENERAL)
    dept_name = models.CharField(max_length=30, unique=True, default='')
    start_time = models.TimeField(default='10:00:00')
    end_time = models.TimeField(default='20:00:00')
    operating_theatre = models.IntegerField(validators=[MinValueValidator(1)])

    class Meta:
        db_table = "department"

    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError('End time must be after start time.')
        return super().clean()

    def __str__(self):
        return self.dept_name