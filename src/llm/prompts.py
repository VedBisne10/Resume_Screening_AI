def document_extraction_prompt(text):

    return f"""
You are an expert ATS (Applicant Tracking System) parser.

Analyze the following document and extract:
1. Technical Skills
2. Education
3. Experience
4. Certifications

IMPORTANT RULES:

- Extract ONLY actual technical skills, tools, technologies,
  programming languages, frameworks, libraries, databases,
  cloud platforms, and software.

- Do NOT include category names such as:
  Programming
  Libraries
  Frameworks
  Tools
  Technologies
  Skills

- Do NOT include soft skills such as:
  Communication
  Teamwork
  Leadership
  Problem Solving
  Time Management

- Return skills as individual items.

Bad Examples:
Programming
Libraries
Frameworks
Technical Skills
Analytical Skills
Problem Solving Skills

Return ONLY valid JSON.

Schema:

{{
    "skills": [],
    "education": [],
    "experience": [],
    "certifications": []
}}

Document:

{text}
"""
# Good Examples:
# Python
# SQL
# Docker
# AWS
# PyTorch
# TensorFlow
# FastAPI
# PostgreSQL
# Git
# Pandas