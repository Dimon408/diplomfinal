from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Client_Time, Worker, Error, Prohod_place, Protect_points, Dostups


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class WorkerInline(admin.StackedInline):
    model = Worker
    can_delete = False
    verbose_name_plural = 'Worker'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    BaseUserAdmin.fields
    inlines = (WorkerInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)



admin.site.register(Client_Time)
admin.site.register(Worker)
admin.site.register(Error)
admin.site.register(Prohod_place)
admin.site.register(Protect_points)
admin.site.register(Dostups)
# Register your models here.
