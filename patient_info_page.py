from flask import render_template_string

def render_patient_info(patients):
    html = '''
    <!doctype html>
    <html>
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width,initial-scale=1">
        <title>Patient Details</title>
        <style>
          :root{--bg:#f6f7fb;--card:#ffffff;--muted:#6b7280;--accent:#6366f1}
          body{font-family:Inter,Segoe UI,Roboto,Arial,sans-serif;background:linear-gradient(180deg,#eef2ff,white);padding:28px}
          .wrap{max-width:980px;margin:0 auto;display:grid;grid-template-columns:1fr;gap:18px}
          .header{display:flex;align-items:center;gap:14px}
          .title{font-size:20px;font-weight:800;color:#0f172a}
          .subtitle{color:var(--muted);font-size:13px}
          .patient-card{background:var(--card);border-radius:12px;padding:18px;box-shadow:0 8px 30px rgba(15,23,42,0.06);display:grid;grid-template-columns:1fr 320px;gap:18px}
          .left{display:flex;flex-direction:column;gap:10px}
          .row{display:flex;gap:12px;align-items:center}
          .pill{background:#f3f4ff;color:var(--accent);padding:6px 10px;border-radius:999px;font-weight:800}
          .label{font-size:12px;color:var(--muted);font-weight:700;text-transform:uppercase}
          .value{font-size:16px;font-weight:800;color:#0f172a}
          .muted{color:var(--muted);font-size:13px}
          .right{background:#fbfbff;padding:12px;border-radius:10px}
          .section{margin-top:8px}
          .info-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}
          .info-box{background:white;border-radius:8px;padding:10px;border:1px solid #eef2ff}
          .info-box .k{font-size:12px;color:var(--muted);font-weight:700}
          .info-box .v{font-size:15px;font-weight:800;color:#0f172a;margin-top:6px}
          a.button{display:inline-block;margin-top:12px;padding:10px 14px;background:linear-gradient(90deg,var(--accent),#7c3aed);color:white;border-radius:8px;text-decoration:none;font-weight:800}
          @media(max-width:880px){.patient-card{grid-template-columns:1fr} .right{order:2}}
        </style>
      </head>
      <body>
        <div class="wrap">
          <div class="header">
            <div class="title">Informations du Patient</div>
            <div class="subtitle">Détails patient, ambulance assignée et hôpital destinataire</div>
          </div>

          {% for patient in patients %}
          <div class="patient-card">
            <div class="left">
              <div style="display:flex;justify-content:space-between;align-items:center">
                <div>
                  <div class="pill">ID #{{ patient.id }}</div>
                  <h2 style="margin-top:10px;margin-bottom:6px">{{ patient.name }}</h2>
                  <div class="muted">{{ patient.localisation or 'Localisation non fournie' }}</div>
                </div>
                <div style="text-align:right">
                  <div class="label">Sexe</div>
                  <div class="value">{{ patient.sexe or 'N/A' }}</div>
                </div>
              </div>

              <div class="section">
                <div class="label">Symptômes</div>
                <div class="value" style="font-weight:600">{{ patient.symptomes or 'N/A' }}</div>
              </div>

              <div class="section info-grid">
                <div class="info-box">
                  <div class="k">Âge</div>
                  <div class="v">{{ patient.age or 'N/A' }}</div>
                </div>
                <div class="info-box">
                  <div class="k">Condition</div>
                  <div class="v">{{ patient.condition or 'N/A' }}</div>
                </div>
              </div>
            </div>

            <div class="right">
              <div style="display:flex;justify-content:space-between;align-items:center">
                <div class="label">Informations de transport</div>
              </div>

              <div style="display:flex;gap:10px;margin-top:8px;flex-direction:column">
                <div style="background:white;padding:12px;border-radius:8px;border:1px solid #eef2ff">
                  <div class="label" style="margin-bottom:8px">🚑 Ambulance assignée</div>
                  {% if patient.ambulance %}
                    <div class="info-grid">
                      <div>
                        <div class="k">Véhicule</div>
                        <div class="v">{{ patient.ambulance.id }}</div>
                      </div>
                      <div>
                        <div class="k">Chauffeur</div>
                        <div class="v">{{ patient.ambulance.driver }}</div>
                      </div>
                    </div>
                    <div style="margin-top:8px">
                      <div class="k">ETA</div>
                      <div class="v">{{ patient.ambulance.eta }}</div>
                    </div>
                    {% if patient.ambulance.localisation %}
                    <div style="margin-top:8px">
                      <div class="k">Localisation ambulance</div>
                      <div class="muted">{{ patient.ambulance.localisation }}</div>
                    </div>
                    {% endif %}
                  {% else %}
                    <div class="muted">Aucune ambulance assignée</div>
                  {% endif %}
                </div>

                <div style="background:white;padding:12px;border-radius:8px;border:1px solid #eef2ff">
                  <div class="label" style="margin-bottom:8px">🏥 Hôpital destinataire</div>
                  {% if patient.hospital %}
                    <div class="k">Nom</div>
                    <div class="v">{{ patient.hospital.name }}</div>
                    <div class="muted" style="margin-top:6px">{{ patient.hospital.address }}</div>
                    <div style="margin-top:8px"><span class="label">Statut:</span> <strong>{{ patient.hospital.acceptance_status }}</strong></div>
                  {% else %}
                    <div class="muted">Aucun hôpital assigné</div>
                  {% endif %}
                </div>
              </div>

              <a class="button" href="/">← Retour</a>
            </div>
          </div>
          {% endfor %}
        </div>
      </body>
    </html>
    '''
    return render_template_string(html, patients=patients)
