from flask import Flask, render_template, request, flash, redirect, url_for, send_file
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
import os
from datetime import datetime
from dotenv import load_dotenv
import io

# Try to import reportlab, fall back to HTML version if not available
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    print("  ReportLab not installed. PDF download will use HTML version.")

# Load environment variables
load_dotenv()

# Import portfolio data
from data.portfolio_data import (
    PERSONAL_INFO,
    SOCIAL_LINKS,
    SKILLS,
    SERVICES,
    PROJECTS,
    EXPERIENCE,
    EDUCATION,
    CERTIFICATIONS,
    TESTIMONIALS,
    BLOG_POSTS,
    CORE_SKILLS,
    PROFESSIONAL_SKILLS,
    LANGUAGES,
    REFERENCES
)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# ===== CONTACT FORM =====
class ContactForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email Address', validators=[DataRequired(), Length(min=5, max=100)])
    subject = StringField('Subject', validators=[Length(max=200)])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10, max=2000)])
    submit = SubmitField('Send Message')

# ===== ROUTES =====

@app.route('/')
def index():
    """Home page / Hero section"""
    return render_template('index.html', 
                         personal=PERSONAL_INFO,
                         social=SOCIAL_LINKS,
                         testimonials=TESTIMONIALS,
                         projects=PROJECTS)

@app.route('/about')
def about():
    """About Me page"""
    return render_template('about.html', 
                         personal=PERSONAL_INFO,
                         social=SOCIAL_LINKS,
                         testimonials=TESTIMONIALS)

@app.route('/services')
def services():
    """Services / What I Do page"""
    return render_template('services.html', 
                         personal=PERSONAL_INFO,
                         social=SOCIAL_LINKS,
                         services=SERVICES)

@app.route('/resume')
def resume():
    """Resume / Experience page"""
    return render_template('resume.html', 
                         personal=PERSONAL_INFO,
                         social=SOCIAL_LINKS,
                         experience=EXPERIENCE,
                         education=EDUCATION,
                         certifications=CERTIFICATIONS,
                         skills=SKILLS,
                         core_skills=CORE_SKILLS,
                         professional_skills=PROFESSIONAL_SKILLS,
                         languages=LANGUAGES,
                         references=REFERENCES,
                         reportlab_available=REPORTLAB_AVAILABLE)

@app.route('/projects')
def projects():
    """Portfolio / Projects page"""
    return render_template('projects.html', 
                         personal=PERSONAL_INFO,
                         social=SOCIAL_LINKS,
                         projects=PROJECTS)

