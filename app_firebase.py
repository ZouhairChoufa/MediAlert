import sys, os
import json
import re
from datetime import datetime
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
from flask import Flask, request, jsonify, render_template, send_file, session, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from patient_info_page import render_patient_info
from medical_reports_page import render_medical_reports, generate_urgence_pdf, generate_specialiste_pdf
from systeme_urgences_medicales.crew import SystemeUrgencesMedicalesCrew
import firebase_config as fb

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_page'

class User(UserMixin):
    def __init__(self, uid, email, display_name):
        self.id = uid
        self.email = email
        self.display_name = display_name

@login_manager.user_loader
def load_user(user_id):
    profile = fb.get_user_profile(user_id)
    if profile:
        return User(user_id, profile['email'], profile['display_name'])
    return None

@app.route('/login')
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    try:
        user = fb.create_user(data['email'], data['password'], data['name'])
        return jsonify({'status': 'ok', 'message': 'Account created successfully'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    try:
        user = fb.verify_user(data['email'], data['password'])
        if user:
            user_obj = User(user.uid, user.email, user.display_name)
            login_user(user_obj)
            return jsonify({'status': 'ok', 'message': 'Login successful'})
        return jsonify({'status': 'error', 'message': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login_page'))

@app.route('/')
@login_required
def dashboard():
    profile = fb.get_user_profile(current_user.id)
    stats = fb.get_system_stats()
    
    stats.update({
        'total_patients': stats.get('total_alerts', 0),
        'active_alerts': stats.get('alerts_today', 0),
        'ambulances_dispatched': stats.get('total_alerts', 0),
        'avg_response_time': 8,
        'user': profile
    })
    
    return render_template('dashboard.html', **stats)

@app.route('/alert')
@login_required
def alert_page():
    return render_template('alert.html')

@app.route('/api/alert', methods=['POST'])
@login_required
def alert_api():
    payload = request.get_json() or {}
    
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
        crew = SystemeUrgencesMedicalesCrew().crew()
        result = crew.kickoff(inputs=inputs)
        
        final_output_str = str(result)
        
        data = {}
        try:
            json_match = re.search(r'\{.*\}', final_output_str, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group(0))
        except Exception as e:
            print(f"JSON Parsing Error: {e}")

        p_data = data.get('patient', {})
        a_data = data.get('ambulance', {})
        h_data = data.get('hopital', {})
        h_team = h_data.get('equipe', {})

        # Extract detailed medical data from AI agents
        raw_output = final_output_str
        
        patient_entry = {
            'name': p_data.get('nom', inputs.get('nom_prenom')),
            'age': p_data.get('age', inputs.get('age')),
            'sexe': p_data.get('sexe', inputs.get('sexe')),
            'symptomes': p_data.get('symptomes', inputs.get('symptomes')),
            'localisation': inputs.get('localisation'),
            'condition': p_data.get('condition', 'En cours d\'évaluation'),
            'niveau_urgence': p_data.get('niveau_urgence', 'URGENT'),
            'timestamp': datetime.now().isoformat(),
            'raw_ai_output': raw_output,  # Store complete AI analysis
            
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
                },
                'medical_analysis': {
                    'diagnostic_differentiel': data.get('diagnostic_differentiel', []),
                    'priorites_prise_en_charge': data.get('priorites_prise_en_charge', []),
                    'protocoles_recommandes': data.get('protocoles_recommandes', []),
                    'prescriptions': data.get('prescriptions', []),
                    'examens_complementaires': data.get('examens_complementaires', [])
                }
            }
        }

        # Save to Firebase
        alert_id = fb.save_alert(current_user.id, patient_entry)
        
        return jsonify({"status": "ok", "text": "Alerte traitée avec succès.", "alert_id": alert_id})

    except Exception as e:
        print(f"Server Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/patient_info')
@login_required
def patient_info():
    alerts = fb.get_user_alerts(current_user.id)
    patients = []
    for i, alert in enumerate(alerts):
        alert['id'] = i + 1
        patients.append(alert)
    return render_patient_info(patients)

@app.route('/medical_reports')
@login_required
def medical_reports():
    alerts = fb.get_user_alerts(current_user.id)
    patients = []
    for i, alert in enumerate(alerts):
        alert['id'] = i + 1
        patients.append(alert)
    return render_medical_reports(patients)

@app.route('/download_report/<int:patient_id>/<report_type>')
@login_required
def download_report(patient_id, report_type):
    alerts = fb.get_user_alerts(current_user.id)
    patient = alerts[patient_id - 1] if patient_id <= len(alerts) else None
    
    if not patient:
        return jsonify({"status": "error", "message": "Patient not found"}), 404
    
    if report_type == 'urgence':
        analyse_urgence = {
            'medecin': patient.get('hospital', {}).get('urgentiste', 'Dr. Urgence'),
            'diagnostic': f"Niveau d'urgence: {patient.get('niveau_urgence', 'N/A')}",
            'recommandations': f"Symptômes: {patient.get('symptomes', 'N/A')}"
        }
        pdf_buffer = generate_urgence_pdf(patient, analyse_urgence)
        return send_file(pdf_buffer, as_attachment=True, download_name=f"analyse_urgence_{patient['name']}.pdf", mimetype='application/pdf')
    
    elif report_type == 'specialiste':
        traitement_specialiste = {
            'specialiste_nom': patient.get('hospital', {}).get('specialiste', {}).get('nom', 'N/A'),
            'specialiste_titre': patient.get('hospital', {}).get('specialiste', {}).get('specialite', 'N/A'),
            'diagnostic': f"Condition: {patient.get('condition', 'En cours')}",
            'plan_traitement': f"Service: {patient.get('hospital', {}).get('service', 'Urgences')}",
            'prescriptions': 'Selon protocole établi'
        }
        pdf_buffer = generate_specialiste_pdf(patient, traitement_specialiste)
        return send_file(pdf_buffer, as_attachment=True, download_name=f"traitement_specialiste_{patient['name']}.pdf", mimetype='application/pdf')
    
    return jsonify({"status": "error", "message": "Invalid report type"}), 400

@app.route('/admin')
@login_required
def admin_panel():
    profile = fb.get_user_profile(current_user.id)
    if profile.get('role') != 'admin':
        return redirect(url_for('dashboard'))
    
    stats = fb.get_system_stats()
    all_alerts = fb.get_all_alerts()
    
    ambulances_data = [
        {"id": "AMB-001", "status": "active", "status_text": "En mission", "location": "Paris 15e"},
        {"id": "AMB-002", "status": "active", "status_text": "Disponible", "location": "Paris 8e"},
        {"id": "AMB-003", "status": "pending", "status_text": "En route", "location": "Paris 12e"},
        {"id": "AMB-004", "status": "active", "status_text": "Disponible", "location": "Paris 5e"},
    ]

    hospitals_data = [
        {"name": "Hôpital Central", "beds_available": 12, "status": "Available", "status_class": "success"},
        {"name": "Clinique Saint-Jean", "beds_available": 5, "status": "Limited", "status_class": "warning"},
        {"name": "Centre Médical Nord", "beds_available": 18, "status": "Available", "status_class": "success"},
        {"name": "Hôpital Universitaire", "beds_available": 2, "status": "Critical", "status_class": "danger"},
    ]

    medical_staff_data = [
        {"name": "Dr. Martin", "specialty": "Urgentiste", "status": "On Duty", "status_class": "success"},
        {"name": "Dr. Dubois", "specialty": "Cardiologue", "status": "On Duty", "status_class": "success"},
        {"name": "Dr. Laurent", "specialty": "Neurologue", "status": "Break", "status_class": "warning"},
        {"name": "Dr. Bernard", "specialty": "Chirurgien", "status": "On Duty", "status_class": "success"},
    ]

    activity_logs_data = [
        {"time": "14:32", "event": "Alert Created", "details": f"Total: {stats['total_alerts']}", "status": "Completed", "status_class": "success"},
        {"time": "14:28", "event": "Ambulance Dispatched", "details": "AMB-003 to Paris 12e", "status": "In Progress", "status_class": "warning"},
        {"time": "14:15", "event": "Hospital Admission", "details": "Patient admitted", "status": "Completed", "status_class": "success"},
    ]
    
    metrics = {
        'alerts_today': stats.get('alerts_today', 0),
        'avg_response': 8,
        'uptime': 99.8
    }
    
    return render_template('admin.html', 
                         ambulances=ambulances_data,
                         hospitals=hospitals_data,
                         medical_staff=medical_staff_data,
                         activity_logs=activity_logs_data,
                         metrics=metrics)

@app.route('/api-docs')
@login_required
def api_docs():
    return render_template('api_docs.html')

@app.route('/api/patients', methods=['GET'])
@login_required
def get_patients():
    alerts = fb.get_user_alerts(current_user.id)
    return jsonify({"status": "ok", "count": len(alerts), "patients": alerts})

@app.route('/api/patient/<alert_id>', methods=['GET'])
@login_required
def get_patient(alert_id):
    alerts = fb.get_user_alerts(current_user.id)
    patient = next((a for a in alerts if a['id'] == alert_id), None)
    if patient:
        return jsonify({"status": "ok", "patient": patient})
    return jsonify({"status": "error", "message": "Patient not found"}), 404

@app.route('/profile')
@login_required
def profile():
    profile = fb.get_user_profile(current_user.id)
    alerts = fb.get_user_alerts(current_user.id)
    return render_template('profile.html', profile=profile, alerts=alerts)

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
