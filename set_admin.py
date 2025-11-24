import firebase_config as fb

email = "zouhair.choufa3@gmail.com"

try:
    user = fb.auth.get_user_by_email(email)
    fb.db.collection('users').document(user.uid).set({
        'email': email,
        'display_name': user.display_name or 'Admin',
        'role': 'admin',
        'total_alerts': 0
    }, merge=True)
    print(f"✓ Admin role set successfully for {email}")
except Exception as e:
    print(f"✗ Failed: {e}")
