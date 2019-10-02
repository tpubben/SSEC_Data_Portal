from django.contrib.gis.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Client(models.Model):
    client_id = models.AutoField(primary_key=True)
    client_company = models.CharField(max_length=70)
    client_email = models.CharField(max_length=70)
    client_phone = models.CharField(max_length=10, null=True)

    def __str__(self):
        return "{}".format(self.client_company)


# add company ID field to the User model to pair with Client table.
class CustomUser(AbstractUser):
    client_id_fk = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.email


class Pipeline(models.Model):
    client_id_fk = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    pipe_name = models.CharField(max_length=20)
    pipe_geom = models.LineStringField(null=True)

    def __str__(self):
        return self.pipe_name


class Infrastructure(models.Model):
    inf_id = models.AutoField(primary_key=True)
    client_id_fk = models.ForeignKey(Client, on_delete=models.CASCADE)
    inf_name = models.CharField(max_length=20)
    inf_geom = models.PointField(null=True)

    def __str__(self):
        return self.inf_name

class SurveyDate(models.Model):
    GEOMETRY_CHOICES = (
        ("PIPELINE", "Pipeline"),
        ("SITE", "Site"),
    )
    client_id_fk = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='surveys')
    pipe_id_fk = models.ForeignKey(Pipeline, null=True, on_delete=models.CASCADE, blank=True)
    survey_date = models.DateField()
    inf_id_fk = models.ForeignKey(Infrastructure, null=True, on_delete=models.CASCADE, blank=True)
    geometry_type = models.CharField(max_length=8, choices=GEOMETRY_CHOICES)
    wind_direction = models.CharField(max_length=3, null=True, blank=True)
    temperature = models.PositiveSmallIntegerField(null=True, blank=True)
    flight_duration = models.CharField(max_length=10, null=True, blank=True)
    survey_comments = models.TextField(null=True, blank=True)


    def __str__(self):
        return str(self.survey_date)

class SurveyPoint(models.Model):
    surveydate_id_fk = models.ForeignKey(SurveyDate, on_delete=models.CASCADE, related_name="surveypoint", null=True)
    gas_value = models.FloatField()
    gas_geom = models.PointField(null=True)
    gas_lat = models.CharField(max_length=50, null=True)
    gas_long = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.gas_value


class Deficiency(models.Model):
    surveydate_id_fk = models.ForeignKey(SurveyDate, on_delete=models.CASCADE, related_name="surveydef")
    deficiency_number = models.IntegerField()
    deficiency_gas = models.FloatField()
    deficiency_desc = models.TextField(null=True, blank=True)
    deficiency_photo = models.ImageField(upload_to='images') # link to image uploaded to photos folder

    def __str__(self):
        return str(self.deficiency_number)