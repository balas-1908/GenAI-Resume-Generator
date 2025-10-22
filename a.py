import streamlit as st
from fpdf import FPDF
import io
from datetime import datetime

# Page configuration
st.set_page_config(page_title="Resume Generator", page_icon="📄", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        padding: 0.5rem;
        border-radius: 5px;
    }
    .template-card {
        border: 2px solid #ddd;
        border-radius: 10px;
        padding: 20px;
        margin: 10px;
        cursor: pointer;
        transition: all 0.3s;
    }
    .template-card:hover {
        border-color: #4CAF50;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'input'
if 'selected_template' not in st.session_state:
    st.session_state.selected_template = None
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}

# Template definitions
TEMPLATES = {
    "Professional": {
        "name": "Professional",
        "description": "Clean and professional design suitable for corporate roles",
        "color": "#2C3E50"
    },
    "Modern": {
        "name": "Modern",
        "description": "Contemporary design with accent colors",
        "color": "#3498DB"
    },
    "Creative": {
        "name": "Creative",
        "description": "Bold and creative layout for design roles",
        "color": "#E74C3C"
    },
    "Minimal": {
        "name": "Minimal",
        "description": "Minimalist design with maximum readability",
        "color": "#95A5A6"
    },
    "Executive": {
        "name": "Executive",
        "description": "Elegant design for senior positions",
        "color": "#8E44AD"
    }
}

class ResumePDF(FPDF):
    def __init__(self, template_color):
        super().__init__()
        self.template_color = template_color
        
    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def create_professional_resume(data):
    pdf = ResumePDF(TEMPLATES["Professional"]["color"])
    pdf.add_page()
    color_rgb = pdf.hex_to_rgb(TEMPLATES["Professional"]["color"])
    
    # Header with background
    pdf.set_fill_color(*color_rgb)
    pdf.rect(0, 0, 210, 45, 'F')
    
    # Name
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Arial', 'B', 24)
    pdf.cell(0, 20, data.get('name', ''), 0, 1, 'C')
    
    # Contact Info
    pdf.set_font('Arial', '', 10)
    contact = f"{data.get('email', '')} | {data.get('phone', '')} | {data.get('location', '')}"
    pdf.cell(0, 8, contact, 0, 1, 'C')
    
    if data.get('linkedin') or data.get('portfolio'):
        links = f"{data.get('linkedin', '')}  {data.get('portfolio', '')}"
        pdf.cell(0, 8, links, 0, 1, 'C')
    
    pdf.set_text_color(0, 0, 0)
    pdf.ln(5)
    
    # Profile Summary
    if data.get('summary'):
        pdf.set_fill_color(*color_rgb)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 8, 'PROFESSIONAL SUMMARY', 0, 1, 'L', True)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font('Arial', '', 10)
        pdf.multi_cell(0, 5, data['summary'])
        pdf.ln(3)
    
    # Education
    if data.get('education'):
        pdf.set_fill_color(*color_rgb)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 8, 'EDUCATION', 0, 1, 'L', True)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font('Arial', '', 10)
        
        for edu in data['education']:
            if edu.get('degree'):
                pdf.set_font('Arial', 'B', 11)
                pdf.cell(0, 6, edu.get('degree', ''), 0, 1)
                pdf.set_font('Arial', '', 10)
                pdf.cell(0, 5, f"{edu.get('institution', '')} | {edu.get('year', '')}", 0, 1)
                if edu.get('gpa'):
                    pdf.cell(0, 5, f"GPA: {edu['gpa']}", 0, 1)
                pdf.ln(2)
    
    # Experience
    if data.get('experience'):
        pdf.set_fill_color(*color_rgb)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 8, 'WORK EXPERIENCE', 0, 1, 'L', True)
        pdf.set_text_color(0, 0, 0)
        
        for exp in data['experience']:
            if exp.get('position'):
                pdf.set_font('Arial', 'B', 11)
                pdf.cell(0, 6, exp.get('position', ''), 0, 1)
                pdf.set_font('Arial', 'I', 10)
                pdf.cell(0, 5, f"{exp.get('company', '')} | {exp.get('duration', '')}", 0, 1)
                pdf.set_font('Arial', '', 10)
                if exp.get('description'):
                    responsibilities = exp['description'].split('\n')
                    for resp in responsibilities:
                        if resp.strip():
                            pdf.cell(5)
                            pdf.multi_cell(0, 5, f"- {resp.strip()}")
                pdf.ln(2)
    
    # Projects
    if data.get('projects'):
        pdf.set_fill_color(*color_rgb)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 8, 'PROJECTS', 0, 1, 'L', True)
        pdf.set_text_color(0, 0, 0)
        
        for proj in data['projects']:
            if proj.get('title'):
                pdf.set_font('Arial', 'B', 11)
                pdf.cell(0, 6, proj.get('title', ''), 0, 1)
                pdf.set_font('Arial', '', 10)
                if proj.get('description'):
                    pdf.multi_cell(0, 5, proj['description'])
                if proj.get('technologies'):
                    pdf.set_font('Arial', 'I', 9)
                    pdf.multi_cell(0, 5, f"Technologies: {proj['technologies']}")
                pdf.ln(2)
    
    # Skills
    if data.get('skills'):
        pdf.set_fill_color(*color_rgb)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 8, 'SKILLS', 0, 1, 'L', True)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font('Arial', '', 10)
        pdf.multi_cell(0, 5, data['skills'])
    
    return pdf

