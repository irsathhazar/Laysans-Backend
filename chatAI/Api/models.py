from django.db import models

# Create your models here.

# Create your models here.
class Client(models.Model):
    Productname=models.CharField(max_length=1000,null=True,blank=True)
    Link=models.CharField(max_length=2000,null=True,blank=True)
    dateandtime=models.DateTimeField(auto_now=True)
   
    def __str__(self):
        return self.Productname
    

class Careers(models.Model):
    JobName=models.CharField(max_length=1000,null=True,blank=True)
    RoleName=models.CharField(max_length=100,blank=True,null=True)
    Aboutjob=models.TextField(max_length=400,blank=True,null=True)
    exp=models.CharField(max_length=100,blank=True,null=True)
    Iconclassname=models.CharField(max_length=1000,null=True,blank=True)
    dateandtime=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.JobName