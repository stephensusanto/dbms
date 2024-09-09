from django.db import models
from base.models import BaseModel
from django.utils.text import slugify
from department.models import Department
from django.utils.translation import gettext_lazy as _
from datetime import datetime  
from django.core.validators import MinValueValidator, MaxValueValidator

class Roles(models.Model):
    id_roles = models.AutoField(primary_key=True)
    name_role = models.CharField(max_length=30, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "roles"

    def __str__(self):
        return self.name_role


class Staff(models.Model):
    id_staff = models.CharField(max_length=30, primary_key=True)
    id_roles = models.ForeignKey(Roles,  db_column='id_roles', on_delete=models.CASCADE)
    id_dept = models.ForeignKey(Department,  db_column='id_dept', on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    address = models.TextField()
    mobile = models.CharField(max_length=13)
    salary = models.IntegerField(validators=[MinValueValidator(1)])

    class Meta:
        db_table = "staff"

    def __str__(self):
        return self.full_name

    
class MedicalSpeciality(models.Model):
    id_medical_speciality = models.AutoField(primary_key=True)
    name_medical_speciality = models.CharField(max_length=50)

    class Meta:
        db_table = "medical_speciality"

    def __str__(self):
        return self.name_medical_speciality


class OwnershipSpeciality(models.Model):
    id_ownership = models.AutoField(primary_key=True)
    id_staff = models.ForeignKey(Staff, db_column='id_staff', on_delete=models.CASCADE)
    id_medical_speciality = models.ForeignKey(MedicalSpeciality, db_column='id_medical_speciality', on_delete=models.CASCADE)
    level_of_profiency = models.CharField(max_length=30)
    training_date = models.DateField()

    class Meta:
        db_table = "ownership_speciality"

    def __str__(self):
        return f"{self.id_staff} - {self.id_medical_speciality}"

class WWCC(models.Model):
    wwcc_id = models.AutoField(primary_key=True)
    wwcc_number = models.CharField(max_length=30, unique=True)
    expired_date = models.DateField(validators=[MinValueValidator(datetime.now())])
    id_staff = models.ForeignKey(Staff, db_column='id_staff', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "wwcc"

    def __str__(self):
        return f"WWCC ID: {self.wwcc_id} - {self.id_staff.full_name}"