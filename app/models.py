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
        if form['password'] != form['confirmPassword']:
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
    
class User(models.Model):
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    level = models.IntegerField(default=0)
    active_account = models.BooleanField(default=1)

    objects = UserManager()

    loggedOn = models.DateTimeField(auto_now=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.firstName} {self.lastName}'

    def fullName(self):
        return f'{self.firstName} {self.lastName}'

roleTypes = [
    ('Student', 'Current Student account'),
    ('Upcoming-Student', 'Enrolled but waiting for class start'),
    ('Alumni', 'Graduated Student'),
    ('Intern', 'Internship'),
    ('Instructor', 'Instructor'),
    ('TA', 'Teachers Assistant')
]

class Profile(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    role = models.BooleanField(default='Student')
    image = models.ImageField(upload_to='profileImgs', default='bee.jpg')
    def __str__(self):
        return f'{self.user.username} Profile'
    
def create_user_profile(sender, instance, created, **kwargs):
    
    if created:
        User.objects.create(user=instance)
        post_save.connect(create_user_profile, sender=User)

class Student(models.Model):
    address01 = models.CharField(max_length=255, blank=True, null=True)
    address02 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    enroll_date = models.DateField(max_length=255, blank=True, null=True)
    graduation_date = models.DateField(blank=True, null=True)
    disenroll_date = models.DateField(blank=True, null=True)
    disenroll_reason = models.CharField(max_length=255, blank=True, null=True)
    student = models.ForeignKey(User, related_name='theStudent', on_delete=CASCADE)

class Staff(models.Model):
    address01 = models.CharField(max_length=255, blank=True, null=True)
    address02 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    hire_date = models.DateField(blank=True, null=True)
    pay_rate = models.DateField(blank=True, null=True)
    supervisor = models.ForeignKey(User, related_name='theSupervisor', on_delete=CASCADE)
    staff = models.ForeignKey(User, related_name='theStaff', on_delete=CASCADE)

class Course(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    course_length = models.CharField(max_length=255, blank=True, null=True)
    course_info = models.CharField(max_length=255, blank=True, null=True)

class Hive(models.Model):
    hive_name = models.CharField(max_length=255, blank=True, null=True)
    instructor = models.ForeignKey(User, related_name='theInstructor', on_delete=CASCADE)
    pass

class Assigned_Hive(models.Model):
    hive = models.ForeignKey()
    student = models.ForeignKey()

class Progress(models.Model):
    hive = models.ForeignKey()
    student = models.ForeignKey()
    reading = models.ForeignKey()
    assignment = models.ForeignKey()
    complete_date = models.DateField()
    pass

class History(models.Model):
    hive = models.ForeignKey()
    instructor = models.ForeignKey()
    taught = models.DateField()
    student_count = models.IntegerField()
    pass_rate = models.IntegerField()
    drop_rate = models.IntegerField()
    pass

class Reading(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    course = models.ForeignKey()
    pass

class Assignment(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    course = models.ForeignKey()
    pass

class Attendance(models.Model):
    hive = models.ForeignKey()
    student = models.ForeignKey()
    marked_by = models.ForeignKey()
    attended = models.BooleanField()
    pass