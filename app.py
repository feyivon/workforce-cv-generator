import streamlit as st
import anthropic
from fpdf import FPDF
import os
import tempfile
from dotenv import load_dotenv

_ = load_dotenv()

client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])



# AI FUNCTIONS
def generate_cv(name, email, phone, location, summary, experience, education, skills):
    prompt = f"""
You are a professional CV writer with 10 years of experience.
Create a clean, professional CV for the following person.
Format it clearly with proper sections and bullet points.
Make it compelling and suitable for job applications in Africa and Internationally.

PERSONAL DETAILS:
Full Name: {name}
Email: {email}
Phone: {phone}
Location: {location}

PROFESSIONAL SUMMARY:
{summary}

WORK EXPERIENCE:
{experience}

EDUCATION:
{education}

SKILLS:
{skills}

Please write a complete, professional CV now.
Use clear section headers like: PROFESSIONAL SUMMARY, WORK EXPERIENCE, EDUCATION, SKILLS.
Make the language strong, active, and professional.
Do NOT include any preamble like "Here is your CV". Just output the CV directly.
"""
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text


def generate_cover_letter(name, email, phone, location, job_title, company_name, job_description, experience, skills, extra_note):
    prompt = f"""
You are a professional cover letter writer with 10 years of experience.
Write a compelling, personalized cover letter for this job application.
It should be warm, confident, and tailored to the role.
Suitable for jobs in Africa and Internationally.

APPLICANT DETAILS:
Full Name: {name}
Email: {email}
Phone: {phone}
Location: {location}

JOB DETAILS:
Job Title: {job_title}
Company Name: {company_name}
Job Description / Requirements: {job_description}

APPLICANT BACKGROUND:
Work Experience: {experience}
Skills: {skills}
Additional Notes: {extra_note}

Write a complete, professional cover letter now.
Use a proper letter format with greeting, 3-4 strong paragraphs, and a closing.
Do NOT include any preamble. Just output the cover letter directly.
"""
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text


