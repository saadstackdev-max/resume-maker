from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.template.loader import render_to_string
from django.template import TemplateDoesNotExist
from .models import Resume, PersonalInfo, Experience, Education, Skill, Project
from .forms import ResumeForm, PersonalInfoForm, ExperienceForm, EducationForm, SkillForm, ProjectForm
from django.views.decorators.http import require_http_methods
from io import BytesIO
from zipfile import ZipFile
from PIL import Image
import re
try:
    import fitz  # PyMuPDF
except Exception:
    fitz = None
try:
    from weasyprint import HTML
except Exception:
    HTML = None

# Create your views here.

def home(request):
    return render(request, 'main/home.html', {
        'title': 'Resume Maker - Create Professional Resumes'
    })

def templates(request):
    templates_data = []
    for tpl_id, tpl_name in Resume.TEMPLATE_CHOICES:
        templates_data.append({
            'id': tpl_id,
            'name': tpl_name,
            'description': f'{tpl_name} resume layout',
            'features': ['ATS friendly', 'Responsive print', 'Clean hierarchy'],
            'preview_url': request.build_absolute_uri(f"/view/preview/{tpl_id}/")
        })
    return render(request, 'main/templates.html', {
        'templates': templates_data,
        'title': 'Resume Templates'
    })

def _seed_dummy_resume_data(resume: Resume):
    pi, _ = PersonalInfo.objects.get_or_create(
        resume=resume,
        defaults=dict(
            first_name='Alex', last_name='Doe', email='alex@example.com', phone='+1 555 123 4567',
            linkedin='https://linkedin.com/in/alexdoe', website='https://alex.dev',
            summary='Results-driven professional with 5+ years building impactful products.',
            city='San Francisco', state='CA', country='USA',
            photo_url='https://avatars.githubusercontent.com/u/9919?s=200&v=4',
        )
    )
    if resume.experiences.count() == 0:
        Experience.objects.create(resume=resume, company='TechCorp', position='Senior Developer',
                                  location='Remote', start_date=timezone.now().date().replace(year=2021, month=1, day=1),
                                  current=True, description='Built scalable services, mentored engineers, led delivery.')
    if resume.education.count() == 0:
        Education.objects.create(resume=resume, institution='State University', degree='B.Sc. Computer Science',
                                 field_of_study='Computer Science', start_date=timezone.now().date().replace(year=2015, month=9, day=1),
                                 end_date=timezone.now().date().replace(year=2019, month=6, day=1), gpa=3.8)
    if resume.skills.count() == 0:
        for n in ['Python','Django','PostgreSQL','Docker','AWS','Git','REST APIs']:
            Skill.objects.create(resume=resume, name=n)
    if resume.projects.count() == 0:
        Project.objects.create(resume=resume, title='Project Atlas', technologies='Django, DRF, React',
                               description='Platform for analytics with dashboards and APIs.',
                               github_url='https://github.com/example/project')

def _dummy_context_for_template(template_key: str):
    dummy_resume = Resume(id=0, title='Sample Resume', template=template_key)
    class P:
        first_name='Jamie'; last_name='Smith'; email='jamie@example.com'; phone='+1 555 111 2222'
        linkedin='https://linkedin.com/in/jamiesmith'; website='https://jamie.dev'; summary='Creative problem-solver.'
        address='123 Main St'; city='NYC'; state='NY'; zip_code='10001'; country='USA'; photo_url='https://placehold.co/140x140'
    experiences=[type('E',(),dict(position='Engineer',company='Acme',location='NY',start_date=timezone.now().date(),end_date=None,current=True,description='Did things.'))()]
    education=[type('Ed',(),dict(degree='B.Sc',institution='Uni',field_of_study='CS',location='NY',start_date=timezone.now().date(),end_date=timezone.now().date(),current=False,gpa=3.7,description='Honors'))()]
    skills=[type('S',(),dict(name='Python', get_level_display=lambda self='': 'Advanced'))(), type('S',(),dict(name='Django', get_level_display=lambda self='': 'Advanced'))()]
    projects=[type('P',(),dict(title='Demo',description='A sample project',technologies='Django',url='',github_url=''))()]
    return {
        'resume': dummy_resume,
        'personal_info': P,
        'experiences': experiences,
        'education': education,
        'skills': skills,
        'projects': projects,
        'title': 'Preview '
    }

def preview_template(request, template_key: str):
    # Render a template preview with dummy data (no auth required)
    try:
        context = _dummy_context_for_template(template_key)
        return render(request, f'main/resume_templates/{template_key}.html', context)
    except TemplateDoesNotExist:
        context = _dummy_context_for_template('modern')
        return render(request, 'main/resume_templates/modern.html', context)

@login_required
def create_sample_resume(request, template_key: str):
    resume = Resume.objects.create(user=request.user, title=f'My {template_key.title()} Resume', template=template_key)
    _seed_dummy_resume_data(resume)
    messages.success(request, 'Sample resume created. You can now customize it!')
    return redirect('main:edit_resume', resume_id=resume.id)

@login_required
def dashboard(request):
    resumes = Resume.objects.filter(user=request.user)
    return render(request, 'main/dashboard.html', {
        'resumes': resumes,
        'title': 'My Resumes'
    })

