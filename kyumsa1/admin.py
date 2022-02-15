from django.contrib import admin
from django.contrib.auth.models import Group

from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from kyumsa1.models import Student, Alumin 
from .forms  import UserAdminCreationForm, UserAdminChangeForm

# removegroup model from admin
#admin.site.unregister(Group)




User = get_user_model()
class UserAdmin(admin.ModelAdmin):
    search_fields=['email']
    list_display =['first_Name', 'last_Name', 'email','status', 'admin']

    class Meta:
        model=User



class StudentAdmin(admin.ModelAdmin):
    search_field =['user', 'course']
    list_display = [ 'user', 'gender','course','contact', 'homeAddress']



class AluminAdmin(admin.ModelAdmin):
    search_field =['user', 'course']
    list_display = ['user' ,'gender','course','contact', 'occupation','homeAddress']


admin.site.register(User, UserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Alumin, AluminAdmin)