from django.db import models
from django.db.models.deletion import CASCADE
from coreApp.models import *
from financeApp.models import *


# Level = SR instructor 
class Instructor(models.Model):
    level = models.CharField(max_length=255, blank=True, null=True)
    instructor = models.ForeignKey(Staff, related_name="theInstructor", on_delete=CASCADE)

# Level = Drone Bee
class Bee(models.Model):
    level = models.CharField(max_length=255, blank=True, null=True)
    bee = models.ForeignKey(Student, related_name="theBee", on_delete=CASCADE)

# Tutoring match
class TutorMatch(models.Model):
    tutor = models.ForeignKey(Instructor, related_name="theTutor", on_delete=CASCADE)
    tutoree = models.ForeignKey(Tutee, related_name="theTutoree", on_delete=CASCADE)

# Tutoring in general
    # API for stats
class Tutoring(models.Model):
    credits_required = models.IntegerField()
    session_length = models.CharField(max_length=255, blank=True, null=True)
    pair = models.ForeignKey(TutorMatch, related_name='thePair', on_delete=CASCADE)
    session_date = models.DateTimeField()
    scheduled_session = models.BooleanField(default=0)
    completed_session = models.BooleanField(default=0)


# Over all course ie Intro to programming
class Course(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    course_length = models.CharField(max_length=255, blank=True, null=True)
    course_info = models.CharField(max_length=255, blank=True, null=True)
    active_course = models.BooleanField(default=1)

class CourseRepo(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    url = models.TextField()
    version = models.CharField(max_length=255, blank=True, null=True)
    subject = models.ForeignKey(Course, related_name='theSubject', on_delete=CASCADE)

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

class AssignmentRepo(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    url = models.TextField()
    version = models.CharField(max_length=255, blank=True, null=True)
    homework = models.ForeignKey(Assignment, related_name='theHomework', on_delete=CASCADE)


# Actual class who is teaching name of class ie june24IntroProgramming active while being taught inactive when done
    # API for stats
class Hive(models.Model):
    hive_name = models.CharField(max_length=255, blank=True, null=True)
    hive_instructor = models.ForeignKey(Instructor, related_name='theHiveInstructor', on_delete=CASCADE)
    course = models.ForeignKey(Course, related_name='theCourse', on_delete=CASCADE)
    active_hive = models.BooleanField(default=1)



# Assign students to the hive
class Assigned_Hive(models.Model):
    hive = models.ForeignKey(Hive, related_name='theHive', on_delete=CASCADE)
    bee = models.ForeignKey(Bee, related_name='theBee', on_delete=CASCADE)



# Auto generated but clicking next / assignment done checkbox will create a new entry for each page read and assignment done with auto date
    # Internal to django pages API
class Progress(models.Model):
    current_hive = models.ForeignKey(Hive, related_name='theCurrentHive', on_delete=CASCADE)
    hive_bee = models.ForeignKey(Bee, related_name='theHiveBee', on_delete=CASCADE)
    reading = models.ForeignKey(Reading, related_name='theReading', on_delete=CASCADE)
    assignment = models.ForeignKey(Assignment, related_name='theAssignment', on_delete=CASCADE)
    complete_date = models.DateTimeField(auto_now_add=True)

# History for instructors
    # Internal to django pages API
class History(models.Model):
    hive_taught = models.ForeignKey(Hive, related_name='thePastHives', on_delete=CASCADE)
    instructor = models.ForeignKey(Instructor, related_name='theInstructor', on_delete=CASCADE)
    taught_start = models.DateField()
    taught_end = models.DateField()
    student_count = models.IntegerField()
    pass_rate = models.IntegerField()
    drop_rate = models.IntegerField()

# current class student and person marking present
# Internal to django pages API
class Attendance(models.Model):
    hive_attendance = models.ForeignKey(Hive, related_name='theHiveAttendance', on_delete=CASCADE)
    bee_attendance = models.ForeignKey(Bee, related_name='theBeeAttendance', on_delete=CASCADE)
    marked_by = models.ForeignKey(Instructor, related_name='theMarkingInstructor', on_delete=CASCADE)
    attended = models.BooleanField(default=0)