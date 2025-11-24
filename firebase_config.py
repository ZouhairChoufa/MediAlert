import firebase_admin
from firebase_admin import credentials, firestore, auth
import os
from password_hash import scrypt_hash, verify_password

# Initialize Firebase Admin SDK
cred = credentials.Certificate('systemeemergecy-store-firebase-adminsdk-fbsvc-bd92fd1bb0.json')
firebase_admin.initialize_app(cred)

# Get Firestore client
db = firestore.client()

def create_user(email, password, display_name):
    """Create a new user in Firebase Auth"""
    try:
        user = auth.create_user(
            email=email,
            password=password,
            display_name=display_name
        )
        
        # Hash password
        password_hash = scrypt_hash(password)
        
        # Set role to admin for specific email
        role = 'admin' if email == 'zouhair.choufa3@gmail.com' else 'user'
        
        # Create user profile in Firestore
        db.collection('users').document(user.uid).set({
            'email': email,
            'display_name': display_name,
            'created_at': firestore.SERVER_TIMESTAMP,
            'total_alerts': 0,
            'role': role,
            'password_hash': password_hash
        })
        
        return user
    except Exception as e:
        raise Exception(f"Error creating user: {str(e)}")

def verify_user(email, password):
    """Verify user credentials"""
    try:
        user = auth.get_user_by_email(email)
        # Get user profile to check password hash
        profile = get_user_profile(user.uid)
        if profile and 'password_hash' in profile:
            if verify_password(password, profile['password_hash']):
                return user
        return None
    except Exception as e:
        return None

def get_user_profile(uid):
    """Get user profile from Firestore"""
    try:
        doc = db.collection('users').document(uid).get()
        if doc.exists:
            return doc.to_dict()
        return None
    except Exception as e:
        return None

def save_alert(user_id, alert_data):
    """Save alert to Firestore"""
    try:
        from datetime import datetime
        
        def make_serializable(obj):
            if isinstance(obj, dict):
                return {k: make_serializable(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [make_serializable(item) for item in obj]
            elif hasattr(obj, '__dict__'):
                return str(obj)
            else:
                return obj
        
        clean_data = make_serializable(alert_data)
        clean_data['user_id'] = user_id
        clean_data['created_at'] = datetime.now()
        
        alert_ref = db.collection('alerts').document()
        alert_ref.set(clean_data)
        
        user_ref = db.collection('users').document(user_id)
        user_ref.update({'total_alerts': firestore.Increment(1)})
        
        return alert_ref.id
    except Exception as e:
        raise Exception(f"Error saving alert: {str(e)}")

def get_user_alerts(user_id):
    """Get all alerts for a user"""
    try:
        alerts = db.collection('alerts').where(filter=firestore.FieldFilter('user_id', '==', user_id)).stream()
        result = [{'id': alert.id, **alert.to_dict()} for alert in alerts]
        result.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        print(f"Retrieved {len(result)} alerts from Firestore")
        return result
    except Exception as e:
        print(f"Error getting alerts: {e}")
        return []

def get_all_alerts():
    """Get all alerts (admin only)"""
    try:
        alerts = db.collection('alerts').order_by('created_at', direction=firestore.Query.DESCENDING).limit(100).stream()
        return [{'id': alert.id, **alert.to_dict()} for alert in alerts]
    except Exception as e:
        return []

def set_admin_role(email):
    """Set admin role for a user"""
    try:
        user = auth.get_user_by_email(email)
        db.collection('users').document(user.uid).update({'role': 'admin'})
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def get_system_stats():
    """Get system statistics"""
    try:
        total_users = len(list(db.collection('users').stream()))
        total_alerts = len(list(db.collection('alerts').stream()))
        
        # Get alerts from last 24 hours
        from datetime import datetime, timedelta
        yesterday = datetime.now() - timedelta(days=1)
        recent_alerts = db.collection('alerts').where(filter=firestore.FieldFilter('created_at', '>=', yesterday)).stream()
        alerts_today = len(list(recent_alerts))
        
        return {
            'total_users': total_users,
            'total_alerts': total_alerts,
            'alerts_today': alerts_today
        }
    except Exception as e:
        return {
            'total_users': 0,
            'total_alerts': 0,
            'alerts_today': 0
        }
