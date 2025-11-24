import sys, os
import json
import re
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
from flask import Flask, request, jsonify, render_template_string, send_file
from patient_info_page import render_patient_info
from medical_reports_page import render_medical_reports, generate_urgence_pdf, generate_specialiste_pdf
from systeme_urgences_medicales.crew import SystemeUrgencesMedicalesCrew

app = Flask(__name__)
patients = []

INDEX_HTML = """
<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Medical Emergency Alert System</title>
    <style>
      * { margin: 0; padding: 0; box-sizing: border-box; }
      body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 20px;
      }
      .container {
        max-width: 500px;
        width: 100%;
      }
      .card {
        background: white;
        border-radius: 12px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        padding: 40px;
      }
      h1 {
        color: #333;
        margin-bottom: 10px;
        font-size: 28px;
      }
      .subtitle {
        color: #888;
        margin-bottom: 30px;
        font-size: 14px;
      }
      .form-group {
        margin-bottom: 20px;
      }
      label {
        display: block;
        color: #555;
        font-weight: 600;
        margin-bottom: 8px;
        font-size: 14px;
      }
      input, textarea, select {
        width: 100%;
        padding: 12px;
        border: 2px solid #e0e0e0;
        border-radius: 8px;
        font-size: 14px;
        font-family: inherit;
        transition: border-color 0.3s;
      }
      input:focus, textarea:focus, select:focus {
        outline: none;
        border-color: #667eea;
      }
      button {
        width: 100%;
        padding: 14px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-size: 16px;
        font-weight: 600;
        cursor: pointer;
        transition: transform 0.2s, box-shadow 0.2s;
        margin-top: 10px;
      }
      button:hover:not(:disabled) {
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
      }
      button:disabled {
        opacity: 0.6;
        cursor: not-allowed;
      }
      .response-card {
        margin-top: 30px;
        padding: 20px;
        border-radius: 8px;
        display: none;
        animation: slideIn 0.3s ease-out;
      }
      .response-card.show {
        display: block;
      }
      .response-card.error {
        background: #ffebee;
        border-left: 5px solid #f44336;
      }
      .response-title {
        font-weight: 600;
        margin-bottom: 10px;
        font-size: 16px;
      }
      .response-card.error .response-title {
        color: #c62828;
      }
      .response-text {
        font-size: 14px;
        line-height: 1.6;
        color: #333;
        word-wrap: break-word;
      }
      .response-card.error .response-text {
        color: #b71c1c;
      }
      @keyframes slideIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
      }
    </style>
  </head>
  <body>
    <div class="container">
      <div class="card">
        <h1>Medical Alert</h1>
        <p class="subtitle">Emergency Medical Dispatch System</p>
        
        <form id="alertForm" onsubmit="return false;">
          <div class="form-group">
            <label for="symptomes">Symptoms *</label>
            <textarea id="symptomes" name="symptomes" placeholder="Describe patient symptoms..." required rows="3"></textarea>
          </div>
          
          <div class="form-group">
            <label for="localisation">Location *</label>
            <input type="text" id="localisation" name="localisation" placeholder="Patient location address..." required />
          </div>
          
          <div class="form-group">
            <label for="nom_prenom">Patient Name (Optional)</label>
            <input type="text" id="nom_prenom" name="nom_prenom" placeholder="Full name" />
          </div>
          
          <div class="form-group">
            <label for="age">Age (Optional)</label>
            <input type="number" id="age" name="age" placeholder="Years" />
          </div>

          <div class="form-group">
            <label for="sexe">Gender (Optional)</label>
            <select id="sexe" name="sexe">
              <option value="">Select...</option>
              <option value="M">Male</option>
              <option value="F">Female</option>
              <option value="Other">Other</option>
            </select>
          </div>
          
          <button type="button" id="submitBtn">Send Alert</button>
        </form>
        
        <div id="responseCard" class="response-card">
          <div class="response-title" id="responseTitle"></div>
          <div class="response-text" id="responseText"></div>
        </div>
      </div>
    </div>
    
    <script>
      const submitBtn = document.getElementById('submitBtn');
      const responseCard = document.getElementById('responseCard');
      const responseTitle = document.getElementById('responseTitle');
      const responseText = document.getElementById('responseText');
      
      submitBtn.addEventListener('click', async (e) => {
        e.preventDefault();
        
        const form = document.getElementById('alertForm');
        if (!form.checkValidity()) {
          form.reportValidity();
          return;
        }
        
        responseCard.className = 'response-card show';
        responseTitle.textContent = '⏳ Processing...';
        responseText.textContent = 'Sending alert to medical system...';
        submitBtn.disabled = true;
        
        const fd = new FormData(form);
        const body = Object.fromEntries(fd.entries());
        
        try {
          const res = await fetch('/api/alert', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
          });
          
          const data = await res.json();
          
          if (data.status === 'ok') {
            window.location.href = '/patient_info';
          } else {
            responseCard.className = 'response-card show error';
            responseTitle.textContent = '✕ Error';
            responseText.textContent = data.message || 'Failed to send alert.';
          }
        } catch (err) {
          responseCard.className = 'response-card show error';
          responseTitle.textContent = '✕ Connection Error';
          responseText.textContent = 'Server connection failed: ' + err.message;
        } finally {
          submitBtn.disabled = false;
        }
      });
    </script>
  </body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(INDEX_HTML)

@app.route('/api/alert', methods=['POST'])
def alert_api():
    payload = request.get_json() or {}
    
    # 1. Prepare Inputs
    inputs = {
        'symptomes': payload.get('symptomes', ''),
        'localisation': payload.get('localisation', ''),
        'nom_prenom': payload.get('nom_prenom', 'Inconnu'),
        'age': payload.get('age', '30'),
        'sexe': payload.get('sexe', 'Non spécifié'),
        'nv_urgence': payload.get('nv_urgence', 'Non évalué'),
        'localisation_ambulance': 'Centre Ville',
        'localisation_patient': payload.get('localisation', '')
    }

    try:
      # 2. Run Crew
      crew = SystemeUrgencesMedicalesCrew().crew()
      result = crew.kickoff(inputs=inputs)
      
      # 3. Extract JSON from Crew Output
      final_output_str = str(result)
      
      print("\n=== DEBUG: CREW OUTPUT ===")
      print(f"Result text (first 500 chars): {final_output_str[:500]}")
      
      data = {}
      try:
          # Clean up markdown code blocks if present
          json_match = re.search(r'\{.*\}', final_output_str, re.DOTALL)
          if json_match:
              data = json.loads(json_match.group(0))
              print(f"Parsed JSON keys: {data.keys()}")
          else:
              print("DEBUG: Could not find JSON brackets, attempting raw load")
              data = json.loads(final_output_str)
      except Exception as e:
          print(f"JSON Parsing Error: {e}")
          print(f"Raw Output: {final_output_str}")

      # 4. Map Data to Patient Info Page Structure
      p_data = data.get('patient', {})
      a_data = data.get('ambulance', {})
      h_data = data.get('hopital', {})
      h_team = h_data.get('equipe', {})

      # Generate a new ID
      new_id = len(patients) + 1

      patient_entry = {
        'id': new_id,
        'name': p_data.get('nom', inputs.get('nom_prenom')),
        'age': p_data.get('age', inputs.get('age')),
        'sexe': p_data.get('sexe', inputs.get('sexe')),
        'symptomes': p_data.get('symptomes', inputs.get('symptomes')),
        'localisation': inputs.get('localisation'),
        'condition': p_data.get('condition', 'En cours d\'évaluation'),
        'niveau_urgence': p_data.get('niveau_urgence', 'URGENT'),
        
        'ambulance': {
            'id': a_data.get('id', 'N/A'),
            'nom': a_data.get('nom', 'Recherche en cours...'),
            'type': a_data.get('type', 'Ambulance'),
            'eta': f"{a_data.get('eta_minutes', 'Unknown')} min",
            'distance_km': a_data.get('distance_km', 0)
        },
        
        'hospital': {
            'id': h_data.get('id', 'N/A'),
            'name': h_data.get('nom', 'Hôpital le plus proche'),
            'address': h_data.get('adresse', 'Adresse non fournie'),
            'service': h_data.get('service', 'Urgences'),
            'distance_km': h_data.get('distance_km', 0),
            'eta': f"{h_data.get('eta_minutes', 'Unknown')} min",
            'acceptance_status': h_data.get('statut_acceptance', 'En attente'),
            'urgentiste': h_team.get('urgentiste', 'De garde'),
            'specialiste': {
                'nom': h_team.get('specialiste_nom', 'N/A'),
                'specialite': h_team.get('specialiste_titre', 'N/A')
            }
        }
      }

      patients.append(patient_entry)
      
      print("\n" + "="*50)
      print("PATIENT ENREGISTRÉ:")
      print(f"ID: {patient_entry['id']}")
      print(f"Nom: {patient_entry['name']}")
      print(f"Ambulance: {patient_entry['ambulance']['id']} - {patient_entry['ambulance']['nom']}")
      print(f"Hôpital: {patient_entry['hospital']['name']}")
      print("="*50 + "\n")
      
      return jsonify({"status": "ok", "text": "Alerte traitée avec succès."})

    except Exception as e:
        print(f"Server Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/patient_info')
def patient_info():
    return render_patient_info(patients)

@app.route('/medical_reports')
def medical_reports():
    return render_medical_reports(patients)

@app.route('/download_report/<int:patient_id>/<report_type>')
def download_report(patient_id, report_type):
    patient = next((p for p in patients if p['id'] == patient_id), None)
    if not patient:
        return jsonify({"status": "error", "message": "Patient not found"}), 404
    
    if report_type == 'urgence':
        analyse_urgence = {
            'medecin': patient['hospital'].get('urgentiste', 'Dr. Urgence'),
            'diagnostic': f"Niveau d'urgence: {patient.get('niveau_urgence', 'N/A')}",
            'recommandations': f"Symptômes: {patient.get('symptomes', 'N/A')}"
        }
        pdf_buffer = generate_urgence_pdf(patient, analyse_urgence)
        return send_file(pdf_buffer, as_attachment=True, download_name=f"analyse_urgence_{patient['name']}.pdf", mimetype='application/pdf')
    
    elif report_type == 'specialiste':
        traitement_specialiste = {
            'specialiste_nom': patient['hospital']['specialiste'].get('nom', 'N/A'),
            'specialiste_titre': patient['hospital']['specialiste'].get('specialite', 'N/A'),
            'diagnostic': f"Condition: {patient.get('condition', 'En cours')}",
            'plan_traitement': f"Service: {patient['hospital'].get('service', 'Urgences')}",
            'prescriptions': 'Selon protocole établi'
        }
        pdf_buffer = generate_specialiste_pdf(patient, traitement_specialiste)
        return send_file(pdf_buffer, as_attachment=True, download_name=f"traitement_specialiste_{patient['name']}.pdf", mimetype='application/pdf')
    
    return jsonify({"status": "error", "message": "Invalid report type"}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