@app.route('/blog')
def blog():
    """Blog page"""
    return render_template('blog.html', 
                         personal=PERSONAL_INFO,
                         social=SOCIAL_LINKS,
                         blog_posts=BLOG_POSTS)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page with form"""
    form = ContactForm()
    
    if form.validate_on_submit():
        # Simple email validation (basic check)
        email = form.email.data
        if '@' not in email or '.' not in email:
            flash('Please enter a valid email address.', 'error')
            return render_template('contact.html', 
                                 form=form, 
                                 personal=PERSONAL_INFO, 
                                 social=SOCIAL_LINKS)
        
        flash('Thank you for your message! I\'ll get back to you soon.', 'success')
        return redirect(url_for('contact'))
    
    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{field}: {error}', 'error')
    
    return render_template('contact.html', 
                         form=form,
                         personal=PERSONAL_INFO,
                         social=SOCIAL_LINKS)

@app.route('/download-resume')
def download_resume():
    """Download resume as PDF"""
    if REPORTLAB_AVAILABLE:
        return generate_pdf_resume()
    else:
        # Fallback to HTML version that can be printed as PDF
        return render_template('resume_print.html', 
                             personal=PERSONAL_INFO,
                             experience=EXPERIENCE,
                             education=EDUCATION,
                             skills=SKILLS,
                             certifications=CERTIFICATIONS,
                             core_skills=CORE_SKILLS,
                             professional_skills=PROFESSIONAL_SKILLS,
                             languages=LANGUAGES,
                             references=REFERENCES)

def generate_pdf_resume():
    """Generate PDF using ReportLab"""
    try:
        # Create a buffer for the PDF
        buffer = io.BytesIO()
        
        # Create the PDF document
        doc = SimpleDocTemplate(buffer, pagesize=letter,
                               rightMargin=72, leftMargin=72,
                               topMargin=72, bottomMargin=72)
        
        # Get styles
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor='#D4AF37',
            alignment=TA_CENTER,
            spaceAfter=12
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor='#D4AF37',
            spaceAfter=8,
            spaceBefore=12
        )
        
        subheading_style = ParagraphStyle(
            'CustomSubheading',
            parent=styles['Heading3'],
            fontSize=14,
            textColor='#333333',
            spaceAfter=4
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['Normal'],
            fontSize=11,
            textColor='#444444',
            spaceAfter=6,
            alignment=TA_LEFT
        )
        
        # Build the PDF content
        story = []
        
        # Title
        story.append(Paragraph(f"{PERSONAL_INFO['name']}", title_style))
        story.append(Paragraph(f"{PERSONAL_INFO['title']}", body_style))
        story.append(Paragraph(f"{PERSONAL_INFO['location']}", body_style))
        story.append(Paragraph(f"{PERSONAL_INFO['email']} | {PERSONAL_INFO['phone']}", body_style))
        story.append(Spacer(1, 0.2*inch))
        story.append(HRFlowable(width="100%", thickness=1, color='#D4AF37'))
        story.append(Spacer(1, 0.2*inch))
        
        # Summary
        story.append(Paragraph("Professional Summary", heading_style))
        story.append(Paragraph(PERSONAL_INFO['bio'], body_style))
        story.append(Spacer(1, 0.1*inch))
        
        # Core Skills
        story.append(Paragraph("Core Skills", heading_style))
        core_skills_text = ', '.join(CORE_SKILLS)
        story.append(Paragraph(core_skills_text, body_style))
        story.append(Spacer(1, 0.1*inch))
        
        # Experience
        story.append(Paragraph("Professional Experience", heading_style))
        for exp in EXPERIENCE:
            story.append(Paragraph(f"<b>{exp['title']}</b>", subheading_style))
            period_location = exp['period']
            if exp.get('location'):
                period_location += f" · {exp['location']}"
            story.append(Paragraph(period_location, body_style))
            story.append(Paragraph(exp['company'], body_style))
            # Split description into bullet points
            desc_parts = exp['description'].split('. ')
            for part in desc_parts:
                if part.strip():
                    story.append(Paragraph(f"• {part.strip()}", body_style))
            story.append(Spacer(1, 0.1*inch))
        
        # Education
        story.append(Paragraph("Education", heading_style))
        for edu in EDUCATION:
            story.append(Paragraph(f"<b>{edu['degree']}</b>", subheading_style))
            story.append(Paragraph(f"{edu['period']} · {edu['institution']}", body_style))
            if edu.get('description'):
                story.append(Paragraph(edu['description'], body_style))
            story.append(Spacer(1, 0.1*inch))
        
        # Skills - Updated to match new structure
        story.append(Paragraph("Technical Skills", heading_style))
        
        # Programming Skills
        if SKILLS.get('programming'):
            story.append(Paragraph("<b>Programming:</b>", subheading_style))
            prog_skills = ', '.join(SKILLS['programming'])
            story.append(Paragraph(prog_skills, body_style))
        
        # Databases
        if SKILLS.get('databases'):
            story.append(Paragraph("<b>Databases:</b>", subheading_style))
            db_skills = ', '.join(SKILLS['databases'])
            story.append(Paragraph(db_skills, body_style))
        
        # Networking
        if SKILLS.get('networking'):
            story.append(Paragraph("<b>Networking:</b>", subheading_style))
            net_skills = ', '.join(SKILLS['networking'])
            story.append(Paragraph(net_skills, body_style))
        
        # Security
        if SKILLS.get('security'):
            story.append(Paragraph("<b>Security:</b>", subheading_style))
            sec_skills = ', '.join(SKILLS['security'])
            story.append(Paragraph(sec_skills, body_style))
        
        # IT Support
        if SKILLS.get('it_support'):
            story.append(Paragraph("<b>IT Support:</b>", subheading_style))
            support_skills = ', '.join(SKILLS['it_support'])
            story.append(Paragraph(support_skills, body_style))
        
        # Development
        if SKILLS.get('development'):
            story.append(Paragraph("<b>Development:</b>", subheading_style))
            dev_skills = ', '.join(SKILLS['development'])
            story.append(Paragraph(dev_skills, body_style))
        
        # Other
        if SKILLS.get('other'):
            story.append(Paragraph("<b>Other:</b>", subheading_style))
            other_skills = ', '.join(SKILLS['other'])
            story.append(Paragraph(other_skills, body_style))
        
        story.append(Spacer(1, 0.1*inch))
        
        # Professional Skills
        story.append(Paragraph("Professional Skills", heading_style))
        prof_skills_text = ', '.join(PROFESSIONAL_SKILLS)
        story.append(Paragraph(prof_skills_text, body_style))
        story.append(Spacer(1, 0.1*inch))
        
        # Languages
        story.append(Paragraph("Languages", heading_style))
        for lang in LANGUAGES:
            story.append(Paragraph(f"<b>{lang['name']}:</b> {lang['level']}", body_style))
        story.append(Spacer(1, 0.1*inch))
        
        # Certifications
        if CERTIFICATIONS:
            story.append(Paragraph("Certifications", heading_style))
            for cert in CERTIFICATIONS:
                story.append(Paragraph(f"<b>{cert['name']}</b>", subheading_style))
                issuer_date = cert['issuer']
                if cert.get('date') and cert['date']:
                    issuer_date += f" · {cert['date']}"
                story.append(Paragraph(issuer_date, body_style))
                if cert.get('credential') and cert['credential']:
                    story.append(Paragraph(f"ID: {cert['credential']}", body_style))
                story.append(Spacer(1, 0.05*inch))
        
        # References
        story.append(Paragraph("References", heading_style))
        for ref in REFERENCES:
            story.append(Paragraph(f"<b>{ref['name']}</b>", subheading_style))
            story.append(Paragraph(ref['title'], body_style))
            if ref.get('phone'):
                story.append(Paragraph(f"Phone: {ref['phone']}", body_style))
            if ref.get('email') and ref['email']:
                story.append(Paragraph(f"Email: {ref['email']}", body_style))
            story.append(Spacer(1, 0.05*inch))
        
        # Build PDF
        doc.build(story)
        
        # Get the value from the buffer
        buffer.seek(0)
        
        # Return the PDF as a download
        return send_file(
            buffer,
            as_attachment=True,
            download_name=f"{PERSONAL_INFO['name'].replace(' ', '_')}_Resume.pdf",
            mimetype='application/pdf'
        )
        
    except Exception as e:
        print(f"Error generating PDF: {e}")
        flash('Error generating PDF. Please try again.', 'error')
        return redirect(url_for('resume'))

# ===== ERROR HANDLERS =====

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', 
                         personal=PERSONAL_INFO, 
                         social=SOCIAL_LINKS), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html', 
                         personal=PERSONAL_INFO, 
                         social=SOCIAL_LINKS), 500

# ===== CONTEXT PROCESSOR =====

@app.context_processor
def inject_globals():
    """Inject global variables into all templates"""
    return {
        'current_year': datetime.now().year,
        'personal': PERSONAL_INFO,
        'social': SOCIAL_LINKS
    }

# ===== RUN APP =====

if __name__ == '__main__':
    # Get host and port from environment or use defaults
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    print(f" Starting Flask application...")
    print(f" Application will be available at: http://localhost:{port}")
    print(f" ReportLab available: {REPORTLAB_AVAILABLE}")
    print("Press Ctrl+C to stop the server")
    print("-" * 50)
    
    app.run(debug=debug, host=host, port=port)