@login_required
def create_resume(request):
    selected_template = request.GET.get('template')
    # Enforce choose-template-first flow
    if request.method == 'GET' and not selected_template:
        messages.info(request, 'Please choose a template to start building your resume.')
        return redirect('main:templates')

    if request.method == 'POST':
        form = ResumeForm(request.POST)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume.save()
            messages.success(request, 'Resume created successfully!')
            return redirect('main:edit_resume', resume_id=resume.id)
    else:
        initial = {}
        if selected_template:
            initial['template'] = selected_template
        form = ResumeForm(initial=initial)
    
    return render(request, 'main/create_resume.html', {
        'form': form,
        'selected_template': selected_template,
        'title': 'Create New Resume'
    })

@login_required
def edit_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    
    if request.method == 'POST':
        form = ResumeForm(request.POST, instance=resume)
        if form.is_valid():
            updated_resume = form.save()
            updated_resume.history.append({
                'ts': timezone.now().isoformat(),
                'event': 'updated_settings',
                'by': request.user.username,
            })
            updated_resume.save(update_fields=['history'])
            messages.success(request, 'Resume updated successfully!')
            return redirect('main:edit_resume', resume_id=resume.id)
    else:
        form = ResumeForm(instance=resume)
    
    # Get or create personal info
    personal_info, created = PersonalInfo.objects.get_or_create(resume=resume)

    # Simple suggestions engine based on missing content and template choice
    suggestions: list[str] = []
    if not personal_info.first_name or not personal_info.last_name:
        suggestions.append('Add your first and last name to personalize the header.')
    if not personal_info.summary:
        suggestions.append('Write a concise professional summary (2-3 sentences).')
    if resume.experiences.count() == 0:
        suggestions.append('Add at least one work experience with achievements using action verbs.')
    if resume.education.count() == 0:
        suggestions.append('Include your most relevant education with degree and institution.')
    if resume.skills.count() < 5:
        suggestions.append('List 5-10 key skills that match the job description.')
    if resume.projects.count() == 0 and resume.template in {'tech','developer','creative'}:
        suggestions.append('Showcase 1-2 projects with links and your role/impact.')
    if resume.template in {'executive','professional','corporate'} and personal_info.linkedin == '':
        suggestions.append('Add your LinkedIn profile for professional credibility.')
    
    context = {
        'resume': resume,
        'form': form,
        'personal_info': personal_info,
        'experiences': resume.experiences.all(),
        'education': resume.education.all(),
        'skills': resume.skills.all(),
        'projects': resume.projects.all(),
        'suggestions': suggestions,
        'title': f'Edit {resume.title}'
    }
    
    return render(request, 'main/edit_resume.html', context)

@login_required
def view_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    
    context = {
        'resume': resume,
        'personal_info': getattr(resume, 'personal_info', None),
        'experiences': resume.experiences.all(),
        'education': resume.education.all(),
        'skills': resume.skills.all(),
        'projects': resume.projects.all(),
        'title': resume.title
    }
    
    template_name = f'main/resume_templates/{resume.template}.html'
    if resume.template == 'custom' or resume.use_custom_theme:
        template_name = 'main/resume_templates/custom.html'
    try:
        return render(request, template_name, context)
    except TemplateDoesNotExist:
        return render(request, 'main/resume_templates/modern.html', context)

