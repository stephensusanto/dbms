from django.db import models

# Create your models here.
class Patient(models.Model):
    id_patient = models.CharField(max_length=20, primary_key=True)
    full_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=13)  
    emergency_contact_number = models.CharField(max_length=13)
    emergency_contact_name = models.CharField(max_length=50)
    dob = models.DateField()
    insu_number = models.CharField(max_length=20, blank=True)

    class Meta:
        db_table = "patient"

    def __str__(self):
        return self.full_name