def create_modern_resume(data):
    pdf = ResumePDF(TEMPLATES["Modern"]["color"])
    pdf.add_page()
    color_rgb = pdf.hex_to_rgb(TEMPLATES["Modern"]["color"])
    
    # Left sidebar background
    pdf.set_fill_color(*color_rgb)
    pdf.rect(0, 0, 70, 297, 'F')
    
    # Name in sidebar
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Arial', 'B', 20)
    pdf.set_xy(5, 20)
    pdf.multi_cell(60, 8, data.get('name', ''), 0, 'C')
    
    pdf.set_font('Arial', '', 9)
    pdf.set_xy(5, 45)
    
    # Contact in sidebar
    if data.get('phone'):
        pdf.cell(60, 5, data['phone'], 0, 1, 'C')
    if data.get('email'):
        pdf.multi_cell(60, 5, data['email'], 0, 'C')
    if data.get('location'):
        pdf.set_xy(5, pdf.get_y())
        pdf.multi_cell(60, 5, data['location'], 0, 'C')
    
    # Skills in sidebar
    if data.get('skills'):
        pdf.set_xy(5, pdf.get_y() + 10)
        pdf.set_font('Arial', 'B', 11)
        pdf.cell(60, 6, 'SKILLS', 0, 1, 'C')
        pdf.set_font('Arial', '', 8)
        skills_list = data['skills'].split(',')
        for skill in skills_list[:8]:
            pdf.set_x(5)
            pdf.multi_cell(60, 5, f"- {skill.strip()}", 0, 'L')
    
    # Main content area
    pdf.set_text_color(0, 0, 0)
    pdf.set_xy(75, 20)
    
    # Summary
    if data.get('summary'):
        pdf.set_font('Arial', 'B', 14)
        pdf.set_text_color(*color_rgb)
        pdf.cell(0, 8, 'PROFILE', 0, 1)
        pdf.set_x(75)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font('Arial', '', 10)
        pdf.multi_cell(0, 5, data['summary'])
        pdf.ln(3)
    
    # Experience
    if data.get('experience'):
        pdf.set_x(75)
        pdf.set_font('Arial', 'B', 14)
        pdf.set_text_color(*color_rgb)
        pdf.cell(0, 8, 'EXPERIENCE', 0, 1)
        pdf.set_text_color(0, 0, 0)
        
        for exp in data['experience']:
            if exp.get('position'):
                pdf.set_x(75)
                pdf.set_font('Arial', 'B', 11)
                pdf.cell(0, 6, exp.get('position', ''), 0, 1)
                pdf.set_x(75)
                pdf.set_font('Arial', 'I', 10)
                pdf.cell(0, 5, f"{exp.get('company', '')} | {exp.get('duration', '')}", 0, 1)
                pdf.set_x(75)
                pdf.set_font('Arial', '', 9)
                if exp.get('description'):
                    for line in exp['description'].split('\n'):
                        if line.strip():
                            pdf.set_x(75)
                            pdf.multi_cell(0, 5, f"- {line.strip()}")
                pdf.ln(2)
    
    # Education
    if data.get('education'):
        pdf.set_x(75)
        pdf.set_font('Arial', 'B', 14)
        pdf.set_text_color(*color_rgb)
        pdf.cell(0, 8, 'EDUCATION', 0, 1)
        pdf.set_text_color(0, 0, 0)
        
        for edu in data['education']:
            if edu.get('degree'):
                pdf.set_x(75)
                pdf.set_font('Arial', 'B', 11)
                pdf.cell(0, 6, edu.get('degree', ''), 0, 1)
                pdf.set_x(75)
                pdf.set_font('Arial', '', 10)
                pdf.cell(0, 5, f"{edu.get('institution', '')} | {edu.get('year', '')}", 0, 1)
                pdf.ln(2)
    
    return pdf

