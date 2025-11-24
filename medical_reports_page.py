from flask import render_template_string
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from io import BytesIO
from datetime import datetime

def generate_urgence_pdf(patient_data, analyse_urgence):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=18, textColor=colors.HexColor('#1a237e'), alignment=TA_CENTER)
    heading_style = ParagraphStyle('CustomHeading', parent=styles['Heading2'], fontSize=14, textColor=colors.HexColor('#283593'))
    
    story = []
    
    # Header
    story.append(Paragraph("RAPPORT D'ANALYSE MÉDICALE D'URGENCE", title_style))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph(f"Date: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
    story.append(Spacer(1, 0.8*cm))
    
    # Patient Info
    story.append(Paragraph("INFORMATIONS PATIENT", heading_style))
    story.append(Spacer(1, 0.3*cm))
    patient_table = Table([
        ['Nom:', patient_data.get('name', 'N/A')],
        ['Âge:', str(patient_data.get('age', 'N/A'))],
        ['Sexe:', patient_data.get('sexe', 'N/A')],
        ['Niveau Urgence:', patient_data.get('niveau_urgence', 'N/A')],
        ['Condition:', patient_data.get('condition', 'N/A')]
    ], colWidths=[4*cm, 12*cm])
    patient_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e3f2fd')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
    ]))
    story.append(patient_table)
    story.append(Spacer(1, 0.8*cm))
    
    # Symptoms
    story.append(Paragraph("SYMPTÔMES", heading_style))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(patient_data.get('symptomes', 'N/A'), styles['Normal']))
    story.append(Spacer(1, 0.8*cm))
    
    # Medical Analysis
    story.append(Paragraph("ANALYSE MÉDICALE D'URGENCE", heading_style))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(f"<b>Médecin Urgentiste:</b> {analyse_urgence.get('medecin', 'Dr. Urgence')}", styles['Normal']))
    story.append(Spacer(1, 0.3*cm))
    
    # Diagnostic Différentiel
    medical_analysis = patient_data.get('hospital', {}).get('medical_analysis', {})
    if medical_analysis.get('diagnostic_differentiel'):
        story.append(Paragraph("<b>Diagnostic Différentiel:</b>", styles['Normal']))
        story.append(Spacer(1, 0.2*cm))
        for diag in medical_analysis['diagnostic_differentiel'][:3]:
            story.append(Paragraph(f"• {diag.get('pathologie', 'N/A')} - Probabilité: {diag.get('probabilite', 'N/A')}", styles['Normal']))
            story.append(Paragraph(f"  Arguments: {diag.get('arguments', 'N/A')}", styles['Normal']))
            story.append(Spacer(1, 0.2*cm))
    
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph(f"<b>Évaluation:</b> {analyse_urgence.get('diagnostic', 'En cours d\'évaluation')}", styles['Normal']))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(f"<b>Recommandations:</b> {analyse_urgence.get('recommandations', 'Surveillance continue')}", styles['Normal']))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

