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

class Student(models.Model):
    enroll_date = models.DateField(max_length=255, blank=True, null=True)
    graduation_date = models.DateField(blank=True, null=True)
    disenroll_date = models.DateField(blank=True, null=True)
    disenroll_reason = models.CharField(max_length=255, blank=True, null=True)
    student = models.ForeignKey(User, related_name='theStudent', on_delete=CASCADE)

class Staff(models.Model):
    hire_date = models.DateField(blank=True, null=True)
    pay_rate = models.DateField(blank=True, null=True)
    department = models.ForeignKey(Department, related_name='theDepartment', on_delete=CASCADE)
    staff = models.ForeignKey(User, related_name='theStaff', on_delete=CASCADE)

class Department(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    information = models.TextField()
    supervisor = models.ForeignKey(User, related_name='theSuper', on_delete=CASCADE)

class Course(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    course_length = models.CharField(max_length=255, blank=True, null=True)
    course_info = models.CharField(max_length=255, blank=True, null=True)
    active_course = models.BooleanField(default=1)

class Hive(models.Model):
    hive_name = models.CharField(max_length=255, blank=True, null=True)
    hive_instructor = models.ForeignKey(User, related_name='theHiveInstructor', on_delete=CASCADE)
    course = models.ForeignKey(Course, related_name='theCourse', on_delete=CASCADE)
    active_hive = models.BooleanField(default=1)

class Assigned_Hive(models.Model):
    hive = models.ForeignKey(Hive, related_name='theHive', on_delete=CASCADE)
    bee = models.ForeignKey(User, related_name='theBee', on_delete=CASCADE)

class Reading(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    course_reading = models.ForeignKey(Course, related_name='theCourseReading', on_delete=CASCADE)
    active_reading = models.BooleanField(default=1)

class Assignment(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    course_assignment = models.ForeignKey(Course, related_name='theCourseAssignment', on_delete=CASCADE)
    active_assignment = models.BooleanField(default=1)

class Progress(models.Model):
    current_hive = models.ForeignKey(Hive, related_name='theCurrentHive', on_delete=CASCADE)
    hive_bee = models.ForeignKey(User, related_name='theHiveBee', on_delete=CASCADE)
    reading = models.ForeignKey(Reading, related_name='theReading', on_delete=CASCADE)
    assignment = models.ForeignKey(Assignment, related_name='theAssignment', on_delete=CASCADE)
    complete_date = models.DateField()

class History(models.Model):
    hive_taught = models.ForeignKey(Hive, related_name='thePastHives', on_delete=CASCADE)
    instructor = models.ForeignKey(User, related_name='theInstructor', on_delete=CASCADE)
    taught = models.DateField()
    student_count = models.IntegerField()
    pass_rate = models.IntegerField()
    drop_rate = models.IntegerField()

class Attendance(models.Model):
    hive_attendance = models.ForeignKey(Hive, related_name='theHiveAttendance', on_delete=CASCADE)
    bee_attendance = models.ForeignKey(User, related_name='theBeeAttendance', on_delete=CASCADE)
    marked_by = models.ForeignKey(User, related_name='theMarkingInstructor', on_delete=CASCADE)
    attended = models.BooleanField(default=0)