# 📤 Git Push Guide - MediAlert

## Quick Push (Automated)

Simply run the setup script:

```bash
git_setup.bat
```

This will automatically:
- Initialize Git repository
- Add remote origin
- Stage all files
- Create initial commit
- Push to GitHub

## Manual Push (Step by Step)

### 1. Initialize Git Repository

```bash
git init
```

### 2. Add Remote Repository

```bash
git remote add origin https://github.com/ZouhairChoufa/MediAlert.git
```

### 3. Stage Files

```bash
git add .
```

### 4. Create Initial Commit

```bash
git commit -m "Initial commit: MediAlert Pro - AI-Powered Emergency Medical System"
```

### 5. Rename Branch to Main

```bash
git branch -M main
```

### 6. Push to GitHub

```bash
git push -u origin main
```

## ⚠️ Important Notes

### Before Pushing

1. **Remove Sensitive Files**: Ensure Firebase credentials are not included
   - `systemeemergecy-store-firebase-adminsdk-fbsvc-bd92fd1bb0.json` should be in `.gitignore`
   - `.env` file should be excluded

2. **Verify .gitignore**: Check that sensitive files are properly ignored

3. **Update .env.example**: Ensure it has placeholder values only

### After Pushing

1. **Verify Repository**: Visit https://github.com/ZouhairChoufa/MediAlert
2. **Check Files**: Ensure no sensitive data was pushed
3. **Update Repository Settings**: 
   - Add description
   - Add topics/tags
   - Enable Issues
   - Add README preview

## 🔄 Subsequent Updates

After initial push, use standard Git workflow:

```bash
# Stage changes
git add .

# Commit changes
git commit -m "Your commit message"

# Push to GitHub
git push
```

## 🆘 Troubleshooting

### Remote Already Exists
```bash
git remote remove origin
git remote add origin https://github.com/ZouhairChoufa/MediAlert.git
```

### Force Push (Use with Caution)
```bash
git push -f origin main
```

### Check Remote URL
```bash
git remote -v
```

## ✅ Verification Checklist

- [ ] Firebase credentials excluded
- [ ] .env file excluded
- [ ] README.md updated with correct URLs
- [ ] LICENSE file included
- [ ] .gitignore properly configured
- [ ] All code files included
- [ ] Documentation files included
- [ ] No sensitive data in repository

---

**Repository URL**: https://github.com/ZouhairChoufa/MediAlert
