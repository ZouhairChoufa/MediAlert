"""
Setup script to create admin user
Run this once to set up your admin account
"""
import firebase_config as fb

# Set admin role for your email
admin_email = "zouhair.choufa@gmail.com"

try:
    result = fb.set_admin_role(admin_email)
    if result:
        print(f"✅ Admin role successfully set for {admin_email}")
        print("You can now login with admin privileges!")
    else:
        print(f"❌ Failed to set admin role. Make sure the user exists in Firebase Auth.")
        print(f"Please create an account first at http://localhost:5000/login")
except Exception as e:
    print(f"❌ Error: {e}")
    print(f"Make sure the user {admin_email} exists in Firebase Authentication")