def create_minimal_resume(data):
    pdf = ResumePDF(TEMPLATES["Minimal"]["color"])
    pdf.add_page()
    
    # Name
    pdf.set_font('Arial', 'B', 28)
    pdf.cell(0, 15, data.get('name', ''), 0, 1, 'C')
    
    # Contact
    pdf.set_font('Arial', '', 10)
    contact = f"{data.get('email', '')} | {data.get('phone', '')} | {data.get('location', '')}"
    pdf.cell(0, 6, contact, 0, 1, 'C')
    pdf.ln(5)
    
    # Horizontal line
    pdf.set_draw_color(200, 200, 200)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    # Summary
    if data.get('summary'):
        pdf.set_font('Arial', '', 10)
        pdf.multi_cell(0, 5, data['summary'])
        pdf.ln(5)
    
    # Experience
    if data.get('experience'):
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 8, 'Experience', 0, 1)
        pdf.set_draw_color(200, 200, 200)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(3)
        
        for exp in data['experience']:
            if exp.get('position'):
                pdf.set_font('Arial', 'B', 11)
                pdf.cell(95, 6, exp.get('position', ''), 0, 0)
                pdf.set_font('Arial', '', 10)
                pdf.cell(0, 6, exp.get('duration', ''), 0, 1, 'R')
                pdf.set_font('Arial', 'I', 10)
                pdf.cell(0, 5, exp.get('company', ''), 0, 1)
                pdf.set_font('Arial', '', 9)
                if exp.get('description'):
                    for line in exp['description'].split('\n'):
                        if line.strip():
                            pdf.multi_cell(0, 5, f"- {line.strip()}")
                pdf.ln(3)
    
    # Education
    if data.get('education'):
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 8, 'Education', 0, 1)
        pdf.set_draw_color(200, 200, 200)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(3)
        
        for edu in data['education']:
            if edu.get('degree'):
                pdf.set_font('Arial', 'B', 11)
                pdf.cell(95, 6, edu.get('degree', ''), 0, 0)
                pdf.set_font('Arial', '', 10)
                pdf.cell(0, 6, edu.get('year', ''), 0, 1, 'R')
                pdf.set_font('Arial', '', 10)
                pdf.cell(0, 5, edu.get('institution', ''), 0, 1)
                pdf.ln(2)
    
    # Projects
    if data.get('projects'):
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 8, 'Projects', 0, 1)
        pdf.set_draw_color(200, 200, 200)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(3)
        
        for proj in data['projects']:
            if proj.get('title'):
                pdf.set_font('Arial', 'B', 11)
                pdf.cell(0, 6, proj.get('title', ''), 0, 1)
                pdf.set_font('Arial', '', 9)
                if proj.get('description'):
                    pdf.multi_cell(0, 5, proj['description'])
                pdf.ln(2)
    
    # Skills
    if data.get('skills'):
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 8, 'Skills', 0, 1)
        pdf.set_draw_color(200, 200, 200)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(3)
        pdf.set_font('Arial', '', 10)
        pdf.multi_cell(0, 5, data['skills'])
    
    return pdf