def generate_specialiste_pdf(patient_data, traitement_specialiste):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=18, textColor=colors.HexColor('#1a237e'), alignment=TA_CENTER)
    heading_style = ParagraphStyle('CustomHeading', parent=styles['Heading2'], fontSize=14, textColor=colors.HexColor('#283593'))
    
    story = []
    
    # Header
    story.append(Paragraph("RAPPORT DE TRAITEMENT SPÉCIALISÉ", title_style))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph(f"Date: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
    story.append(Spacer(1, 0.8*cm))
    
    # Patient Info
    story.append(Paragraph("INFORMATIONS PATIENT", heading_style))
    story.append(Spacer(1, 0.3*cm))
    patient_table = Table([
        ['Nom:', patient_data.get('name', 'N/A')],
        ['Âge:', str(patient_data.get('age', 'N/A'))],
        ['Sexe:', patient_data.get('sexe', 'N/A')]
    ], colWidths=[4*cm, 12*cm])
    patient_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e3f2fd')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
    ]))
    story.append(patient_table)
    story.append(Spacer(1, 0.8*cm))
    
    # Specialist Treatment
    story.append(Paragraph("TRAITEMENT SPÉCIALISÉ", heading_style))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(f"<b>Médecin Spécialiste:</b> {traitement_specialiste.get('specialiste_nom', 'N/A')}", styles['Normal']))
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph(f"<b>Spécialité:</b> {traitement_specialiste.get('specialiste_titre', 'N/A')}", styles['Normal']))
    story.append(Spacer(1, 0.5*cm))
    
    story.append(Paragraph(f"<b>Diagnostic Retenu:</b> {traitement_specialiste.get('diagnostic', 'En cours')}", styles['Normal']))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(f"<b>Plan de Traitement:</b> {traitement_specialiste.get('plan_traitement', 'À définir')}", styles['Normal']))
    story.append(Spacer(1, 0.5*cm))
    
    # Prescriptions détaillées
    medical_analysis = patient_data.get('hospital', {}).get('medical_analysis', {})
    if medical_analysis.get('prescriptions'):
        story.append(Paragraph("<b>PRESCRIPTIONS MÉDICAMENTEUSES:</b>", styles['Normal']))
        story.append(Spacer(1, 0.3*cm))
        for i, presc in enumerate(medical_analysis['prescriptions'][:5], 1):
            story.append(Paragraph(f"<b>{i}. {presc.get('medicament', 'N/A')}</b>", styles['Normal']))
            story.append(Paragraph(f"   Posologie: {presc.get('posologie', 'N/A')}", styles['Normal']))
            story.append(Paragraph(f"   Voie: {presc.get('voie', 'N/A')} - Durée: {presc.get('duree', 'N/A')}", styles['Normal']))
            story.append(Paragraph(f"   Surveillance: {presc.get('surveillance', 'N/A')}", styles['Normal']))
            story.append(Spacer(1, 0.3*cm))
    else:
        story.append(Paragraph(f"<b>Prescriptions:</b> {traitement_specialiste.get('prescriptions', 'Selon protocole établi')}", styles['Normal']))
    
    # Examens complémentaires
    if medical_analysis.get('examens_complementaires'):
        story.append(Spacer(1, 0.5*cm))
        story.append(Paragraph("<b>EXAMENS COMPLÉMENTAIRES:</b>", styles['Normal']))
        story.append(Spacer(1, 0.3*cm))
        for exam in medical_analysis['examens_complementaires'][:3]:
            story.append(Paragraph(f"• {exam.get('examen', 'N/A')} - Urgence: {exam.get('urgence', 'N/A')}", styles['Normal']))
            story.append(Spacer(1, 0.2*cm))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