# PDF GENERATION
def create_pdf(text, filename="document.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_margins(20, 20, 20)
    pdf.set_auto_page_break(auto=True, margin=20)

    lines = text.split("\n")

    for line in lines:
        line = line.strip()
        if not line:
            pdf.ln(3)
            continue

        # Detect section headers (all caps lines)
        if line.isupper() and len(line) > 3:
            pdf.set_font("Helvetica", style="B", size=12)
            pdf.set_text_color(30, 30, 120)
            pdf.ln(2)
            pdf.cell(0, 8, line, ln=True)
            pdf.set_draw_color(30, 30, 120)
            pdf.line(20, pdf.get_y(), 190, pdf.get_y())
            pdf.ln(2)
            pdf.set_text_color(0, 0, 0)
        elif line.startswith("-") or line.startswith("•"):
            pdf.set_font("Helvetica", size=10)
            pdf.set_x(25)
            # Replace bullet characters for FPDF compatibility
            clean_line = line.lstrip("-•").strip()
            pdf.cell(5, 6, "-", ln=False)
            pdf.multi_cell(0, 6, clean_line)
        else:
            pdf.set_font("Helvetica", size=10)
            pdf.multi_cell(0, 6, line)

    # Save to temp file
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(tmp.name)
    return tmp.name



# PAGE CONFIG & STYLES
st.set_page_config(
    page_title="WORK-FORCE CV Generator",
    page_icon="📄",
    layout="centered"
)

st.markdown("""
<style>
    .main { background-color: #f8f9fc; }
    h1 { color: #1e1e7e; }
    .stButton > button {
        background-color: #1e1e7e;
        color: white;
        border-radius: 8px;
        font-weight: bold;
        padding: 0.6em 1.2em;
    }
    .stButton > button:hover {
        background-color: #2e2ea0;
        color: white;
    }
    .cv-preview {
        background: white;
        border: 1px solid #dde;
        border-radius: 10px;
        padding: 2rem;
        font-family: 'Georgia', serif;
        font-size: 14px;
        line-height: 1.7;
        white-space: pre-wrap;
        color: #1a1a2e;
        box-shadow: 0 2px 8px rgba(0,0,0,0.07);
    }
    .section-label {
        font-size: 13px;
        font-weight: 600;
        color: #555;
        margin-bottom: 4px;
    }
</style>
""", unsafe_allow_html=True)



# HEADER
st.markdown("# 📄 WORK-FORCE")
st.markdown("#### AI-Powered CV & Cover Letter Generator")
st.markdown("Fill in your details and **Claude AI** will write professional documents in seconds.")
st.divider()


# TABS
tab1, tab2 = st.tabs(["📋 CV Generator", "✉️ Cover Letter Generator"])

# TAB 1 — CV GENERATOR
with tab1:
    st.subheader("👤 Personal Information")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name", placeholder="e.g. Chidi Okeke", key="cv_name")
        email = st.text_input("Email Address", placeholder="e.g. chidi@gmail.com", key="cv_email")
    with col2:
        phone = st.text_input("Phone Number", placeholder="e.g. +234 801 234 5678", key="cv_phone")
        location = st.text_input("City, Country", placeholder="e.g. Lagos, Nigeria", key="cv_location")

    st.divider()
    st.subheader("💼 Professional Summary")
    summary = st.text_area(
        "Write 2-3 sentences about yourself and your career goals",
        placeholder="e.g. Passionate software developer with 2 years of experience...",
        height=100, key="cv_summary"
    )

    st.divider()
    st.subheader("🏢 Work Experience")
    experience = st.text_area(
        "List your jobs — company name, role, dates and what you did",
        placeholder="e.g.\n\nSoftware Developer - TechCorp Nigeria (2022 - Present)\n- Built and maintained company website\n- Reduced page load time by 40%",
        height=180, key="cv_experience"
    )

    st.divider()
    st.subheader("🎓 Education")
    education = st.text_area(
        "List your schools, degrees and graduation years",
        placeholder="e.g.\n\nB.Sc Computer Science - University of Lagos (2019 - 2023)\n- Graduated with Second Class Upper",
        height=140, key="cv_education"
    )

    st.divider()
    st.subheader("⚡ Skills")
    skills = st.text_input(
        "List your key skills separated by commas",
        placeholder="e.g. Python, Microsoft Excel, Customer Service, Team Leadership",
        key="cv_skills"
    )

    st.divider()

    if st.button("🚀 Generate My CV", type="primary", use_container_width=True, key="gen_cv"):
        if not name or not email or not experience:
            st.warning("⚠️ Please fill in at least your Name, Email and Work Experience.")
        else:
            with st.spinner("✨ Claude is writing your CV... please wait"):
                cv_text = generate_cv(name, email, phone, location, summary, experience, education, skills)
            st.success("✅ Your CV is ready!")
            st.session_state["cv_text"] = cv_text

    if "cv_text" in st.session_state:
        st.divider()
        st.subheader("📋 Your Generated CV")
        st.markdown(f'<div class="cv-preview">{st.session_state["cv_text"]}</div>', unsafe_allow_html=True)

        st.divider()

        # PDF Download
        pdf_path = create_pdf(st.session_state["cv_text"])
        with open(pdf_path, "rb") as f:
            st.download_button(
                label="⬇️ Download CV as PDF",
                data=f,
                file_name=f"{name.replace(' ', '_')}_CV.pdf" if name else "CV.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        os.unlink(pdf_path)


# TAB 2 — COVER LETTER GENERATOR
with tab2:
    st.subheader("👤 Your Details")
    col1, col2 = st.columns(2)
    with col1:
        cl_name = st.text_input("Full Name", placeholder="e.g. Chidi Okeke", key="cl_name")
        cl_email = st.text_input("Email Address", placeholder="e.g. chidi@gmail.com", key="cl_email")
    with col2:
        cl_phone = st.text_input("Phone Number", placeholder="e.g. +234 801 234 5678", key="cl_phone")
        cl_location = st.text_input("City, Country", placeholder="e.g. Lagos, Nigeria", key="cl_location")

    st.divider()
    st.subheader("🏢 Job Details")
    col3, col4 = st.columns(2)
    with col3:
        job_title = st.text_input("Job Title You're Applying For", placeholder="e.g. Marketing Manager")
    with col4:
        company_name = st.text_input("Company Name", placeholder="e.g. Flutterwave")

    job_description = st.text_area(
        "Paste the job description or key requirements",
        placeholder="e.g. We're looking for a results-driven marketer with 3+ years experience...",
        height=130
    )

    st.divider()
    st.subheader("💼 Your Background")
    cl_experience = st.text_area(
        "Briefly describe your relevant experience",
        placeholder="e.g. 3 years in digital marketing at two Lagos startups, managed campaigns reaching 500k+ users",
        height=100, key="cl_experience"
    )
    cl_skills = st.text_input(
        "Your relevant skills",
        placeholder="e.g. SEO, Google Ads, Content Strategy, Team Leadership",
        key="cl_skills"
    )
    extra_note = st.text_area(
        "Anything extra you want mentioned? (optional)",
        placeholder="e.g. I'm especially excited about this role because...",
        height=80
    )

    st.divider()

    if st.button("✉️ Generate Cover Letter", type="primary", use_container_width=True, key="gen_cl"):
        if not cl_name or not job_title or not company_name:
            st.warning("⚠️ Please fill in your Name, Job Title and Company Name.")
        else:
            with st.spinner("✨ Claude is writing your cover letter... please wait"):
                cl_text = generate_cover_letter(
                    cl_name, cl_email, cl_phone, cl_location,
                    job_title, company_name, job_description,
                    cl_experience, cl_skills, extra_note
                )
            st.success("✅ Your Cover Letter is ready!")
            st.session_state["cl_text"] = cl_text

    if "cl_text" in st.session_state:
        st.divider()
        st.subheader("✉️ Your Generated Cover Letter")
        st.markdown(f'<div class="cv-preview">{st.session_state["cl_text"]}</div>', unsafe_allow_html=True)

        st.divider()

        # PDF Download
        pdf_path = create_pdf(st.session_state["cl_text"])
        with open(pdf_path, "rb") as f:
            cl_name_val = st.session_state.get("cl_name", "Cover_Letter")
            st.download_button(
                label="⬇️ Download Cover Letter as PDF",
                data=f,
                file_name=f"{cl_name_val.replace(' ', '_')}_Cover_Letter.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        os.unlink(pdf_path)



# FOOTER
st.divider()
st.markdown(
    "<p style='text-align:center; color:#aaa; font-size:13px;'>WORK-FORCE © 2025 · Powered by Claude AI</p>",
    unsafe_allow_html=True
)