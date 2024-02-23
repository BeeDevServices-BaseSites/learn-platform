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
# All users regardless of student or staff
    # API needed for stats to include profile roles

    # Levels = 0 never logged in | 1 = general user | 
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
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
    ('SuperAdmin', '1st User'),
    ('Admissions', 'Admissions Team'),
    ('Admin', 'General Admin'),
    ('Instructor', 'Instructor'),
    ('TA', 'Teachers Assistant'),
    ('Tutee', 'Tutoring Client')
]
# All users regardless of student or staff but distinguished by role
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

# Staff with supervisor coming from user
class Department(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    information = models.TextField()
    supervisor = models.ForeignKey(User, related_name='theSuper', on_delete=CASCADE)

# Students only
    # API for stats
class Student(models.Model):
    enroll_date = models.DateField(max_length=255, blank=True, null=True)
    graduation_date = models.DateField(blank=True, null=True)
    disenroll_date = models.DateField(blank=True, null=True)
    disenroll_reason = models.CharField(max_length=255, blank=True, null=True)
    student = models.ForeignKey(User, related_name='theStudent', on_delete=CASCADE)
    github_id = models.CharField(max_length=255, blank=True, null=True)

# Being Tutored only
class Tutee(models.Model):
    tutor_credits_purchased = models.IntegerField()
    tutor_credits_remaining = models.IntegerField()
    purchase_date = models.DateField()
    expire_date = models.DateField()
    tutee = models.ForeignKey(User, related_name='theTutee', on_delete=CASCADE)

# Staff only
    # Internal to admin django pages API
class Staff(models.Model):
    hire_date = models.DateField(blank=True, null=True)
    pay_rate = models.DateField(blank=True, null=True)
    department = models.ForeignKey(Department, related_name='theDepartment', on_delete=CASCADE)
    staff = models.ForeignKey(User, related_name='theStaff', on_delete=CASCADE)

# For FlexxBuy 
    # Internal to admin django pages API
class Tuition(models.Model):
    invoiced = models.DateField(blank=True, null=True)
    financed = models.DateField(blank=True, null=True)
    finance_reported = models.DateField(blank=True, null=True)
    paid = models.DateField(blank=True, null=True)
    updated_role = models.BooleanField(default=0)
    payer = models.ForeignKey(User, related_name='thePayer', on_delete=CASCADE)
    
# Over all course ie Intro to programming
class Course(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    course_length = models.CharField(max_length=255, blank=True, null=True)
    course_info = models.CharField(max_length=255, blank=True, null=True)
    active_course = models.BooleanField(default=1)

# Tutoring in general
    # API for stats
class Tutoring(models.Model):
    credits_required = models.IntegerField()
    session_length = models.CharField(max_length=255, blank=True, null=True)
    tutoree = models.ForeignKey(User, related_name='theTutoree', on_delete=CASCADE)
    tutor = models.ForeignKey(User, related_name='theTutor', on_delete=CASCADE)
    session_date = models.DateTimeField()
    scheduled_session = models.BooleanField(default=0)
    completed_session = models.BooleanField(default=0)

# Actual class who is teaching name of class ie june24IntroProgramming active while being taught inactive when done
    # API for stats
class Hive(models.Model):
    hive_name = models.CharField(max_length=255, blank=True, null=True)
    hive_instructor = models.ForeignKey(User, related_name='theHiveInstructor', on_delete=CASCADE)
    course = models.ForeignKey(Course, related_name='theCourse', on_delete=CASCADE)
    active_hive = models.BooleanField(default=1)

# Assign students to the hive
class Assigned_Hive(models.Model):
    hive = models.ForeignKey(Hive, related_name='theHive', on_delete=CASCADE)
    bee = models.ForeignKey(User, related_name='theBee', on_delete=CASCADE)

# Course content to include a page with a link to assignment (assignment link must open in new tab)
class Reading(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    course_reading = models.ForeignKey(Course, related_name='theCourseReading', on_delete=CASCADE)
    page_number = models.IntegerField(default=1)
    url = models.CharField(max_length=255, blank=True, null=True)

# Assignments level = optional/practice/core
class Assignment(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    course_assignment = models.ForeignKey(Course, related_name='theCourseAssignment', on_delete=CASCADE)
    level = models.CharField(max_length=255, blank=True, null=True)
    active_assignment = models.BooleanField(default=1)
    url = models.CharField(max_length=255, blank=True, null=True)
    assignment_number = models.IntegerField(default=1)

# Auto generated but clicking next / assignment done checkbox will create a new entry for each page read and assignment done with auto date
    # Internal to django pages API
class Progress(models.Model):
    current_hive = models.ForeignKey(Hive, related_name='theCurrentHive', on_delete=CASCADE)
    hive_bee = models.ForeignKey(User, related_name='theHiveBee', on_delete=CASCADE)
    reading = models.ForeignKey(Reading, related_name='theReading', on_delete=CASCADE)
    assignment = models.ForeignKey(Assignment, related_name='theAssignment', on_delete=CASCADE)
    complete_date = models.DateTimeField(auto_now_add=True)

# History for instructors
    # Internal to django pages API
class History(models.Model):
    hive_taught = models.ForeignKey(Hive, related_name='thePastHives', on_delete=CASCADE)
    instructor = models.ForeignKey(User, related_name='theInstructor', on_delete=CASCADE)
    taught_start = models.DateField()
    taught_end = models.DateField()
    student_count = models.IntegerField()
    pass_rate = models.IntegerField()
    drop_rate = models.IntegerField()

# current class student and person marking present
# Internal to django pages API
class Attendance(models.Model):
    hive_attendance = models.ForeignKey(Hive, related_name='theHiveAttendance', on_delete=CASCADE)
    bee_attendance = models.ForeignKey(User, related_name='theBeeAttendance', on_delete=CASCADE)
    marked_by = models.ForeignKey(User, related_name='theMarkingInstructor', on_delete=CASCADE)
    attended = models.BooleanField(default=0)