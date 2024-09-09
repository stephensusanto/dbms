# Generated by Django 5.1 on 2024-09-09 10:21

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bill", "0005_alter_bill_discharge_date_alter_payment_expired_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bill",
            name="discharge_date",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 9, 9, 10, 21, 51, 705783)
            ),
        ),
        migrations.AlterField(
            model_name="payment",
            name="expired_date",
            field=models.DateField(
                validators=[
                    django.core.validators.MinValueValidator(
                        datetime.datetime(2024, 9, 9, 10, 21, 51, 705882)
                    )
                ]
            ),
        ),
    ]
