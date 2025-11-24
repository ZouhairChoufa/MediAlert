# ⚡ Quick Start Guide - MediAlert Pro

Get your professional medical emergency system running in 5 minutes!

## 🚀 Installation (2 minutes)

### Step 1: Install UV
```bash
pip install uv
```

### Step 2: Install Dependencies
```bash
cd systeme_urgences_medicales_Groq-project
uv sync
```

### Step 3: Configure Environment
```bash
# Copy the example environment file
copy .env.example .env

# Edit .env and add your Groq API key
# GROQ_API_KEY=your_key_here
```

## ▶️ Run the Application (30 seconds)

### Option 1: New Professional Version (Recommended)
```bash
uv run python app.py
```

### Option 2: Original Version
```bash
uv run python web_app.py
```

## 🌐 Access the System

Open your browser and visit:

```
🏠 Dashboard:        http://localhost:5000
🆘 Create Alert:     http://localhost:5000/alert
👥 Patients:         http://localhost:5000/patient_info
📋 Reports:          http://localhost:5000/medical_reports
⚙️  Admin Panel:     http://localhost:5000/admin
📚 API Docs:         http://localhost:5000/api-docs
```

## 🎯 First Steps

### 1. Explore the Dashboard
- View system statistics
- Check out feature cards
- Navigate to different sections

### 2. Create Your First Alert
1. Click "Create Emergency Alert" button
2. Fill in symptoms: "Severe chest pain, difficulty breathing"
3. Add location: "123 Main Street, Paris"
4. Optionally add patient details
5. Click "Send Emergency Alert"
6. Watch the AI agents coordinate the response!

### 3. View Patient Information
- See the assigned ambulance
- Check hospital destination
- View medical team details
- Track response times

### 4. Generate Medical Reports
- Navigate to Medical Reports
- Download PDF reports
- Review emergency analysis
- Check specialist treatment plans

### 5. Monitor the System
- Open Admin Panel
- View ambulance fleet status
- Check hospital network
- Monitor medical staff
- Review activity logs

## 📱 Quick Feature Tour

### Dashboard Features
✅ Real-time statistics
✅ System performance metrics
✅ Quick action buttons
✅ Feature showcase

### Alert System
✅ Easy form submission
✅ Real-time validation
✅ AI-powered processing
✅ Instant coordination

### Patient Management
✅ Comprehensive patient records
✅ Ambulance assignments
✅ Hospital destinations
✅ Medical team info

### Admin Panel
✅ Fleet monitoring
✅ Hospital network status
✅ Staff tracking
✅ Activity logs

### API Access
✅ RESTful endpoints
✅ JSON responses
✅ Complete documentation
✅ Easy integration

## 🔧 Common Tasks

### Create an Emergency Alert via API
```bash
curl -X POST http://localhost:5000/api/alert \
  -H "Content-Type: application/json" \
  -d '{
    "symptomes": "Severe headache and dizziness",
    "localisation": "456 Oak Avenue, Lyon",
    "nom_prenom": "Marie Dubois",
    "age": 32,
    "sexe": "F"
  }'
```

### Get All Patients
```bash
curl http://localhost:5000/api/patients
```

### Get Specific Patient
```bash
curl http://localhost:5000/api/patient/1
```

### Check Ambulance Fleet
```bash
curl http://localhost:5000/api/ambulances
```

### View Hospital Network
```bash
curl http://localhost:5000/api/hospitals
```

## 🎨 Customization Quick Tips

### Change Brand Name
Edit templates (dashboard.html, alert.html, etc.):
```html
<a href="/" class="logo">🏥 Your Brand Name</a>
```

### Update Colors
Edit `static/css/main.css`:
```css
:root {
  --primary: #YOUR_COLOR;
  --secondary: #YOUR_COLOR;
}
```

### Modify Statistics
Edit `app.py`:
```python
stats = {
    'total_patients': your_value,
    'active_alerts': your_value,
    ...
}
```

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Change port in app.py
app.run(debug=True, port=5001)
```

### Module Not Found
```bash
uv sync --force
```

### API Key Error
```bash
# Check .env file exists
# Verify GROQ_API_KEY is set
# Restart the application
```

## 📚 Learn More

- **Full Documentation**: See README.md
- **Deployment Guide**: See DEPLOYMENT.md
- **Feature List**: See FEATURES.md
- **API Reference**: http://localhost:5000/api-docs
- **Changelog**: See CHANGELOG.md

## 🎯 What's Next?

### For Development
1. Read FEATURES.md for complete feature list
2. Explore the code structure
3. Customize the design
4. Add your own features

### For Production
1. Read DEPLOYMENT.md
2. Configure environment variables
3. Set up monitoring
4. Deploy to your server

### For Integration
1. Check API documentation
2. Test endpoints
3. Integrate with your systems
4. Build custom features

## 💡 Pro Tips

1. **Use the Admin Panel** to monitor system health
2. **Check API Docs** for integration examples
3. **Review Activity Logs** to track system events
4. **Download PDF Reports** for documentation
5. **Test with Sample Data** before going live

## 🆘 Need Help?

- **Documentation**: All .md files in project root
- **API Docs**: http://localhost:5000/api-docs
- **GitHub Issues**: Report bugs and request features
- **Community**: Join CrewAI Discord

## ✅ Checklist

Before going live, make sure you:
- [ ] Configured environment variables
- [ ] Tested alert creation
- [ ] Verified API endpoints
- [ ] Reviewed admin panel
- [ ] Generated test reports
- [ ] Checked all pages
- [ ] Read deployment guide
- [ ] Set up monitoring
- [ ] Configured backups
- [ ] Tested on mobile

## 🎉 You're Ready!

Your professional medical emergency system is now running!

**Start saving lives with AI-powered emergency coordination!** 🚑💙

---

**Quick Links**:
- Dashboard: http://localhost:5000
- Admin: http://localhost:5000/admin
- API Docs: http://localhost:5000/api-docs

**Support**: Check README.md for detailed documentation
