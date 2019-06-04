from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Client(models.Model):
    client_id = models.AutoField(primary_key=True)
    client_company = models.CharField(max_length=70)
    client_email = models.CharField(max_length=70)
    client_phone = models.CharField(max_length=10, null=True)
    #client_name = models.CharField(max_length=70, null=True)

    def __str__(self):
        return "{} | Client ID {:03d}".format(self.client_company, self.client_id)


# add company ID field to the User model to pair with Client table.
class CustomUser(AbstractUser):
    client_id_fk = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.email


class Pipeline(models.Model):
    pipe_id = models.AutoField(primary_key=True)
    client_id_fk = models.ForeignKey(Client, on_delete=models.CASCADE)
    pipe_name = models.CharField(max_length=20)

    def __str__(self):
        return self.pipe_name


class SurveyDate(models.Model):
    client_id_fk = models.ForeignKey(Client, on_delete=models.CASCADE)
    pipe_id_fk = models.ForeignKey(Pipeline, on_delete=models.CASCADE)
    survey_date = models.DateField()

    def __str__(self):
        return str(self.survey_date, self.pipe_id_fk)


class Report(models.Model):
    report_id = models.AutoField(primary_key=True)
    pipe_id_fk = models.ForeignKey(Pipeline, on_delete=models.CASCADE)
    report_object = models.BinaryField(null=True)
    report_date = models.DateField(null=True)

    def __str__(self):
        return self.report_id
