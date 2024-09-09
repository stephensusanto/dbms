from django.db import models
from admission.models import Admission
from patient.models import Patient
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime  
# Create your models here.
class Bill(models.Model):
    id_bill = models.AutoField(primary_key=True)
    id_admission = models.ForeignKey(Admission, db_column='id_admission', on_delete=models.CASCADE)
    id_patient = models.ForeignKey(Patient, db_column='id_patient', on_delete=models.CASCADE)
    total_cost = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(50000)])
    cost_covered_insu = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    balanced_owed = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    discharge_date = models.DateTimeField(default=datetime.now())
    is_paid = models.BooleanField(default=False)

    class Meta:
        db_table = "bill"

    def __str__(self):
        return f"Bill ID: {self.id_bill}"


class Payment(models.Model):
    id_payment = models.AutoField(primary_key=True)
    id_bill = models.ForeignKey(Bill, db_column='id_bill', on_delete=models.CASCADE)
    cc_number = models.CharField(max_length=20)
    expired_date = models.DateField(validators=[MinValueValidator(datetime.now())])
    card_holder_name = models.CharField(max_length=30)
    
    class Meta:
        db_table = "payment"
        
    def __str__(self):
        return f"Payment: {self.id_payment} - {self.id_bill.id_patient.full_name}"