def create_creative_resume(data):
    pdf = ResumePDF(TEMPLATES["Creative"]["color"])
    pdf.add_page()
    color_rgb = pdf.hex_to_rgb(TEMPLATES["Creative"]["color"])
    
    # Header with angled design
    pdf.set_fill_color(*color_rgb)
    pdf.rect(0, 0, 210, 50, 'F')
    
    # Name
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Arial', 'B', 26)
    pdf.set_xy(15, 15)
    pdf.cell(0, 10, data.get('name', ''), 0, 1)
    
    # Job Role
    if data.get('job_role'):
        pdf.set_font('Arial', '', 12)
        pdf.set_x(15)
        pdf.cell(0, 8, data['job_role'], 0, 1)
    
    # Contact
    pdf.set_font('Arial', '', 9)
    pdf.set_x(15)
    contact = f"{data.get('email', '')} | {data.get('phone', '')} | {data.get('location', '')}"
    pdf.cell(0, 6, contact, 0, 1)
    
    pdf.set_text_color(0, 0, 0)
    pdf.ln(8)
    
    # Two column layout
    col_width = 90
    
    # Left column - Summary and Skills
    pdf.set_xy(15, 60)
    if data.get('summary'):
        pdf.set_fill_color(240, 240, 240)
        pdf.rect(15, pdf.get_y(), col_width, 5, 'F')
        pdf.set_font('Arial', 'B', 11)
        pdf.set_text_color(*color_rgb)
        pdf.cell(col_width, 5, 'ABOUT ME', 0, 1)
        pdf.set_x(15)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font('Arial', '', 9)
        pdf.multi_cell(col_width, 5, data['summary'])
        pdf.ln(3)
    
    # Skills
    if data.get('skills'):
        pdf.set_x(15)
        pdf.set_fill_color(240, 240, 240)
        pdf.rect(15, pdf.get_y(), col_width, 5, 'F')
        pdf.set_font('Arial', 'B', 11)
        pdf.set_text_color(*color_rgb)
        pdf.cell(col_width, 5, 'SKILLS', 0, 1)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font('Arial', '', 9)
        pdf.set_x(15)
        pdf.multi_cell(col_width, 5, data['skills'])
    
    # Right column - Experience and Education
    pdf.set_xy(110, 60)
    
    if data.get('experience'):
        pdf.set_fill_color(240, 240, 240)
        pdf.rect(110, pdf.get_y(), col_width, 5, 'F')
        pdf.set_font('Arial', 'B', 11)
        pdf.set_text_color(*color_rgb)
        pdf.cell(col_width, 5, 'EXPERIENCE', 0, 1)
        pdf.set_text_color(0, 0, 0)
        
        for exp in data['experience'][:2]:
            if exp.get('position'):
                pdf.set_x(110)
                pdf.set_font('Arial', 'B', 10)
                pdf.cell(0, 5, exp.get('position', ''), 0, 1)
                pdf.set_x(110)
                pdf.set_font('Arial', 'I', 9)
                pdf.cell(0, 4, f"{exp.get('company', '')} - {exp.get('duration', '')}", 0, 1)
                pdf.set_x(110)
                pdf.set_font('Arial', '', 8)
                if exp.get('description'):
                    lines = exp['description'].split('\n')[:3]
                    for line in lines:
                        if line.strip():
                            pdf.set_x(110)
                            pdf.multi_cell(col_width, 4, f"- {line.strip()}")
                pdf.ln(2)
    
    if data.get('education'):
        pdf.set_x(110)
        pdf.set_fill_color(240, 240, 240)
        pdf.rect(110, pdf.get_y(), col_width, 5, 'F')
        pdf.set_font('Arial', 'B', 11)
        pdf.set_text_color(*color_rgb)
        pdf.cell(col_width, 5, 'EDUCATION', 0, 1)
        pdf.set_text_color(0, 0, 0)
        
        for edu in data['education']:
            if edu.get('degree'):
                pdf.set_x(110)
                pdf.set_font('Arial', 'B', 10)
                pdf.cell(0, 5, edu.get('degree', ''), 0, 1)
                pdf.set_x(110)
                pdf.set_font('Arial', '', 9)
                pdf.cell(0, 4, edu.get('institution', ''), 0, 1)
    
    return pdf

def create_executive_resume(data):
    pdf = ResumePDF(TEMPLATES["Executive"]["color"])
    pdf.add_page()
    color_rgb = pdf.hex_to_rgb(TEMPLATES["Executive"]["color"])
    
    # Elegant header
    pdf.set_font('Arial', 'B', 24)
    pdf.set_text_color(*color_rgb)
    pdf.cell(0, 12, data.get('name', ''), 0, 1, 'C')
    
    pdf.set_font('Arial', '', 10)
    pdf.set_text_color(100, 100, 100)
    if data.get('job_role'):
        pdf.cell(0, 6, data['job_role'], 0, 1, 'C')
    
    contact = f"{data.get('email', '')} - {data.get('phone', '')} - {data.get('location', '')}"
    pdf.cell(0, 6, contact, 0, 1, 'C')
    
    pdf.set_draw_color(*color_rgb)
    pdf.set_line_width(0.5)
    pdf.line(20, pdf.get_y() + 3, 190, pdf.get_y() + 3)
    pdf.ln(8)
    
    pdf.set_text_color(0, 0, 0)
    
    # Executive Summary
    if data.get('summary'):
        pdf.set_font('Arial', 'B', 13)
        pdf.set_text_color(*color_rgb)
        pdf.cell(0, 8, 'EXECUTIVE SUMMARY', 0, 1)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font('Arial', '', 10)
        pdf.multi_cell(0, 6, data['summary'])
        pdf.ln(4)
    
    # Professional Experience
    if data.get('experience'):
        pdf.set_font('Arial', 'B', 13)
        pdf.set_text_color(*color_rgb)
        pdf.cell(0, 8, 'PROFESSIONAL EXPERIENCE', 0, 1)
        pdf.set_text_color(0, 0, 0)
        
        for exp in data['experience']:
            if exp.get('position'):
                pdf.set_font('Arial', 'B', 12)
                pdf.cell(120, 6, exp.get('position', ''), 0, 0)
                pdf.set_font('Arial', '', 10)
                pdf.cell(0, 6, exp.get('duration', ''), 0, 1, 'R')
                pdf.set_font('Arial', 'I', 11)
                pdf.cell(0, 6, exp.get('company', ''), 0, 1)
                pdf.set_font('Arial', '', 10)
                if exp.get('description'):
                    for line in exp['description'].split('\n'):
                        if line.strip():
                            pdf.multi_cell(0, 5, f"- {line.strip()}")
                pdf.ln(3)
    
    # Education & Qualifications
    if data.get('education'):
        pdf.set_font('Arial', 'B', 13)
        pdf.set_text_color(*color_rgb)
        pdf.cell(0, 8, 'EDUCATION & QUALIFICATIONS', 0, 1)
        pdf.set_text_color(0, 0, 0)
        
        for edu in data['education']:
            if edu.get('degree'):
                pdf.set_font('Arial', 'B', 11)
                pdf.cell(0, 6, edu.get('degree', ''), 0, 1)
                pdf.set_font('Arial', '', 10)
                pdf.cell(120, 5, edu.get('institution', ''), 0, 0)
                pdf.cell(0, 5, edu.get('year', ''), 0, 1, 'R')
                pdf.ln(2)
    
    # Core Competencies
    if data.get('skills'):
        pdf.set_font('Arial', 'B', 13)
        pdf.set_text_color(*color_rgb)
        pdf.cell(0, 8, 'CORE COMPETENCIES', 0, 1)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font('Arial', '', 10)
        pdf.multi_cell(0, 6, data['skills'])
    
    return pdf

