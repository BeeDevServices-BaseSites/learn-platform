from django.db import models
from django.db.models.deletion import CASCADE
from coreApp.models import *


# Employee Finance information

class PayRates(models.Model):
    pay_tier = models.CharField(max_length=255, blank=True, null=True)
    pay_classification = models.CharField(max_length=255, blank=True, null=True)
    pay_rate = models.IntegerField(blank=True, null=True)

class StaffPay(models.Model):
    employee = models.ForeignKey(Staff, related_name='theEmployee', on_delete=CASCADE)
    pay = models.ForeignKey(PayRates, related_name='thePay', on_delete=CASCADE)
    rate_start = models.DateField(blank=True, null=True)

#Learner Finance Information
    
program_types = [
    ('0', 'Prerequisites'),
    ('0a', 'Tutoring'),
    ('0b', 'Mini Classes'),
    ('1', 'Software Development'),
    ('1a', 'Single Full Stack'),
    ('1b', 'Two Full Stacks'),
    ('2', 'Game Dev'),
    ('2a', '2D Game Dev'),
    ('3', 'Career Services'),
    ('3a', 'Product Management'),
]

class Program(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    program = models.CharField(max_length=255, choices=program_types, default=0)
    cost = models.IntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=1)
    length = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)


class Tuition(models.Model):
    invoice_date = models.DateField(blank=True, null=True)
    finance_date = models.DateField(blank=True, null=True)
    finance_flexxbuy_reported = models.DateField(blank=True, null=True)
    paid_date = models.DateField(blank=True, null=True)
    payer = models.ForeignKey(Learner, related_name='thePayer', on_delete=CASCADE)
    program = models.ForeignKey(Program, related_name='theProgram', on_delete=CASCADE, default=1)

