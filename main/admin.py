from django.contrib import admin
from .models import Resume, PersonalInfo, Experience, Education, Skill, Project

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'template', 'created_at', 'updated_at')
    list_filter = ('template', 'created_at', 'updated_at')
    search_fields = ('title', 'user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-updated_at',)

@admin.register(PersonalInfo)
class PersonalInfoAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'resume')
    list_filter = ('country',)
    search_fields = ('first_name', 'last_name', 'email', 'resume__title')
    ordering = ('last_name', 'first_name')

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('position', 'company', 'location', 'start_date', 'end_date', 'current', 'resume')
    list_filter = ('current', 'start_date', 'end_date')
    search_fields = ('position', 'company', 'resume__title')
    ordering = ('-start_date',)

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('degree', 'institution', 'field_of_study', 'start_date', 'end_date', 'current', 'resume')
    list_filter = ('current', 'start_date', 'end_date')
    search_fields = ('degree', 'institution', 'field_of_study', 'resume__title')
    ordering = ('-start_date',)

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'resume')
    list_filter = ('level',)
    search_fields = ('name', 'resume__title')
    ordering = ('name',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'technologies', 'start_date', 'end_date', 'resume')
    list_filter = ('start_date', 'end_date')
    search_fields = ('title', 'technologies', 'resume__title')
    ordering = ('-start_date',)
