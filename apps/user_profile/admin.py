from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models.squadron import Squadron
from .models.user_profile import UserProfile

# Register your models here.

@admin.register(Squadron)
class SquadronAdmin(ImportExportModelAdmin):
    """Admin configuration for Squadron model."""
    
    list_display = ('name', 'url', 'date_created', 'date_modified', 'user')
    list_filter = ('date_created', 'date_modified')
    search_fields = ('name', 'url')
    date_hierarchy = 'date_created'

@admin.register(UserProfile)
class UserProfileAdmin(ImportExportModelAdmin):
    """Admin configuration for UserProfile model."""
    
    list_display = ('user', 'squadron', 'timezone', 'date_created', 'date_modified')
    list_filter = ('squadron', 'timezone', 'date_created', 'date_modified')
    search_fields = ('user__username', 'user__email', 'bio')
    date_hierarchy = 'date_created'
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'avatar', 'bio')
        }),
        ('Preferences', {
            'fields': ('squadron', 'timezone')
        }),
        ('Metadata', {
            'fields': ('date_created', 'date_modified')
        }),
    )
    readonly_fields = ('date_created', 'date_modified')
