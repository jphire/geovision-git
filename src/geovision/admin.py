from django.contrib import admin
from django.contrib.sites.models import Site
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import *

def _(x):
	return x

class MyUserAdmin(UserAdmin):
# Based on django UserAdmin
	fieldsets = (
		(None, {'fields': ('username', 'password')}),
		(_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
		(_('Permissions'), {'fields': ('is_active', 'is_staff',)}),
	)
def setup_admin():
	admin.site.unregister(Group)
	admin.site.unregister(Site)
	admin.site.unregister(User)
	admin.site.register(User, MyUserAdmin)