def render_medical_reports(patients, user=None):
    html = '''
    <!doctype html>
    <html>
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width,initial-scale=1">
        <title>Medical Reports - MediAlert Pro</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
        <link rel="stylesheet" href="/static/css/main.css">
        <style>
          :root{--bg:#f6f7fb;--card:#ffffff;--muted:#6b7280;--accent:#6366f1}
          .wrap{max-width:1200px;margin:0 auto;padding:2rem}
          .page-header{color:white;margin-bottom:2rem}
          .page-header h1{font-size:2.5rem;margin-bottom:0.5rem}
          .page-header p{font-size:1.1rem;opacity:0.9}
          .patient-card{background:var(--card);border-radius:16px;padding:2rem;box-shadow:0 10px 40px rgba(15,23,42,0.08);margin-bottom:2rem}
          .patient-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:1.5rem;padding-bottom:1rem;border-bottom:2px solid #e2e8f0}
          .patient-name{font-size:1.5rem;font-weight:800;color:#0f172a}
          .reports-grid{display:grid;grid-template-columns:1fr 1fr;gap:1.5rem}
          .report-box{background:#f8fafc;padding:1.5rem;border-radius:12px;border:1px solid #e2e8f0;transition:transform 0.3s}
          .report-box:hover{transform:translateY(-5px)}
          .report-title{font-size:1.1rem;font-weight:700;color:var(--accent);margin-bottom:1rem}
          .doctor-info{margin-bottom:1rem;font-size:14px}
          .doctor-name{font-weight:700;color:#0f172a;font-size:1rem}
          .download-btn{display:inline-block;margin-top:1rem;padding:10px 20px;background:linear-gradient(90deg,var(--accent),#7c3aed);color:white;text-decoration:none;border-radius:8px;font-size:14px;font-weight:700;transition:transform 0.3s}
          .download-btn:hover{transform:translateY(-2px)}
          @media(max-width:768px){.reports-grid{grid-template-columns:1fr}}
        </style>
      </head>
      <body>
        <nav class="navbar">
          <div class="navbar-content">
            <a href="/" class="logo"><i class="fa-solid fa-book-medical"></i> MediAlert Pro</a>
            <ul class="nav-links">
              <li><a href="/"><i class="fas fa-home"></i> Dashboard</a></li>
              <li><a href="/alert"><i class="fas fa-plus-circle"></i> New Alert</a></li>
              <li><a href="/patient_info"><i class="fas fa-users"></i> Patients</a></li>
              <li><a href="/medical_reports"><i class="fas fa-file-medical"></i> Reports</a></li>
              {% if user and user.get('role') == 'admin' %}
              <li><a href="/admin"><i class="fas fa-cog"></i> Admin</a></li>
              {% endif %}
              <li><a href="/profile"><i class="fas fa-user"></i> Profile</a></li>
              <li><a href="/logout" style="color: #ef4444;"><i class="fas fa-sign-out-alt"></i> Logout</a></li>
            </ul>
          </div>
        </nav>
        <div class="wrap">
          <div class="page-header">
            <h1><i class="fa-solid fa-file-medical"></i> Medical Reports</h1>
            <p>Comprehensive medical documentation and treatment records</p>
          </div>

          {% for patient in patients %}
          <div class="patient-card">
            <div class="patient-header">
              <div class="patient-name">{{ patient.get('name', 'N/A') }}</div>
              <div style="color:var(--muted);font-size:14px">ID: #{{ patient.get('id', loop.index) }}</div>
            </div>
            
            <div class="reports-grid">
              <div class="report-box">
                <div class="report-title"><i class="fa-solid fa-truck-medical"></i> Analyse d'Urgence</div>
                <div class="doctor-info">
                  <div class="doctor-name"><i class="fa-solid fa-user-doctor"></i> {{ patient.get('hospital', {}).get('urgentiste', 'Dr. Urgence') }}</div>
                  <div style="color:var(--muted);font-size:13px"><i class="fa-solid fa-stethoscope"></i> Médecine d'urgence</div>
                </div>
                <div style="font-size:13px;color:var(--muted);margin-bottom:12px">
                  <i class="fa-solid fa-clipboard-check"></i> Évaluation initiale et diagnostic différentiel
                </div>
                <a class="download-btn" href="/download_report/{{ patient.get('id', loop.index) }}/urgence"><i class="fa-solid fa-download"></i> Télécharger PDF</a>
              </div>
              
              <div class="report-box">
                <div class="report-title"><i class="fa-solid fa-user-doctor"></i> Traitement Spécialisé</div>
                <div class="doctor-info">
                  <div class="doctor-name"><i class="fa-solid fa-user-md"></i> {{ patient.get('hospital', {}).get('specialiste', {}).get('nom', 'N/A') }}</div>
                  <div style="color:var(--muted);font-size:13px"><i class="fa-solid fa-briefcase-medical"></i> {{ patient.get('hospital', {}).get('specialiste', {}).get('specialite', 'Spécialiste') }}</div>
                </div>
                <div style="font-size:13px;color:var(--muted);margin-bottom:12px">
                  <i class="fa-solid fa-prescription"></i> Plan de traitement et prescriptions
                </div>
                <a class="download-btn" href="/download_report/{{ patient.get('id', loop.index) }}/specialiste"><i class="fa-solid fa-download"></i> Télécharger PDF</a>
              </div>
            </div>
          </div>
          {% endfor %}
        </div>
      </body>
    </html>
    '''
    return render_template_string(html, patients=patients, user=user)