def generate_resume(template_name, data):
    if template_name == "Professional":
        return create_professional_resume(data)
    elif template_name == "Modern":
        return create_modern_resume(data)
    elif template_name == "Minimal":
        return create_minimal_resume(data)
    elif template_name == "Creative":
        return create_creative_resume(data)
    elif template_name == "Executive":
        return create_executive_resume(data)

# Main Application
st.title("📄 Professional Resume Generator")
st.markdown("Create your professional resume in minutes with our beautiful templates!")

# Sidebar navigation
with st.sidebar:
    st.header("Navigation")
    if st.button("📝 Enter Details"):
        st.session_state.page = 'input'
    if st.button("🎨 Choose Template"):
        st.session_state.page = 'template'
    if st.session_state.selected_template:
        if st.button("👀 Preview & Download"):
            st.session_state.page = 'preview'

# INPUT PAGE
if st.session_state.page == 'input':
    st.header("Enter Your Details")
    
    with st.form("resume_form"):
        # Personal Information
        st.subheader("Personal Information")
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name*", value=st.session_state.user_data.get('name', ''))
            email = st.text_input("Email*", value=st.session_state.user_data.get('email', ''))
            phone = st.text_input("Phone*", value=st.session_state.user_data.get('phone', ''))
        with col2:
            job_role = st.text_input("Job Role/Title", value=st.session_state.user_data.get('job_role', ''))
            location = st.text_input("Location", value=st.session_state.user_data.get('location', ''))
            linkedin = st.text_input("LinkedIn", value=st.session_state.user_data.get('linkedin', ''))
        
        portfolio = st.text_input("Portfolio/Website", value=st.session_state.user_data.get('portfolio', ''))
        
        # Professional Summary
        st.subheader("Professional Summary")
        summary = st.text_area("Write a brief summary about yourself", 
                               value=st.session_state.user_data.get('summary', ''),
                               height=100)
        
        # Education
        st.subheader("Education")
        num_education = st.number_input("Number of Education Entries", min_value=1, max_value=5, value=1)
        education = []
        for i in range(int(num_education)):
            st.markdown(f"**Education {i+1}**")
            col1, col2 = st.columns(2)
            with col1:
                degree = st.text_input(f"Degree/Qualification", key=f"degree_{i}")
                institution = st.text_input(f"Institution", key=f"institution_{i}")
            with col2:
                year = st.text_input(f"Year", key=f"year_{i}")
                gpa = st.text_input(f"GPA/Grade (optional)", key=f"gpa_{i}")
            education.append({"degree": degree, "institution": institution, "year": year, "gpa": gpa})
        
        # Work Experience
        st.subheader("Work Experience")
        num_experience = st.number_input("Number of Experience Entries", min_value=1, max_value=5, value=1)
        experience = []
        for i in range(int(num_experience)):
            st.markdown(f"**Experience {i+1}**")
            col1, col2 = st.columns(2)
            with col1:
                position = st.text_input(f"Position/Job Title", key=f"position_{i}")
                company = st.text_input(f"Company", key=f"company_{i}")
            with col2:
                duration = st.text_input(f"Duration (e.g., Jan 2020 - Present)", key=f"duration_{i}")
            description = st.text_area(f"Job Description (separate points with new lines)", key=f"exp_desc_{i}", height=100)
            experience.append({"position": position, "company": company, "duration": duration, "description": description})
        
        # Projects
        st.subheader("Projects (Optional)")
        num_projects = st.number_input("Number of Projects", min_value=0, max_value=5, value=0)
        projects = []
        for i in range(int(num_projects)):
            st.markdown(f"**Project {i+1}**")
            col1, col2 = st.columns(2)
            with col1:
                project_title = st.text_input(f"Project Title", key=f"proj_title_{i}")
            with col2:
                technologies = st.text_input(f"Technologies Used", key=f"proj_tech_{i}")
            project_desc = st.text_area(f"Project Description", key=f"proj_desc_{i}", height=80)
            projects.append({"title": project_title, "description": project_desc, "technologies": technologies})
        
        # Skills
        st.subheader("Skills")
        skills = st.text_area("List your skills (separate with commas or new lines)", 
                             value=st.session_state.user_data.get('skills', ''),
                             height=80,
                             placeholder="Python, JavaScript, Project Management, Communication...")
        
        # Submit button
        submitted = st.form_submit_button("💾 Save Details & Continue to Templates")
        
        if submitted:
            if not name or not email or not phone:
                st.error("❌ Please fill in all required fields (Name, Email, Phone)")
            else:
                st.session_state.user_data = {
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "job_role": job_role,
                    "location": location,
                    "linkedin": linkedin,
                    "portfolio": portfolio,
                    "summary": summary,
                    "education": education,
                    "experience": experience,
                    "projects": projects,
                    "skills": skills
                }
                st.success("✅ Details saved successfully!")
                st.info("👈 Click 'Choose Template' in the sidebar to select your resume design")

