from flask import render_template_string

def render_patient_info(patients, user=None):
    html = '''
    <!doctype html>
    <html>
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width,initial-scale=1">
        <title>Patient Details - MediAlert Pro</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
        <link rel="stylesheet" href="/static/css/main.css">
        <style>
          :root{--bg:#f6f7fb;--card:#ffffff;--muted:#6b7280;--accent:#6366f1}
          .wrap{max-width:1200px;margin:0 auto;padding:2rem}
          .page-header{color:white;margin-bottom:2rem}
          .page-header h1{font-size:2.5rem;margin-bottom:0.5rem}
          .page-header p{font-size:1.1rem;opacity:0.9}
          .patient-card{background:var(--card);border-radius:16px;padding:2rem;box-shadow:0 10px 40px rgba(15,23,42,0.08);display:grid;grid-template-columns:1fr 380px;gap:2rem;margin-bottom:2rem}
          .left{display:flex;flex-direction:column;gap:1rem}
          .pill{background:#f3f4ff;color:var(--accent);padding:8px 16px;border-radius:999px;font-weight:800;display:inline-block;width:fit-content}
          .label{font-size:12px;color:var(--muted);font-weight:700;text-transform:uppercase}
          .value{font-size:16px;font-weight:800;color:#0f172a}
          .muted{color:var(--muted);font-size:14px}
          .right{background:#f8fafc;padding:1.5rem;border-radius:12px}
          .section{margin-top:1rem}
          .info-grid{display:grid;grid-template-columns:1fr 1fr;gap:1rem}
          .info-box{background:white;border-radius:10px;padding:1rem;border:1px solid #e2e8f0}
          .info-box .k{font-size:12px;color:var(--muted);font-weight:700}
          .info-box .v{font-size:15px;font-weight:800;color:#0f172a;margin-top:6px}
          a.button{display:inline-block;margin-top:12px;padding:12px 18px;background:linear-gradient(90deg,var(--accent),#7c3aed);color:white;border-radius:10px;text-decoration:none;font-weight:700;transition:transform 0.3s}
          a.button:hover{transform:translateY(-2px)}
          @media(max-width:880px){.patient-card{grid-template-columns:1fr} .right{order:2}}
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
            <h1><i class="fas fa-users"></i> Patient Information</h1>
            <p>Detailed patient records, ambulance assignments, and hospital destinations</p>
          </div>

          {% if not patients %}
          <div style="text-align:center;padding:4rem;background:white;border-radius:16px">
            <i class="fas fa-inbox" style="font-size:4rem;color:#cbd5e1;margin-bottom:1rem"></i>
            <h2 style="color:#64748b">No Patients Yet</h2>
            <p style="color:#94a3b8">Create an emergency alert to see patient information here</p>
            <a href="/alert" class="button" style="margin-top:1rem">Create Alert</a>
          </div>
          {% endif %}

          {% for patient in patients %}
          <div class="patient-card">
            <div class="left">
              <div style="display:flex;justify-content:space-between;align-items:center">
                <div>
                  <div class="pill">ID #{{ loop.index }}</div>
                  <h2 style="margin-top:10px;margin-bottom:6px">{{ patient.get('name', 'N/A') }}</h2>
                  <div class="muted">{{ patient.get('localisation', 'Localisation non fournie') }}</div>
                </div>
                <div style="text-align:right">
                  <div class="label">Sexe</div>
                  <div class="value">{{ patient.get('sexe', 'N/A') }}</div>
                </div>
              </div>

              <div class="section">
                <div class="label">Symptômes</div>
                <div class="value" style="font-weight:600">{{ patient.get('symptomes', 'N/A') }}</div>
              </div>

              <div class="section info-grid">
                <div class="info-box">
                  <div class="k">Âge</div>
                  <div class="v">{{ patient.get('age', 'N/A') }}</div>
                </div>
                <div class="info-box">
                  <div class="k">Condition</div>
                  <div class="v">{{ patient.get('condition', 'N/A') }}</div>
                </div>
              </div>
            </div>

            <div class="right">
              <div style="display:flex;justify-content:space-between;align-items:center">
                <div class="label">Informations de transport</div>
              </div>

              <div style="display:flex;gap:10px;margin-top:8px;flex-direction:column">
                <div style="background:white;padding:12px;border-radius:8px;border:1px solid #eef2ff">
                  <div class="label" style="margin-bottom:8px"><i class="fa-solid fa-truck-medical"></i> Ambulance assignée</div>
                  {% if patient.get('ambulance') %}
                    <div class="info-grid">
                      <div>
                        <div class="k">ID Véhicule</div>
                        <div class="v">{{ patient.ambulance.get('id', 'N/A') }}</div>
                      </div>
                      <div>
                        <div class="k">Type</div>
                        <div class="v">{{ patient.ambulance.get('type', 'Ambulance') }}</div>
                      </div>
                    </div>
                    <div style="margin-top:8px">
                      <div class="k">Nom</div>
                      <div class="v">{{ patient.ambulance.get('nom', 'Équipe disponible') }}</div>
                    </div>
                    <div class="info-grid" style="margin-top:8px">
                      <div>
                        <div class="k">Distance</div>
                        <div class="v">{{ patient.ambulance.get('distance_km', 0) }} km</div>
                      </div>
                      <div>
                        <div class="k">ETA</div>
                        <div class="v">{{ patient.ambulance.get('eta', 'N/A') }}</div>
                      </div>
                    </div>
                  {% else %}
                    <div class="muted">Aucune ambulance assignée</div>
                  {% endif %}
                </div>

                <div style="background:white;padding:12px;border-radius:8px;border:1px solid #eef2ff">
                  <div class="label" style="margin-bottom:8px"><i class="fa-solid fa-hospital"></i> Hôpital destinataire</div>
                  {% if patient.get('hospital') %}
                    <div class="info-grid">
                      <div>
                        <div class="k">ID Hôpital</div>
                        <div class="v">{{ patient.hospital.get('id', 'N/A') }}</div>
                      </div>
                      <div>
                        <div class="k">Distance</div>
                        <div class="v">{{ patient.hospital.get('distance_km', 0) }} km</div>
                      </div>
                    </div>
                    <div style="margin-top:8px">
                      <div class="k">Nom</div>
                      <div class="v">{{ patient.hospital.get('name', 'N/A') }}</div>
                    </div>
                    <div class="muted" style="margin-top:6px">{{ patient.hospital.get('address', 'N/A') }}</div>
                    <div style="margin-top:8px">
                      <div class="k">Service</div>
                      <div class="v">{{ patient.hospital.get('service', 'Urgences') }}</div>
                    </div>
                    <div class="info-grid" style="margin-top:8px">
                      <div>
                        <div class="k">ETA Hôpital</div>
                        <div class="v">{{ patient.hospital.get('eta', 'N/A') }}</div>
                      </div>
                      <div>
                        <div class="k">Statut</div>
                        <div class="v">{{ patient.hospital.get('acceptance_status', 'En attente') }}</div>
                      </div>
                    </div>
                    <div style="margin-top:12px;padding-top:12px;border-top:1px solid #eef2ff">
                      <div class="label" style="margin-bottom:6px"><i class="fa-solid fa-user-doctor"></i> Équipe médicale</div>
                      <div style="margin-top:6px">
                        <div class="k">Urgentiste</div>
                        <div class="v">{{ patient.hospital.get('urgentiste', 'N/A') }}</div>
                      </div>
                      {% if patient.hospital.get('specialiste') and patient.hospital.specialiste.get('nom') != 'N/A' %}
                      <div style="margin-top:6px">
                        <div class="k">Spécialiste</div>
                        <div class="v">{{ patient.hospital.specialiste.get('nom', 'N/A') }}</div>
                        <div class="muted" style="font-size:12px">{{ patient.hospital.specialiste.get('specialite', 'N/A') }}</div>
                      </div>
                      {% endif %}
                    </div>
                  {% else %}
                    <div class="muted">Aucun hôpital assigné</div>
                  {% endif %}
                </div>
              </div>

              <div style="display:flex;gap:10px">
                <a class="button" href="/" style="flex:1">← Retour</a>
                <a class="button" href="/medical_reports" style="flex:1;background:linear-gradient(90deg,#10b981,#059669)"><i class="fa-solid fa-chart-bar"></i> Rapports</a>
              </div>
            </div>
          </div>
          {% endfor %}
        </div>
      </body>
    </html>
    '''
    return render_template_string(html, patients=patients, user=user)
