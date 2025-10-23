<<<<<<< HEAD
# Resume Maker

A professional Django application for creating beautiful and professional resumes with multiple templates. Build stunning resumes that stand out and help you land your dream job.

## Features

- 🎨 **Multiple Templates**: Choose from Modern, Classic, Creative, and Minimal designs
- ✏️ **Easy Editor**: Simple and intuitive interface for building your resume
- 📱 **Responsive Design**: Works perfectly on all devices and screen sizes
- 💾 **Save & Edit**: Save your progress and edit anytime
- 📄 **PDF Export**: Download your resume as a professional PDF
- 🔒 **Secure**: Your data is safe with Django's built-in security features
- 🚀 **Fast & Efficient**: Built with Django's powerful framework

## Technology Stack

- **Django 5.2.5**: Web framework
- **Python 3.11+**: Programming language
- **Bootstrap 5.3**: Frontend framework
- **SQLite**: Database (can be easily changed to PostgreSQL/MySQL)

## Quick Start

### Prerequisites

- Python 3.11 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd resumw-project
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Open your browser**
   Navigate to `http://127.0.0.1:8000/`

## Project Structure

```
resumw-project/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── README.md                # Project documentation
├── resumw_project/          # Main project settings
│   ├── __init__.py
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL configuration
│   ├── wsgi.py              # WSGI configuration
│   └── asgi.py              # ASGI configuration
├── main/                    # Main application
│   ├── __init__.py
│   ├── admin.py             # Admin interface configuration
│   ├── apps.py              # App configuration
│   ├── models.py            # Database models (Resume, PersonalInfo, etc.)
│   ├── views.py             # View functions
│   ├── forms.py             # Django forms for data input
│   ├── urls.py              # App URL configuration
│   └── migrations/          # Database migrations
├── templates/               # HTML templates
│   ├── base.html            # Base template
│   └── main/                # App-specific templates
│       ├── home.html        # Home page
│       ├── templates.html   # Template selection page
│       ├── dashboard.html   # User dashboard
│       ├── create_resume.html # Resume creation page
│       ├── edit_resume.html # Resume editor
│       ├── view_resume.html # Resume viewer
│       └── about.html       # About page
└── static/                  # Static files (CSS, JS, images)
    ├── css/
    └── js/
```

## Available Pages

- **Home** (`/`): Welcome page with resume creation features
- **Templates** (`/templates/`): Browse available resume templates
- **Dashboard** (`/dashboard/`): Manage your created resumes
- **Create Resume** (`/create/`): Start building a new resume
- **Edit Resume** (`/edit/<id>/`): Edit existing resume content
- **View Resume** (`/view/<id>/`): Preview your resume
- **About** (`/about/`): Information about the application
- **Admin** (`/admin/`): Django admin interface

## Resume Templates

### 1. Modern Template
- **Best for**: Tech professionals, startups, modern companies
- **Features**: Clean layout, professional typography, ATS-friendly
- **Style**: Contemporary and sleek

### 2. Classic Template
- **Best for**: Traditional industries, corporate jobs
- **Features**: Traditional format, widely accepted, conservative style
- **Style**: Timeless and professional

### 3. Creative Template
- **Best for**: Designers, artists, creative professionals
- **Features**: Unique design, creative layout, eye-catching
- **Style**: Stand out and memorable

### 4. Minimal Template
- **Best for**: Students, recent graduates, content-focused resumes
- **Features**: Clean design, content focused, minimal distractions
- **Style**: Simple and elegant

## Admin Access

- **URL**: `http://127.0.0.1:8000/admin/`
- **Username**: `admin`
- **Password**: `admin123`

## Development

### Adding New Templates

1. Add template choice to `Resume.TEMPLATE_CHOICES` in `main/models.py`
2. Create template HTML file in `templates/main/resume_templates/`
3. Update template preview in `main/views.py`

### Adding New Resume Sections

1. Create model in `main/models.py`
2. Add form in `main/forms.py`
3. Update views in `main/views.py`
4. Create migration: `python manage.py makemigrations`

### Customizing Styles

- Edit `templates/base.html` for global styles
- Add custom CSS files to `static/css/`
- Bootstrap 5.3 is included for responsive design

## Resume Sections

The application supports the following resume sections:

- **Personal Information**: Name, contact details, summary
- **Experience**: Work history with company, position, dates
- **Education**: Academic background, degrees, institutions
- **Skills**: Technical and soft skills with proficiency levels
- **Projects**: Portfolio projects with descriptions and links

## Deployment

For production deployment, consider:

1. **Change DEBUG setting**: Set `DEBUG = False` in `settings.py`
2. **Use a production database**: PostgreSQL or MySQL
3. **Configure static files**: Use a CDN or web server
4. **Set up environment variables**: For sensitive settings
5. **Use HTTPS**: Configure SSL certificates
6. **Add PDF generation**: Install WeasyPrint or similar library

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

For support and questions, please open an issue on the project repository.
=======
# resume-creater
for create resume faster
>>>>>>> 74861fb1f39addc20d1564b5037e286ecc11e096
