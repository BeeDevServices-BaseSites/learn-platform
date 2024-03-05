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
role (list of choices)
FK-staff

#### Departments
department
FK-Staff - supervisor

##### Add department staff
FK-department
FK-staff

### Users where is_staff == 0
contact date
staff contact
FK-user

#### Add Learner Roles
role (list of roles)
FK-learner

# Finance App

## Pay Rates
level
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