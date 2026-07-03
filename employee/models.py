
from django.db import models

class Employee(models.Model):
    emp_id = models.CharField(max_length=10, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=50)
    designation = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"