from django.db import models
from django.db.models.deletion import CASCADE
from coreApp.models import *
from financeApp.models import *

class Skill(models.Model):
    skill = models.CharField(max_length=255, blank=True, null=True)

# Level = SR instructor 
class Instructor(models.Model):
    level = models.CharField(max_length=255, blank=True, null=True)
    instructor = models.ForeignKey(Staff, related_name="theInstructor", on_delete=CASCADE)

class TeachersAssistant(models.Model):
    level = models.CharField(max_length=255, blank=True, null=True)
    ta = models.ForeignKey(Staff, related_name="theTa", on_delete=CASCADE)

class InstructorCert(models.Model):
    cert_date = models.DateField(blank=True, null=True)
    instructor_cert = models.ForeignKey(Skill, related_name="theInstructorSkill", on_delete=CASCADE)
    skilled_instructor = models.ForeignKey(Instructor, related_name="theSkilledInstructor", on_delete=CASCADE)

class TACert(models.Model):
    cert_date = models.DateField(blank=True, null=True)
    ta_cert = models.ForeignKey(Skill, related_name="theTASkill", on_delete=CASCADE)
    skilled_ta = models.ForeignKey(Instructor, related_name="theSkilledTA", on_delete=CASCADE)

class BeeType(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)

# Level = Drone Bee
class Bee(models.Model):
    level = models.ForeignKey(BeeType, related_name="theBeeType", on_delete=CASCADE)
    bee = models.ForeignKey(Learner, related_name="theBee", on_delete=CASCADE)

# Tutoring match
class TutorMatch(models.Model):
    tutor = models.ForeignKey(Staff, related_name="theTutor", on_delete=CASCADE)
    tutee = models.ForeignKey(Bee, related_name="theTutee", on_delete=CASCADE)

# Tutoring in general
    # API for stats
class Tutoring(models.Model):
    credits_required = models.IntegerField()
    session_length = models.CharField(max_length=255, blank=True, null=True)
    pair = models.ForeignKey(TutorMatch, related_name='thePair', on_delete=CASCADE)
    session_date = models.DateTimeField()
    is_scheduled = models.BooleanField(default=0)
    is_completed = models.BooleanField(default=0)
    notes = models.TextField(blank=True, null=True)

repo_type = [
    ('0', 'Reading'),
    ('1', 'Assignment')
]

class RepoUrl(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    version = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    repo_purpose = models.CharField(max_length=255, choices=repo_type, default=1)


# Over all course ie Intro to programming
class Course(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    course_length = models.CharField(max_length=255, blank=True, null=True)
    course_info = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=1)
    root_Program = models.CharField(max_length=255, choices=program_types, default=0)


# Course content to include a page with a link to assignment (assignment link must open in new tab)
class Reading(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    course_reading = models.ForeignKey(Course, related_name='theCourseReading', on_delete=CASCADE)
    page_number = models.IntegerField(default=1)
    reading_url = models.ForeignKey(RepoUrl, related_name='theReadingURL', on_delete=CASCADE)
    is_active = models.BooleanField(default=1)

# Assignments level = optional/practice/core
class Assignment(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    course_assignment = models.ForeignKey(Course, related_name='theCourseAssignment', on_delete=CASCADE)
    assignment_url = models.ForeignKey(RepoUrl, related_name='theAssignmentURL', on_delete=CASCADE)
    level = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=1)

# Actual class who is teaching name of class ie june24IntroProgramming active while being taught inactive when done
    # API for stats
class Hive(models.Model):
    hive_name = models.CharField(max_length=255, blank=True, null=True)
    hive_instructor = models.ForeignKey(Instructor, related_name='theHiveInstructor', on_delete=CASCADE)
    hive_ta = models.ForeignKey(TeachersAssistant, related_name='theHiveTA', on_delete=CASCADE, blank=True, null=True)
    course = models.ForeignKey(Course, related_name='theCourse', on_delete=CASCADE)
    is_active = models.BooleanField(default=1)
    hive_start = models.DateField(blank=True, null=True)
    hive_end = models.DateField(blank=True, null=True)

reading_progress = list(Reading.objects.all().values())
assignment_progress = list(Assignment.objects.all().values())

# Assign students to the hive
class Assigned_Hive(models.Model):
    hive = models.ForeignKey(Hive, related_name='theHive', on_delete=CASCADE)
    bee = models.ForeignKey(Bee, related_name='theBee', on_delete=CASCADE)
    last_reading = models.CharField(max_length=255, choices=reading_progress, blank=True, null=True)
    last_assignment = models.CharField(max_length=255, choices=assignment_progress, blank=True, null=True)

status_code = [
    ('0', 'Present'),
    ('1', 'Late'),
    ('2', 'Absent'),
    ('3', 'Dropped'),
    ('4', 'Postponed'),
    ('5', 'Rollback')
]

# current class student and person marking present
# Internal to django pages API
class Attendance(models.Model):
    hive_attendance = models.ForeignKey(Hive, related_name='theHiveAttendance', on_delete=CASCADE)
    bee_attendance = models.ForeignKey(Bee, related_name='theBeeAttendance', on_delete=CASCADE)
    marked_by = models.ForeignKey(Instructor, related_name='theMarkingInstructor', on_delete=CASCADE)
    attendance_status = models.CharField(max_length=255, choices=status_code, null=True, blank=True)
