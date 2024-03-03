from django.db import models
from django.db.models.deletion import CASCADE
from coreApp.models import *


# Staff with supervisor coming from user
class Department(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    information = models.TextField()
    supervisor = models.ForeignKey(User, related_name='theSuper', on_delete=CASCADE)

# Staff only
    # Internal to admin django pages API
class Staff(models.Model):
    hire_date = models.DateField(blank=True, null=True)
    pay_rate = models.DateField(blank=True, null=True)
    department = models.ForeignKey(Department, related_name='theDepartment', on_delete=CASCADE)
    staff = models.ForeignKey(User, related_name='theStaff', on_delete=CASCADE)


# Being Tutored only
class Tutee(models.Model):
    tutor_credits_purchased = models.IntegerField()
    tutor_credits_remaining = models.IntegerField()
    purchase_date = models.DateField()
    expire_date = models.DateField()
    tutee = models.ForeignKey(User, related_name='theTutee', on_delete=CASCADE)

# Students only
    # API for stats
class Student(models.Model):
    enroll_date = models.DateField(max_length=255, blank=True, null=True)
    graduation_date = models.DateField(blank=True, null=True)
    disenroll_date = models.DateField(blank=True, null=True)
    disenroll_reason = models.CharField(max_length=255, blank=True, null=True)
    student = models.ForeignKey(User, related_name='theStudent', on_delete=CASCADE)
    github_id = models.CharField(max_length=255, blank=True, null=True)

# For FlexxBuy 
    # Internal to admin django pages API
class Tuition(models.Model):
    invoiced = models.DateField(blank=True, null=True)
    financed = models.DateField(blank=True, null=True)
    finance_reported = models.DateField(blank=True, null=True)
    paid = models.DateField(blank=True, null=True)
    updated_role = models.BooleanField(default=0)
    payer = models.ForeignKey(Student, related_name='thePayer', on_delete=CASCADE)