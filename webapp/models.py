from django.db import models

class Employees(models.Model):
    firstname = models.CharField(max_length=25)
    lastname = models.CharField(max_length=25)
    phone_no = models.CharField(max_length=30, null=True)
    emp_id = models.IntegerField()
    
    def __str__(self):
        return str(self.emp_id)
    
    def get_fieldnames():
        print("hy")
        return ["firstname", "lastname", "emp_id", "phone_no"]
    