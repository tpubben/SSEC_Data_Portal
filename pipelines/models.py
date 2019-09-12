from django.contrib.gis.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Client(models.Model):
    client_id = models.AutoField(primary_key=True)
    client_company = models.CharField(max_length=70)
    client_email = models.CharField(max_length=70)
    client_phone = models.CharField(max_length=10, null=True)

    def __str__(self):
        return "{} | Client ID {:03d}".format(self.client_company, self.client_id)


# add company ID field to the User model to pair with Client table.
class CustomUser(AbstractUser):
    client_id_fk = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.email


class Pipeline(models.Model):
    # pipe_id = models.AutoField(primary_key=True)
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
    client_id_fk = models.ForeignKey(Client, on_delete=models.CASCADE)
    pipe_id_fk = models.ForeignKey(Pipeline, on_delete=models.CASCADE)
    survey_date = models.DateField()

    def __str__(self):

        # create a slug based off the returned foreign key from the client model
        if str(self.client_id_fk).split()[1] != '|':
            client_slug = str(self.client_id_fk).split()[0]+str(self.client_id_fk).split()[1]
        else:
            client_slug = str(self.client_id_fk).split()[0]

        # return that slug along with the pipeline ID and date of survey for display and parsing into JS script
        return "{}_{}_{}".format(client_slug, self.pipe_id_fk, self.survey_date)

class SurveyPoint(models.Model):
    surveydate_id_fk = models.ForeignKey(SurveyDate, on_delete=models.CASCADE, related_name="surveypoint")
    gas_value = models.FloatField()
    gas_geom = models.PointField()

    def __str__(self):
        return self.gas_value