# TEMPLATE SELECTION PAGE
elif st.session_state.page == 'template':
    st.header("Choose Your Resume Template")
    
    if not st.session_state.user_data:
        st.warning("⚠️ Please enter your details first!")
        if st.button("Go to Details Entry"):
            st.session_state.page = 'input'
    else:
        st.markdown("Select a template that best fits your professional style:")
        
        # Display templates in grid
        cols = st.columns(3)
        template_keys = list(TEMPLATES.keys())
        
        for idx, (template_name, template_info) in enumerate(TEMPLATES.items()):
            with cols[idx % 3]:
                st.markdown(f"""
                <div style='border: 3px solid {template_info['color']}; 
                            border-radius: 10px; 
                            padding: 20px; 
                            text-align: center;
                            background: linear-gradient(135deg, {template_info['color']}15 0%, {template_info['color']}05 100%);
                            margin-bottom: 20px;'>
                    <h3 style='color: {template_info['color']};'>{template_info['name']}</h3>
                    <p style='font-size: 14px; color: #666;'>{template_info['description']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Select {template_name}", key=f"select_{template_name}", use_container_width=True):
                    st.session_state.selected_template = template_name
                    st.success(f"✅ {template_name} template selected!")
                    st.info("👈 Click 'Preview & Download' in the sidebar to see your resume")

# PREVIEW AND DOWNLOAD PAGE
elif st.session_state.page == 'preview':
    st.header("Preview & Download Your Resume")
    
    if not st.session_state.user_data or not st.session_state.selected_template:
        st.warning("⚠️ Please complete the previous steps first!")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Go to Details Entry"):
                st.session_state.page = 'input'
        with col2:
            if st.button("Go to Template Selection"):
                st.session_state.page = 'template'
    else:
        st.success(f"✅ Resume generated using **{st.session_state.selected_template}** template")
        
        # Generate PDF
        try:
            pdf = generate_resume(st.session_state.selected_template, st.session_state.user_data)
            # Generate PDF as bytes
            pdf_bytes = pdf.output(dest='S')
            if isinstance(pdf_bytes, str):
                pdf_output = pdf_bytes.encode('latin-1', errors='ignore')
            else:
                pdf_output = pdf_bytes
            
            # Create download button
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.download_button(
                    label="📥 Download Resume (PDF)",
                    data=pdf_output,
                    file_name=f"{st.session_state.user_data.get('name', 'resume').replace(' ', '_')}_resume.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            
            st.markdown("---")
            
            # VISUAL PREVIEW OF RESUME
            st.subheader("📄 Resume Preview")
            
            # Get template color
            template_color = TEMPLATES[st.session_state.selected_template]["color"]
            data = st.session_state.user_data
            
            # Create visual preview card
            st.markdown(f"""
            <div style='border: 3px solid {template_color}; border-radius: 15px; padding: 30px; 
                        background: white; box-shadow: 0 8px 16px rgba(0,0,0,0.1); margin: 20px 0;'>
                
                <!-- Header Section -->
                <div style='background: linear-gradient(135deg, {template_color} 0%, {template_color}dd 100%); 
                            padding: 30px; border-radius: 10px; margin-bottom: 25px; text-align: center;'>
                    <h1 style='color: white; margin: 0; font-size: 36px; font-weight: bold;'>{data.get('name', '')}</h1>
                    <p style='color: white; margin: 10px 0 5px 0; font-size: 18px; opacity: 0.95;'>{data.get('job_role', '')}</p>
                    <p style='color: white; margin: 5px 0; font-size: 14px; opacity: 0.9;'>
                        {data.get('email', '')} | {data.get('phone', '')} | {data.get('location', '')}
                    </p>
                    {f"<p style='color: white; margin: 5px 0; font-size: 13px; opacity: 0.85;'>{data.get('linkedin', '')} | {data.get('portfolio', '')}</p>" if data.get('linkedin') or data.get('portfolio') else ''}
                </div>
                
                <!-- Professional Summary -->
                {f'''
                <div style='margin-bottom: 25px;'>
                    <h3 style='color: {template_color}; border-bottom: 3px solid {template_color}; 
                               padding-bottom: 8px; margin-bottom: 15px; font-size: 20px;'>
                        💼 PROFESSIONAL SUMMARY
                    </h3>
                    <p style='color: #333; line-height: 1.8; font-size: 15px; text-align: justify;'>
                        {data.get('summary', '')}
                    </p>
                </div>
                ''' if data.get('summary') else ''}
                
                <!-- Work Experience -->
                {f'''
                <div style='margin-bottom: 25px;'>
                    <h3 style='color: {template_color}; border-bottom: 3px solid {template_color}; 
                               padding-bottom: 8px; margin-bottom: 15px; font-size: 20px;'>
                        💼 WORK EXPERIENCE
                    </h3>
                    {"".join([f'''
                    <div style='margin-bottom: 20px; padding: 15px; background: #f8f9fa; border-radius: 8px; 
                                border-left: 4px solid {template_color};'>
                        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;'>
                            <h4 style='color: {template_color}; margin: 0; font-size: 18px;'>{exp.get('position', '')}</h4>
                            <span style='color: #666; font-size: 14px; font-style: italic;'>{exp.get('duration', '')}</span>
                        </div>
                        <p style='color: #555; margin: 5px 0 10px 0; font-size: 15px; font-weight: 500;'>
                            {exp.get('company', '')}
                        </p>
                        <div style='color: #444; line-height: 1.7; font-size: 14px;'>
                            {"".join([f"<p style='margin: 5px 0;'>• {line.strip()}</p>" for line in exp.get('description', '').split('\\n') if line.strip()])}
                        </div>
                    </div>
                    ''' for exp in data.get('experience', []) if exp.get('position')])}
                </div>
                ''' if data.get('experience') and any(exp.get('position') for exp in data.get('experience', [])) else ''}
                
                <!-- Education -->
                {f'''
                <div style='margin-bottom: 25px;'>
                    <h3 style='color: {template_color}; border-bottom: 3px solid {template_color}; 
                               padding-bottom: 8px; margin-bottom: 15px; font-size: 20px;'>
                        🎓 EDUCATION
                    </h3>
                    {"".join([f'''
                    <div style='margin-bottom: 15px; padding: 15px; background: #f8f9fa; border-radius: 8px;'>
                        <div style='display: flex; justify-content: space-between; align-items: center;'>
                            <div>
                                <h4 style='color: {template_color}; margin: 0 0 5px 0; font-size: 17px;'>{edu.get('degree', '')}</h4>
                                <p style='color: #555; margin: 0; font-size: 15px;'>{edu.get('institution', '')}</p>
                                {f"<p style='color: #666; margin: 5px 0 0 0; font-size: 14px;'>GPA: {edu.get('gpa')}</p>" if edu.get('gpa') else ''}
                            </div>
                            <span style='color: #666; font-size: 15px; font-weight: 500;'>{edu.get('year', '')}</span>
                        </div>
                    </div>
                    ''' for edu in data.get('education', []) if edu.get('degree')])}
                </div>
                ''' if data.get('education') and any(edu.get('degree') for edu in data.get('education', [])) else ''}
                
                <!-- Projects -->
                {f'''
                <div style='margin-bottom: 25px;'>
                    <h3 style='color: {template_color}; border-bottom: 3px solid {template_color}; 
                               padding-bottom: 8px; margin-bottom: 15px; font-size: 20px;'>
                        🚀 PROJECTS
                    </h3>
                    {"".join([f'''
                    <div style='margin-bottom: 15px; padding: 15px; background: #f8f9fa; border-radius: 8px;'>
                        <h4 style='color: {template_color}; margin: 0 0 8px 0; font-size: 17px;'>{proj.get('title', '')}</h4>
                        <p style='color: #444; margin: 0 0 8px 0; line-height: 1.6; font-size: 14px;'>{proj.get('description', '')}</p>
                        {f"<p style='color: #666; margin: 0; font-size: 13px; font-style: italic;'><strong>Technologies:</strong> {proj.get('technologies')}</p>" if proj.get('technologies') else ''}
                    </div>
                    ''' for proj in data.get('projects', []) if proj.get('title')])}
                </div>
                ''' if data.get('projects') and any(proj.get('title') for proj in data.get('projects', [])) else ''}
                
                <!-- Skills -->
                {f'''
                <div style='margin-bottom: 25px;'>
                    <h3 style='color: {template_color}; border-bottom: 3px solid {template_color}; 
                               padding-bottom: 8px; margin-bottom: 15px; font-size: 20px;'>
                        ⚡ SKILLS
                    </h3>
                    <div style='display: flex; flex-wrap: wrap; gap: 10px;'>
                        {"".join([f"<span style='background: {template_color}; color: white; padding: 8px 16px; border-radius: 20px; font-size: 14px; font-weight: 500;'>{skill.strip()}</span>" for skill in data.get('skills', '').replace('\\n', ',').split(',') if skill.strip()])}
                    </div>
                </div>
                ''' if data.get('skills') else ''}
                
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Display resume info
            st.subheader("📋 Resume Details")
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"**Name:** {st.session_state.user_data.get('name', 'N/A')}")
                st.info(f"**Email:** {st.session_state.user_data.get('email', 'N/A')}")
                st.info(f"**Phone:** {st.session_state.user_data.get('phone', 'N/A')}")
            with col2:
                st.info(f"**Template:** {st.session_state.selected_template}")
                st.info(f"**Experience Entries:** {len(st.session_state.user_data.get('experience', []))}")
                st.info(f"**Education Entries:** {len(st.session_state.user_data.get('education', []))}")
            
            st.markdown("---")
            
            # Options
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("📝 Edit Details", use_container_width=True):
                    st.session_state.page = 'input'
                    st.rerun()
            with col2:
                if st.button("🎨 Change Template", use_container_width=True):
                    st.session_state.page = 'template'
                    st.rerun()
            with col3:
                if st.button("🔄 Start New Resume", use_container_width=True):
                    st.session_state.user_data = {}
                    st.session_state.selected_template = None
                    st.session_state.page = 'input'
                    st.rerun()
            
            # Tips
            with st.expander("💡 Tips for an Outstanding Resume"):
                st.markdown("""
                ### Content Tips:
                - **Keep it concise**: Aim for 1-2 pages maximum
                - **Use action verbs**: Start bullet points with strong verbs (Led, Managed, Developed, Achieved)
                - **Quantify achievements**: Use numbers and percentages (Increased sales by 30%, Managed team of 10)
                - **Tailor for each job**: Customize your resume for each application
                - **Highlight key accomplishments**: Focus on results, not just responsibilities
                
                ### Formatting Tips:
                - **Consistent formatting**: Maintain uniform fonts, sizes, and spacing throughout
                - **White space**: Don't overcrowd - leave adequate white space for readability
                - **Professional font**: Stick with Arial, as used in these templates
                - **Bullet points**: Keep them concise (1-2 lines max per point)
                
                ### Technical Tips:
                - **Proofread carefully**: Check for spelling and grammar errors multiple times
                - **Update regularly**: Keep your resume current with latest achievements
                - **Include keywords**: Use industry-specific keywords for ATS (Applicant Tracking Systems)
                - **PDF format**: Always send as PDF to preserve formatting
                - **File naming**: Use "FirstName_LastName_Resume.pdf" format
                
                ### What to Avoid:
                - Personal pronouns (I, me, my)
                - Irrelevant personal information (age, photo, marital status)
                - Outdated or irrelevant experiences
                - Fancy fonts, colors, or graphics (unless applying for creative roles)
                - Lies or exaggerations
                """)
                
        except Exception as e:
            st.error(f"❌ Error generating resume: {str(e)}")
            st.info("💡 Please try a different template or check your input data.")
            
            with st.expander("🔍 Error Details (for debugging)"):
                st.code(str(e))
                st.write("**Possible solutions:**")
                st.write("- Try a different template")
                st.write("- Check if all text fields contain valid characters")
                st.write("- Ensure no special Unicode characters in your text")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p><strong>📄 Professional Resume Generator</strong> | Built with Streamlit & FPDF</p>
    <p style='font-size: 12px;'>Create stunning, ATS-friendly resumes in minutes!</p>
    <p style='font-size: 11px; color: #999;'>© 2025 | Version 1.0</p>
</div>
""", unsafe_allow_html=True)