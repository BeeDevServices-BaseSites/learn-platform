from django.db import models
from django.db.models.signals import post_save
import datetime
from django.db.models.deletion import CASCADE
from django.core.validators import RegexValidator
import re

class UserManager(models.Manager):
    def validate(self, form):
        errors = {}
        emailCheck = self.filter(email=form['email'])
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(form['email']):
            errors['email'] = 'Invalid Email Address'
        if emailCheck:
            print('found email error')
            errors['email'] = 'Email already in use'
        if form['password'] != form['confirm']:
            print('mis matched password error')
            errors['password'] = 'Passwords do not match'
        return errors
    
    def updatePassword(self, form):
        errors = {}
        if form['password'] != form['confirm']:
            errors['password'] = "Passwords do not match"
        return errors
    
    def updateEmail(self, form):
        errors = {}
        emailCheck = self.filter(email=form['email'])
        if emailCheck:
            errors['email'] = 'Email is already registered'
        return errors
# All users regardless of student or staff
    # API needed for stats to include profile roles

    # Levels = 0 never logged in | 1 = logged in | 24 = superadmin
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=1)
    is_default_pass =  models.BooleanField(default=0)

    objects = UserManager()

    logged_on = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.firstName} {self.lastName}'

    def fullName(self):
        return f'{self.firstName} {self.lastName}'

# All users regardless of learner or staff
class Profile(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    # 0 = not staff | 1 = staff
    is_staff = models.BooleanField(default=0)
    image = models.ImageField(upload_to='profileImgs', default='bee.jpg')
    address01 = models.CharField(max_length=255, blank=True, null=True)
    address02 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self):
        return f'{self.user.username} Profile'
    
def create_user_profile(sender, instance, created, **kwargs):
    
    if created:
        User.objects.create(user=instance)
        post_save.connect(create_user_profile, sender=User)

# if is_staff == 1 
        
staff_roles = [
    ('0', 'Developer'),
    ('1', 'Instructor'),
    ('2', 'TA'),
    ('3', 'Tutor'),
    ('4', 'Supervisor'),
    ('5', 'Management'),
    ('6', 'Team Lead'),
]

class Staff(models.Model):
    hire_date = models.DateField(blank=True, null=True)
    inactive_date = models.DateField(blank=True, null=True)
    staff = models.ForeignKey(User, related_name='theStaff', on_delete=CASCADE)

class StaffRole(models.Model):
    role = models.CharField(max_length=255, choices=staff_roles, default=0)
    job = models.ForeignKey(Staff, related_name='theStaffJob', on_delete=CASCADE)

class Department(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    supervisor = models.ForeignKey(Staff, related_name='theSuper', on_delete=CASCADE)

class DepartmentStaff(models.Model):
    worker = models.ForeignKey(Staff, related_name='theWorker', on_delete=CASCADE)
    workstation = models.ForeignKey(Department, related_name='theWorkStation', on_delete=CASCADE)

# if is_staff == 0
    
learner_roles = [
    ('0', 'Current Student'),
    ('1', 'Current Tutee'),
    ('2', 'Alumni'),
    ('3', 'Intern'),
    ('4', 'Prospective Learner')
]
    
class Learner(models.Model):
    contact_date = models.DateField(blank=True, null=True)
    intake_staff = models.ForeignKey(Staff, related_name='theIntakeStaff', on_delete=CASCADE)
    learner = models.ForeignKey(User, related_name='theLearner', on_delete=CASCADE)

class LearnerRoles(models.Model):
    role = models.CharField(max_length=255, choices=learner_roles, default=0)
    learner_type = models.ForeignKey(Learner, related_name='theLearnerType', on_delete=CASCADE)