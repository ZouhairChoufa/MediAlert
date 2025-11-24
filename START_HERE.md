# 🚀 START HERE - MediAlert Pro Quick Setup

> **Welcome to MediAlert Pro!** This guide will get you up and running in under 5 minutes.

## 🎯 What is MediAlert Pro?

**AI-Powered Emergency Medical System** that coordinates ambulances, hospitals, and medical staff through intelligent multi-agent collaboration. Think of it as the brain that manages emergency medical responses automatically.

### ⚡ Key Capabilities
- **Instant Emergency Processing**: Submit alerts and get AI-powered triage
- **Smart Ambulance Dispatch**: Automatic selection of nearest available ambulance
- **Hospital Coordination**: Real-time bed availability and specialist matching
- **Medical Reports**: AI-generated diagnosis and treatment plans

## 🏃‍♂️ Quick Start (5 Minutes)

### Step 1: Prerequisites Check
```bash
# Check Python version (3.10-3.13 required)
python --version

# If you don't have Python 3.10+, download from:
# https://www.python.org/downloads/
```

### Step 2: Get Your API Key
1. Visit [Groq Console](https://console.groq.com/)
2. Sign up/Login
3. Create API key
4. Copy the key (you'll need it in Step 4)

### Step 3: Clone & Install
```bash
# Clone the repository
git clone https://github.com/ZouhairChoufa/MediAlert.git
cd MediAlert

# Install UV package manager
pip install uv

# Install all dependencies
uv sync
```

### Step 4: Configure Environment
```bash
# Copy environment template
cp .env.example .env

# Edit .env file and add your Groq API key:
# GROQ_API_KEY=your_groq_api_key_here
```

### Step 5: Launch Application
```bash
# Start the system
uv run python app.py

# Open your browser to:
# http://localhost:5000
```

## 🎉 You're Ready!

Visit these pages to explore:

| Page | URL | Purpose |
|------|-----|---------|
| **Dashboard** | http://localhost:5000 | System overview and statistics |
| **Emergency Alert** | http://localhost:5000/alert | Create new emergency alerts |
| **Patient Info** | http://localhost:5000/patient_info | View patient records |
| **Medical Reports** | http://localhost:5000/medical_reports | AI-generated medical reports |
| **Admin Panel** | http://localhost:5000/admin | System management |
| **API Docs** | http://localhost:5000/api-docs | Complete API reference |

## 🧪 Test the System

### Create Your First Emergency Alert

1. Go to http://localhost:5000/alert
2. Fill in the form:
   - **Name**: John Doe
   - **Age**: 45
   - **Gender**: Male
   - **Symptoms**: Severe chest pain
   - **Location**: 123 Main St, Paris
3. Click "Submit Emergency Alert"
4. Watch the AI agents work their magic! 🤖

### View the Results

- **Patient Info**: See ambulance assignment and hospital destination
- **Medical Reports**: Download AI-generated diagnosis and treatment plan
- **Admin Panel**: Monitor system performance

## 📚 What's Next?

### For Users
- [📖 Full Documentation](README.md) - Complete feature guide
- [🔌 API Reference](http://localhost:5000/api-docs) - Integrate with your systems
- [⚙️ Configuration Guide](DEPLOYMENT.md) - Advanced setup options

### For Developers
- [🏗️ Architecture Overview](README.md#system-architecture) - Understand the AI agents
- [🤖 Agent Configuration](src/systeme_urgences_medicales/config/) - Customize AI behavior
- [🧪 Testing Guide](tests/) - Run and write tests
- [🚀 Deployment Guide](DEPLOYMENT.md) - Production deployment

### For Contributors
- [🤝 Contributing Guide](README.md#contributing) - How to contribute
- [📋 Project Structure](README.md#project-structure) - Codebase overview
- [🐛 Issue Tracker](https://github.com/ZouhairChoufa/MediAlert/issues) - Report bugs

## 🆘 Need Help?

### Common Issues

**"ModuleNotFoundError"**
```bash
# Make sure you're using UV
uv sync
uv run python app.py
```

**"API Key Error"**
```bash
# Check your .env file has:
GROQ_API_KEY=your_actual_api_key_here
```

**"Port 5000 in use"**
```bash
# Use a different port
uv run python app.py --port 8080
```

### Get Support
- 📖 [Full Documentation](README.md)
- 🐛 [GitHub Issues](https://github.com/ZouhairChoufa/MediAlert/issues)
- 💬 [CrewAI Discord](https://discord.com/invite/X4JWnZnxPb)

## 🌟 Key Features to Explore

### 🤖 AI Agents in Action
The system uses 7 specialized AI agents:
- **Patient Agent**: Processes emergency alerts
- **Coordinator Agent**: Orchestrates response
- **Ambulance Agent**: Handles dispatch
- **Hospital Agent**: Manages admissions
- **Emergency Physician**: Provides diagnosis
- **Specialist Agent**: Creates treatment plans
- **Administrative Agent**: Generates reports

### 📊 Real-Time Dashboard
Monitor system performance with live metrics:
- Active emergencies
- Ambulance fleet status
- Hospital capacity
- Response times

### 🔌 RESTful API
Integrate with existing systems:
```bash
# Create emergency alert
curl -X POST http://localhost:5000/api/alert \
  -H "Content-Type: application/json" \
  -d '{"symptomes":"chest pain","localisation":"Paris","nom_prenom":"John Doe","age":45,"sexe":"M"}'

# Get all patients
curl http://localhost:5000/api/patients
```

## 🎯 Success Checklist

- [ ] Python 3.10+ installed
- [ ] Groq API key obtained
- [ ] Repository cloned
- [ ] Dependencies installed with `uv sync`
- [ ] Environment configured (.env file)
- [ ] Application running on http://localhost:5000
- [ ] First emergency alert created successfully
- [ ] Medical report generated and downloaded

## 🚀 Ready to Save Lives!

You now have a fully functional AI-powered emergency medical system. The system is designed to be intuitive, so feel free to explore all the features.

**Remember**: This is a demonstration system. For production use, ensure proper security, compliance, and integration with real emergency services.

---

<div align="center">

**🏥 MediAlert Pro - AI-Powered Emergency Medical System**

[🌐 Website](https://medialert-pro.com) • [📖 Docs](README.md) • [🐛 Issues](https://github.com/ZouhairChoufa/MediAlert/issues) • [💬 Discord](https://discord.com/invite/X4JWnZnxPb)

**Built with ❤️ for saving lives**

</div>