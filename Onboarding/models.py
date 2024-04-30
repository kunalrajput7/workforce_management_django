from django.db import models

# Create your models here.
class Resource(models.Model):
    EmpCode = models.CharField(max_length=20)
    EmpName = models.CharField(max_length=100)
    Grade = models.CharField(max_length=50)
    Role = models.CharField(max_length=100)
    Location = models.CharField(max_length=100)
    Billed = models.CharField(max_length=100)
    Status = models.CharField(max_length=100)

    def __str__(self):
        return self.EmpName