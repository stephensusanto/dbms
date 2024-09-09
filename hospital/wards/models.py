from django.db import models
from department.models import Department
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.
class Wards(models.Model):
    WARD_TYPE_CHOICES = (
        ('general', 'General'),
        ('ICU', 'ICU'),
    )
    id_wards = models.AutoField(primary_key=True)
    id_dept = models.ForeignKey(Department, on_delete=models.CASCADE)
    type_ward = models.CharField(max_length=10, choices=WARD_TYPE_CHOICES)

    class Meta:
        db_table = "wards"

    def __str__(self):
        return f"{self.type_ward} Ward - {self.id_dept}"
    
class Bed(models.Model):
    id_bed = models.CharField(max_length=10, primary_key=True)
    id_wards = models.ForeignKey(Wards, db_column='id_wards', on_delete=models.CASCADE)
    comfort_levels = models.CharField(max_length=30)
    bed_length = models.FloatField(validators=[MinValueValidator(0.01), MaxValueValidator(2.13)])
    bed_width = models.FloatField(validators=[MinValueValidator(0.01), MaxValueValidator(1.27)])
    bed_thickness = models.FloatField(validators=[MinValueValidator(15.24), MaxValueValidator(17.78)])
    bed_cost = models.IntegerField(validators=[MinValueValidator(1)])

    class Meta:
        db_table = "bed"

    def __str__(self):
        return f"Bed - {self.id_bed} ({self.comfort_levels})"