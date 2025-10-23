from django.db import models
from django.contrib.auth.models import User

class Resume(models.Model):
    TEMPLATE_CHOICES = [
        ('modern', 'Modern'),
        ('classic', 'Classic'),
        ('creative', 'Creative'),
        ('minimal', 'Minimal'),
        ('elegant', 'Elegant'),
        ('professional', 'Professional'),
        ('executive', 'Executive'),
        ('tech', 'Tech'),
        ('simple', 'Simple'),
        ('bold', 'Bold'),
        ('compact', 'Compact'),
        ('timeline', 'Timeline'),
        ('sidebar', 'Sidebar'),
        ('infographic', 'Infographic'),
        ('corporate', 'Corporate'),
        ('academic', 'Academic'),
        ('graduate', 'Graduate'),
        ('junior', 'Junior'),
        ('senior', 'Senior'),
        ('developer', 'Developer'),
        ('custom', 'Custom Theme'),
        ('gradient', 'Gradient'),
        ('mono', 'Monochrome'),
        ('photo-left', 'Photo Left'),
        ('card', 'Card Sections'),
        ('material', 'Material'),
        ('neon', 'Neon'),
        ('pastel', 'Pastel'),
        ('newspaper', 'Newspaper'),
        ('grid', 'Grid'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    template = models.CharField(max_length=20, choices=TEMPLATE_CHOICES, default='modern')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Custom theme settings
    use_custom_theme = models.BooleanField(default=False)
    color_primary = models.CharField(max_length=32, blank=True, default='')
    color_secondary = models.CharField(max_length=32, blank=True, default='')
    color_accent = models.CharField(max_length=32, blank=True, default='')
    color_bg = models.CharField(max_length=32, blank=True, default='')
    color_text = models.CharField(max_length=32, blank=True, default='')
    font_family = models.CharField(max_length=64, blank=True, default='')
    # Audit trail
    history = models.JSONField(default=list, blank=True)
    
    def __str__(self):
        return f"{self.title} - {self.get_template_display()}"
    
    class Meta:
        ordering = ['-updated_at']

class PersonalInfo(models.Model):
    resume = models.OneToOneField(Resume, on_delete=models.CASCADE, related_name='personal_info')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    photo_url = models.URLField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    linkedin = models.URLField(blank=True)
    website = models.URLField(blank=True)
    summary = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Experience(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='experiences')
    company = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    current = models.BooleanField(default=False)
    description = models.TextField()
    
    def __str__(self):
        return f"{self.position} at {self.company}"
    
    class Meta:
        ordering = ['-start_date']

class Education(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='education')
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=200)
    field_of_study = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=200, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    current = models.BooleanField(default=False)
    gpa = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.degree} from {self.institution}"
    
    class Meta:
        ordering = ['-start_date']

class Skill(models.Model):
    SKILL_LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]
    
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=20, choices=SKILL_LEVEL_CHOICES, default='intermediate')
    
    def __str__(self):
        return f"{self.name} ({self.get_level_display()})"
    
    class Meta:
        ordering = ['name']

class Project(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=200)
    description = models.TextField()
    technologies = models.CharField(max_length=200, blank=True)
    url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-start_date']
