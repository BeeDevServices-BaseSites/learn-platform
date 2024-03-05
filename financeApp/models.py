from django.db import models
from django.db.models.deletion import CASCADE
from coreApp.models import *

learnerRoleTypes = [
    ('Student', 'Current Student account'),
    ('Upcoming-Student', 'Enrolled but waiting for class start'),
    ('Alumni', 'Graduated Student'),
    ('Intern', 'Internship'),
    ('SuperAdmin', '1st User'),
    ('Admissions', 'Admissions Team'),
    ('Admin', 'General Admin'),
    ('Instructor', 'Instructor'),
    ('TA', 'Teachers Assistant'),
    ('Tutee', 'Tutoring Client')
]
class Learner(models.Model):
    contact_date = models.DateField(blank=True, null=True)
    staff_contact = models.ForeignKey(User, related_name='theStaffContact', on_delete=CASCADE)
    learner = models.ForeignKey(User, related_name='theLearner', on_delete=CASCADE)



# Being Tutored only
class Tutee(models.Model):
    tutor_credits_purchased = models.IntegerField()
    tutor_credits_remaining = models.IntegerField()
    purchase_date = models.DateField()
    expire_date = models.DateField()
    tutee = models.ForeignKey(User, related_name='theTutee', on_delete=CASCADE)

# Mini class learner only
class MiniStudent(models.Model):
    enroll_date = models.DateField(max_length=255, blank=True, null=True)
    micro_student = models.ForeignKey(User, related_name='theMicroStudent', on_delete=CASCADE)

# Students only
    # API for stats
class Student(models.Model):
    enroll_date = models.DateField(max_length=255, blank=True, null=True)
    graduation_date = models.DateField(blank=True, null=True)
    disenroll_date = models.DateField(blank=True, null=True)
    disenroll_reason = models.CharField(max_length=255, blank=True, null=True)
    student = models.ForeignKey(User, related_name='theStudent', on_delete=CASCADE)
    github_id = models.CharField(max_length=255, blank=True, null=True)

programTypes = [
    ('0a', 'Tutoring'),
    ('0b', 'Mini Classes'),
    ('1a', 'Single Full Stack'),
    ('1b', 'Two Full Stacks'),
    ('2a', '2D Game Dev'),
    ('3a', 'Product Management'),
]

class Program(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    program_type = models.CharField(max_length=255, choices=programTypes, default='1b')

# For FlexxBuy 
    # Internal to admin django pages API
class Tuition(models.Model):
    invoiced = models.DateField(blank=True, null=True)
    financed = models.DateField(blank=True, null=True)
    finance_reported = models.DateField(blank=True, null=True)
    paid = models.DateField(blank=True, null=True)
    updated_role = models.BooleanField(default=0)
    payer = models.ForeignKey(Student, related_name='thePayer', on_delete=CASCADE)
    program = models.ForeignKey(Program, related_name='theProgram', on_delete=CASCADE, default=1)

