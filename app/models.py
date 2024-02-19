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
    pass

class Staff(models.Model):
    pass

