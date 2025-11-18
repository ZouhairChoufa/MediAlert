import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
from flask import Flask, request, jsonify, render_template_string
from patient_info_page import render_patient_info
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
      input, textarea {
        width: 100%;
        padding: 12px;
        border: 2px solid #e0e0e0;
        border-radius: 8px;
        font-size: 14px;
        font-family: inherit;
        transition: border-color 0.3s;
      }
      input:focus, textarea:focus {
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
      .response-card.success {
        background: #e8f5e9;
        border-left: 5px solid #4caf50;
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
      .response-card.success .response-title {
        color: #2e7d32;
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
      .response-card.success .response-text {
        color: #1b5e20;
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
    inputs = {
        'symptomes': payload.get('symptomes', ''),
        'localisation': payload.get('localisation', ''),
        'nom_prenom': payload.get('nom_prenom', ''),
        'age': payload.get('age', ''),
        'sexe': payload.get('sexe', ''),
        'nv_urgence': payload.get('nv_urgence', ''),
        'localisation_ambulance': payload.get('localisation_ambulance', ''),
        'localisation_patient': payload.get('localisation_patient', '')
    }

    try:
      crew = SystemeUrgencesMedicalesCrew().crew()
      result = crew.kickoff(inputs=inputs)

      def to_dict_safe(obj):
        for method in ("to_dict", "dict", "toJSON", "json", "serialize", "to_serializable"):
          fn = getattr(obj, method, None)
          if callable(fn):
            try:
              return fn()
            except Exception:
              pass
        if isinstance(obj, dict):
          return obj
        try:
          return obj.__dict__
        except Exception:
          return {}

      result_dict = to_dict_safe(result) or {}
      
      result_text = str(result)
      
      import re
      
      ambulance_id = 'AMB-' + str(len(patients) + 1).zfill(3)
      ambulance_driver = 'Équipe disponible'
      ambulance_eta = '15-20 min'
      ambulance_localisation = inputs.get('localisation_ambulance') or 'Base centrale'
      
      # Try to extract from result text
      if 'ambulance' in result_text.lower():
          # Look for ambulance ID patterns
          amb_match = re.search(r'ambulance[:\s]+([A-Z0-9-]+)', result_text, re.IGNORECASE)
          if amb_match:
              ambulance_id = amb_match.group(1)
          
          # Look for ETA patterns
          eta_match = re.search(r'ETA[:\s]+(\d+[-\s]?\d*\s*min)', result_text, re.IGNORECASE)
          if eta_match:
              ambulance_eta = eta_match.group(1)
          
          # Look for driver/chauffeur
          driver_match = re.search(r'(?:chauffeur|driver|équipe)[:\s]+([A-Za-zÀ-ÿ\s]+?)(?:\n|,|\.|\|)', result_text, re.IGNORECASE)
          if driver_match:
              ambulance_driver = driver_match.group(1).strip()
      
      # Parse hospital info from text
      hospital_name = 'Hôpital d\'urgence le plus proche'
      hospital_address = 'En cours de détermination'
      hospital_status = 'En attente de confirmation'
      
      if 'hôpital' in result_text.lower() or 'hopital' in result_text.lower():
          # Look for hospital name
          hosp_match = re.search(r'(?:hôpital|hopital)[:\s]+([A-Za-zÀ-ÿ\s\'-]+?)(?:\n|,|\.|;)', result_text, re.IGNORECASE)
          if hosp_match:
              hospital_name = hosp_match.group(1).strip()
          
          # Look for address
          addr_match = re.search(r'(?:adresse|address)[:\s]+([^,\n]+)', result_text, re.IGNORECASE)
          if addr_match:
              hospital_address = addr_match.group(1).strip()
          
          # Look for status
          if 'accepté' in result_text.lower() or 'confirmé' in result_text.lower():
              hospital_status = 'Accepté'
          elif 'disponible' in result_text.lower():
              hospital_status = 'Disponible'

      # Build patient entry from submitted fields and attach any found ambulance/hospital info
      try:
        new_id = max([p.get('id', 0) for p in patients]) + 1 if patients else 1
      except Exception:
        new_id = len(patients) + 1

      patient_entry = {
        'id': new_id,
        'name': inputs.get('nom_prenom') or f'Patient {new_id}',
        'age': inputs.get('age') or '',
        'sexe': inputs.get('sexe') or '',
        'symptomes': inputs.get('symptomes') or '',
        'localisation': inputs.get('localisation') or '',
        'condition': 'Évaluation en cours',
        'ambulance': {
            'id': ambulance_id,
            'driver': ambulance_driver,
            'eta': ambulance_eta,
            'localisation': ambulance_localisation
        },
        'hospital': {
            'name': hospital_name,
            'address': hospital_address,
            'acceptance_status': hospital_status
        }
      }

      # Append to in-memory patients list (demo persistence)
      patients.append(patient_entry)
      
      # Print to console for debugging
      print("\n" + "="*50)
      print("PATIENT ENREGISTRÉ:")
      print(f"ID: {patient_entry['id']}")
      print(f"Nom: {patient_entry['name']}")
      print(f"Ambulance: {patient_entry['ambulance']['id']} - {patient_entry['ambulance']['driver']}")
      print(f"Hôpital: {patient_entry['hospital']['name']}")
      print("="*50 + "\n")

      # Extract a primary textual field from the CrewOutput for display
      def extract_text(obj):
        # Try common conversion methods first
        for method in ("to_dict", "dict", "toJSON", "json", "serialize", "to_serializable"):
          fn = getattr(obj, method, None)
          if callable(fn):
            try:
              obj = fn()
              break
            except Exception:
              pass

        # If it's a dict-like, look for common text fields
        def find_text(d):
          if d is None:
            return None
          if isinstance(d, str):
            return d
          if isinstance(d, list):
            # join list of strings or try first element recursively
            for item in d:
              t = find_text(item)
              if t:
                return t
            return None
          if isinstance(d, dict):
            for key in ("message", "text", "content", "output", "result", "answer", "body"):
              if key in d and d[key] is not None:
                t = find_text(d[key])
                if t:
                  return t
            # handle choices array (OpenAI style)
            if "choices" in d and isinstance(d["choices"], list) and len(d["choices"])>0:
              return find_text(d["choices"][0])
            # fallback: look at any string-valued item
            for v in d.values():
              t = find_text(v)
              if t:
                return t
          # fallback to string conversion
          try:
            return str(d)
          except Exception:
            return None

        # If obj has __dict__ and wasn't converted, try that
        if not isinstance(obj, (dict, list, str)):
          try:
            obj = obj.__dict__
          except Exception:
            pass

        text = find_text(obj)
        return text or "(no textual content)"

      text = extract_text(result)
      return jsonify({"status": "ok", "text": text})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/patient_info')
def patient_info():
    return render_patient_info(patients)

if __name__ == '__main__':
    app.run(debug=True, port=5000)