# General outline overivew of database

## Inside the CoreApp
- On apps 1st launch it will land on the registration page where a code is required.  This will set the user as admin and direct them to the dashboard.

- After this user is created on app load it will go to the log in page.  Registration page is only seen on app initial launch or by manually typing in the link. All users after the 1st one will need to be added by an admin user and when that user logs in for the 1st time they will be logged in and sent to a password reset page.  This will change the is_default_pass boolean from 0 to 1 allowing them to just log in (this can be changed for password resets at any time)

- Staff users will have a department, role and supervisor pre-done when their user is added to the system

- Learner users will also have some presets when added to the system to include who they spoke too (ie who is adding them)

## Inside the FinanceApp
- From there it goes to the finance app where the staff has a pay rate and other information regarding their pay

- Learners have a program they are part of that will tie into what they are paying for.

## Inside CourseApp
- From there it's over to the course app. Where staff becomes TA or Instructor or potentially just staff but skills are added via certificates earned...(show skills in html get certificate)

- Learners become bee's regardless of reason for being part of the platform.  

- Tutor matching simply matches up who is tutoring who as pairs then moves into the tutoring table where # of credits required, session length as well as when it is scheduled and complete are.

- Next up is where we start the course content.  A table for the repo links, table for the program  then on to the individual courses by name

- after that we link the readings and assignments or essentially the repos to the course name

- Then we create the hive or classroom, who is teaching it when does it start and end, what are they teaching, a boolean to hide when inactive....


# Core App

## All Users
first_name
last_name
email
password
is_active (1 == active user | 0 == inactive user -> account locked)
is_new (1 == new user  / must change password | 0 == not new / password change not needed)
last_logged_on_date
is_staff (1 == staff | 0 == learner)
image
address01
address02
city
state
zip
phone

### Users where is_staff == 1
hire date
fire date
FK-user

#### Add Staff Roles
(This will be like a many to many table as staff might have more than 1 role)
role (list of choices)
FK-staff

#### Departments
department
FK-Staff - supervisor

##### Add department staff
(This is also like a many to many as staff may be apart of more than 1 department)
FK-department
FK-staff

### Users where is_staff == 0
contact date
staff contact
FK-user

#### Add Learner Roles
(many to many table as learners might have more than one role)
role (list of roles)
FK-learner

# Finance App

## Pay Rates
level - M1 (management level 1)
pay type - hourly vs salary
payrate

### Add Staff Pay
FK-Staff
FK-pay
rate date start

## program offerings
program name (choice list)
tuition

### tuition
FK-program
FK-learner
invoice date
financed date
paid date
reported date

# Course app

## Skills
skill name

## Instructor
FK-Staff
rank (jr sr instructor)

### instructor-certificatioins
FK-skills
FK-instructor
cert date

## TA
FK-Staff
rank (jr sr ta)

### TA - certifications
FK-skill
FK-TA
cert date

## Bee levels
title
(drone = new to programming | worker = in programming (tutees, mini classes, reached full stack in program) | royal = post grad (interns, alumni))

## Bee
level (drone, worker)
FK-learner

## tutor matching
FK-staff
FK-bee

### tutoring
session credits
session length
FK-tutormatching
session date
is_scheduled
is_completed
notes

## repo urls
repo type (assignment course)
url
version
title

## programs
title
description
program id (0 for pre requisist courses 1 software dev)
is_active
length

### course
title
FK-program

#### readings
FK-course
FK-repo
is_active

#### assignments
FK-course
FK-repo
level
is_active

### hive
name
FK-instructor
FK-ta
FK-course
start date
end date
is_active

#### assignedhive
FK-hive
FK-bee
last reading (list of FK-readings)
last assignment (list of FK-assignments)

#### attendance
FK-bee
currenthive (list of FK-hives)
FK-marked by (list of FK-instructors)
date


## metrics
FK-hive
bee-count-start
bee-count-end
bee-count-dismissed
bee-count-rollback
bee-count-postponed