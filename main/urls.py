from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('templates/', views.templates, name='templates'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create/', views.create_resume, name='create_resume'),
    path('edit/<int:resume_id>/', views.edit_resume, name='edit_resume'),
    path('builder/<int:resume_id>/', views.builder_resume, name='builder_resume'),
    path('builder/<int:resume_id>/history/', views.builder_resume, name='resume_history'),
    path('view/<int:resume_id>/', views.view_resume, name='view_resume'),
    path('view/preview/<str:template_key>/', views.preview_template, name='preview_template'),
    path('export/<int:resume_id>/', views.export_resume_pdf, name='export_resume_pdf'),
    path('delete/<int:resume_id>/', views.delete_resume, name='delete_resume'),
    path('create/sample/<str:template_key>/', views.create_sample_resume, name='create_sample_resume'),
    path('about/', views.about, name='about'),
    # Tools
    path('tools/convert/', views.tools_convert, name='tools_convert'),
    path('tools/convert/image-to-pdf/', views.tool_image_to_pdf, name='tool_image_to_pdf'),
    path('tools/convert/pdf-to-images/', views.tool_pdf_to_images, name='tool_pdf_to_images'),
    
    # AJAX endpoints
    path('save-personal-info/<int:resume_id>/', views.save_personal_info, name='save_personal_info'),
    path('add-experience/<int:resume_id>/', views.add_experience, name='add_experience'),
    path('add-education/<int:resume_id>/', views.add_education, name='add_education'),
    path('add-skill/<int:resume_id>/', views.add_skill, name='add_skill'),
    path('add-project/<int:resume_id>/', views.add_project, name='add_project'),
]
