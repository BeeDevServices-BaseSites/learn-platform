from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Staff)
admin.site.register(StaffRole)
admin.site.register(Department)
admin.site.register(DepartmentStaff)
admin.site.register(Learner)
admin.site.register(LearnerRoles)
