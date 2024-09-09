from django.db import models
from staff.models import Staff
from patient.models import Patient
from department.models import Department
from datetime import datetime  
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Admission(models.Model):
    id_admission = models.AutoField(primary_key=True)
    doctor = models.ForeignKey(Staff, db_column='doctor', related_name='staff_roles_doctor', on_delete=models.CASCADE)
    nurse = models.ForeignKey(Staff, db_column='nurse', related_name='staff_roles_nurse', on_delete=models.CASCADE)
    id_patient = models.ForeignKey(Patient, db_column='id_patient', on_delete=models.CASCADE)
    id_dept = models.ForeignKey(Department,db_column='id_dept', on_delete=models.CASCADE)
    type_admission = models.CharField(max_length=20, choices=[('planned', 'Planned'), ('emergency', 'Emergency')])
    date_time_admission = models.DateTimeField(default=datetime.now())

    class Meta:
        db_table = "admission"

    def __str__(self):
        return f"Admission ID: {self.id_admission} - {self.id_patient.full_name} - {self.type_admission}"

class EmergencyAdmission(models.Model):
    id_emergency_admission = models.AutoField(primary_key=True)
    id_admission = models.OneToOneField(Admission, db_column='id_admission', on_delete=models.CASCADE, related_name='emergency_admission')
    triage_nurse = models.ForeignKey(Staff, related_name='triage_nurse_admissions', on_delete=models.CASCADE)
    patient_condition = models.TextField()

    class Meta:
        db_table = "emergency_admission"

    def __str__(self):
        return f"Emergency Admission ID: {self.id_emergency_admission}"

class PlannedAdmission(models.Model):
    id_planned_admission = models.AutoField(primary_key=True)
    id_admission = models.OneToOneField(Admission, db_column='id_admission', on_delete=models.CASCADE, related_name='planned_admission')
    reference_number = models.CharField(max_length=20, unique=True)
    referring_health_practitioner = models.CharField(max_length=50)

    class Meta:
        db_table = "planned_admission"
    
    def __str__(self):
        return f"Planned Admission ID: {self.id_planned_admission}"
    
class Services(models.Model):
    id_services = models.AutoField(primary_key=True)
    id_admission = models.ForeignKey(Admission, db_column='id_admission', on_delete=models.CASCADE)  # Assuming Admission is another model
    name_of_services = models.CharField(max_length=20)
    services_cost = models.IntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return f"Service ID: {self.id_services} - {self.name_of_services}"
