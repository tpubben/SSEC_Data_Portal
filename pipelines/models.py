from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Client(models.Model):
    client_id = models.AutoField(primary_key=True)
    client_company = models.CharField(max_length=70)
    client_email = models.CharField(max_length=70)
    client_phone = models.IntegerField
    client_name = models.CharField(max_length=70, null=True)


# add company ID field to the User model to pair with Client table.
class CustomUser(AbstractUser):
    client_name = models.CharField(max_length=70, default='NewClient')

    def __str__(self):
        return self.email

class Pipeline(models.Model):
    pipe_id = models.AutoField(primary_key=True)
    client_id_fk = models.ForeignKey(Client, on_delete=models.CASCADE)
    pipe_name = models.CharField(max_length=20)


class Report(models.Model):
    report_id = models.AutoField(primary_key=True)
    pipe_id_fk = models.ForeignKey(Pipeline, on_delete=models.CASCADE)
    report_object = models.BinaryField
    report_date = models.DateField