@login_required
def export_resume_pdf(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    context = {
        'resume': resume,
        'personal_info': getattr(resume, 'personal_info', None),
        'experiences': resume.experiences.all(),
        'education': resume.education.all(),
        'skills': resume.skills.all(),
        'projects': resume.projects.all(),
    }
    template_name = f'main/resume_templates/{resume.template}.html'
    try:
        html_string = render_to_string(template_name, context, request=request)
    except TemplateDoesNotExist:
        html_string = render_to_string('main/resume_templates/modern.html', context, request=request)

    if HTML is None:
        messages.error(request, 'PDF export is not available on this server. Please install WeasyPrint.')
        return redirect('main:view_resume', resume_id=resume.id)

    pdf = HTML(string=html_string, base_url=request.build_absolute_uri('/')).write_pdf()
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{resume.title.replace(" ", "_")}.pdf"'
    return response

@login_required
def delete_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    if request.method == 'POST':
        resume.delete()
        messages.success(request, 'Resume deleted successfully!')
        return redirect('main:dashboard')
    
    return render(request, 'main/delete_resume.html', {
        'resume': resume,
        'title': 'Delete Resume'
    })

def about(request):
    return render(request, 'main/about.html', {
        'title': 'About Resume Maker'
    })

@login_required
def builder_resume(request, resume_id):
    """Split view: left forms, right live preview."""
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    if request.method == 'POST':
        form = ResumeForm(request.POST, instance=resume)
        if form.is_valid():
            updated_resume = form.save()
            updated_resume.history.append({
                'ts': timezone.now().isoformat(),
                'event': 'updated_settings',
                'by': request.user.username,
            })
            updated_resume.save(update_fields=['history'])
            messages.success(request, 'Resume updated successfully!')
            return redirect('main:builder_resume', resume_id=resume.id)
    else:
        form = ResumeForm(instance=resume)

    personal_info, _ = PersonalInfo.objects.get_or_create(resume=resume)
    suggestions = []
    if not personal_info.first_name or not personal_info.last_name:
        suggestions.append('Add your first and last name to personalize the header.')
    if not personal_info.summary:
        suggestions.append('Write a concise professional summary (2-3 sentences).')
    if resume.experiences.count() == 0:
        suggestions.append('Add at least one work experience with achievements using action verbs.')
    if resume.education.count() == 0:
        suggestions.append('Include your most relevant education with degree and institution.')
    if resume.skills.count() < 5:
        suggestions.append('List 5-10 key skills that match the job description.')

    context = {
        'resume': resume,
        'form': form,
        'personal_info': personal_info,
        'experiences': resume.experiences.all(),
        'education': resume.education.all(),
        'skills': resume.skills.all(),
        'projects': resume.projects.all(),
        'suggestions': suggestions,
        'title': f'Builder · {resume.title}'
    }
    return render(request, 'main/edit_resume_split.html', context)

# Tools: Image ↔ PDF
def tools_convert(request):
    return render(request, 'main/tools_convert.html', {
        'title': 'Convert: Image ↔ PDF'
    })

@require_http_methods(["POST"]) 
def tool_image_to_pdf(request):
    uploaded_files = request.FILES.getlist('images')
    if not uploaded_files:
        messages.error(request, 'Please upload at least one image.')
        return redirect('main:tools_convert')

    images = []
    for f in uploaded_files:
        try:
            img = Image.open(f)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            else:
                img = img.copy()
            images.append(img)
        except Exception:
            continue

    if not images:
        messages.error(request, 'Could not read any of the uploaded images.')
        return redirect('main:tools_convert')

    buf = BytesIO()
    if len(images) == 1:
        images[0].save(buf, format='PDF')
    else:
        images[0].save(buf, format='PDF', save_all=True, append_images=images[1:])
    buf.seek(0)

    response = HttpResponse(buf.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="images_to_pdf.pdf"'
    return response

@require_http_methods(["POST"]) 
def tool_pdf_to_images(request):
    if fitz is None:
        messages.error(request, 'PDF to Image requires PyMuPDF. Please ensure it is installed.')
        return redirect('main:tools_convert')

    pdf_file = request.FILES.get('pdf')
    fmt = request.POST.get('format', 'png').lower()
    if fmt not in {'png', 'jpg', 'jpeg'}:
        fmt = 'png'

    if not pdf_file:
        messages.error(request, 'Please upload a PDF file.')
        return redirect('main:tools_convert')

    data = pdf_file.read()
    doc = fitz.open(stream=data, filetype='pdf')
    zip_buf = BytesIO()
    with ZipFile(zip_buf, 'w') as zf:
        for i, page in enumerate(doc):
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
            img_bytes = pix.tobytes(output=fmt)
            safe_name = re.sub(r'[^A-Za-z0-9_.-]', '_', pdf_file.name.rsplit('.', 1)[0]) or 'page'
            zf.writestr(f"{safe_name}_page_{i+1}.{fmt if fmt != 'jpg' else 'jpg'}", img_bytes)
    doc.close()
    zip_buf.seek(0)

    resp = HttpResponse(zip_buf.getvalue(), content_type='application/zip')
    resp['Content-Disposition'] = 'attachment; filename="pdf_pages.zip"'
    return resp

# AJAX views for dynamic form handling
@login_required
@csrf_exempt
def save_personal_info(request, resume_id):
    if request.method == 'POST':
        resume = get_object_or_404(Resume, id=resume_id, user=request.user)
        personal_info, created = PersonalInfo.objects.get_or_create(resume=resume)
        
        form = PersonalInfoForm(request.POST, instance=personal_info)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@login_required
@csrf_exempt
def add_experience(request, resume_id):
    if request.method == 'POST':
        resume = get_object_or_404(Resume, id=resume_id, user=request.user)
        form = ExperienceForm(request.POST)
        if form.is_valid():
            experience = form.save(commit=False)
            experience.resume = resume
            experience.save()
            return JsonResponse({'status': 'success', 'id': experience.id})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@login_required
@csrf_exempt
def add_education(request, resume_id):
    if request.method == 'POST':
        resume = get_object_or_404(Resume, id=resume_id, user=request.user)
        form = EducationForm(request.POST)
        if form.is_valid():
            education = form.save(commit=False)
            education.resume = resume
            education.save()
            return JsonResponse({'status': 'success', 'id': education.id})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@login_required
@csrf_exempt
def add_skill(request, resume_id):
    if request.method == 'POST':
        resume = get_object_or_404(Resume, id=resume_id, user=request.user)
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.resume = resume
            skill.save()
            return JsonResponse({'status': 'success', 'id': skill.id})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@login_required
@csrf_exempt
def add_project(request, resume_id):
    if request.method == 'POST':
        resume = get_object_or_404(Resume, id=resume_id, user=request.user)
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.resume = resume
            project.save()
            return JsonResponse({'status': 'success', 'id': project.id})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
