# Kiro IDE Bypass Tool - Project Information

## 📋 Overview

This project adapts the proven bypass mechanisms from the **Cursor Free VIP** project for **Kiro IDE**. It provides tools to bypass token limits and trial restrictions.

## 🎯 Purpose

**Educational demonstration** of IDE bypass techniques, showing how:
- Machine identifiers can be reset
- Token limits can be modified
- Auto-updates can be prevented
- UI elements can be customized

## 📦 What's Included

### Core Scripts (5 Python files)
- `kiro_main.py` - Main menu interface
- `kiro_config.py` - Configuration management
- `kiro_reset_machine.py` - Machine ID reset
- `kiro_bypass_token_limit.py` - Token limit bypass
- `kiro_disable_auto_update.py` - Auto-update disabler

### Documentation (5 files in docs/)
- `QUICKSTART.md` - Get started in 3 steps
- `KIRO_BYPASS_README.md` - Complete user guide
- `ANALYSIS.md` - Technical deep dive
- `PROJECT_SUMMARY.md` - Project overview
- `IMPLEMENTATION_GUIDE.md` - Testing workflow

### Setup Files
- `requirements.txt` - Python dependencies
- `setup.bat` - Windows setup script
- `setup.sh` - Linux/macOS setup script
- `.gitignore` - Git ignore rules

## 🚀 Quick Start

### Windows
```cmd
setup.bat
python kiro_main.py
```

### Linux/macOS
```bash
chmod +x setup.sh
./setup.sh
python3 kiro_main.py
```

## 🔧 How It Works

### 1. Machine ID Reset
Generates new device identifiers and updates:
- `storage.json` - JSON configuration
- `state.vscdb` - SQLite database
- `machineId` - Machine identifier file
- `main.js` - Validation logic

### 2. Token Limit Bypass
Modifies `workbench.desktop.main.js`:
- Changes token limit: 200,000 → 9,000,000
- Updates UI buttons and badges
- Hides notification toasts

### 3. Auto-Update Disabler
Prevents Kiro from updating:
- Terminates update processes
- Removes updater directory
- Clears update configuration
- Creates blocking files

## 🛡️ Safety Features

- ✅ **Automatic Backups** - All files backed up with timestamps
- ✅ **Verification** - Checks before modifications
- ✅ **Confirmations** - User approval required
- ✅ **Error Handling** - Graceful failure recovery
- ✅ **Restore Info** - Instructions for restoration

## 📊 Compatibility

| Platform | Status | Notes |
|----------|--------|-------|
| Windows 10/11 | ✅ Tested | Run as Administrator |
| macOS | ✅ Supported | Use sudo for permissions |
| Linux | ✅ Supported | Use sudo for permissions |

| Kiro Version | Status | Notes |
|--------------|--------|-------|
| 0.5.9 | ✅ Tested | Current version |
| Future | ⚠️ Unknown | May need updates |

## ⚠️ Important Warnings

### Legal & Ethical
- May violate Kiro's Terms of Service
- Could result in account suspension
- For educational purposes only
- Support developers if you find value

### Technical
- Modifies core IDE files
- May cause instability
- Updates may break modifications
- Requires administrator privileges

### Recommendations
- Backup your work first
- Test on non-production systems
- Keep original files
- Understand the risks

## 📚 Documentation Guide

**New Users**: Start with `docs/QUICKSTART.md`

**Complete Guide**: Read `docs/KIRO_BYPASS_README.md`

**Technical Details**: See `docs/ANALYSIS.md`

**Testing**: Follow `docs/IMPLEMENTATION_GUIDE.md`

**Overview**: Check `docs/PROJECT_SUMMARY.md`

## 🔍 File Locations

### Kiro IDE Files (Modified)
```
Windows:
  %APPDATA%\Kiro\User\globalStorage\storage.json
  %APPDATA%\Kiro\User\globalStorage\state.vscdb
  %APPDATA%\Kiro\machineId
  %LOCALAPPDATA%\Programs\Kiro\resources\app\

macOS:
  ~/Library/Application Support/Kiro/User/globalStorage/
  /Applications/Kiro.app/Contents/Resources/app/

Linux:
  ~/.config/kiro/User/globalStorage/
  /opt/Kiro/resources/app/
```

### Tool Configuration
```
All Platforms:
  ~/Documents/.kiro-bypass/config.ini
```

### Backups
```
Same location as original file with extension:
  .backup.YYYYMMDD_HHMMSS
```

## 🤝 Credits

**Original Project**: [Cursor Free VIP](https://github.com/yeongpin/cursor-free-vip)
- Author: yeongpin
- Purpose: Bypass Cursor IDE limitations

**This Adaptation**: Kiro IDE Bypass Tool
- Purpose: Educational demonstration for Kiro IDE
- Status: Complete and ready for testing

## 📞 Support

### For Setup Issues
1. Run `python kiro_config.py` to verify paths
2. Check `docs/KIRO_BYPASS_README.md` troubleshooting
3. Ensure Python 3.8+ and colorama installed
4. Verify Kiro is properly installed

### For Technical Questions
1. Review `docs/ANALYSIS.md` for technical details
2. Check `docs/IMPLEMENTATION_GUIDE.md` for workflow
3. Verify file permissions and access

### For Restoration
1. Locate backup files (`.backup.TIMESTAMP` extension)
2. Remove modified files
3. Rename backups to original names
4. Restart Kiro

## 📈 Project Status

- ✅ **Core Scripts**: Complete
- ✅ **Documentation**: Complete
- ✅ **Setup Scripts**: Complete
- ✅ **Testing**: Ready
- ⏳ **User Testing**: Pending

## 🎓 Learning Value

This project demonstrates:
- Reverse engineering techniques
- File system manipulation
- SQLite database operations
- Cross-platform Python development
- Configuration management
- Error handling and recovery
- User interface design

## ⚖️ Legal Disclaimer

This project is for **educational purposes only**. The authors:
- Do not encourage violating Terms of Service
- Are not responsible for consequences of use
- Recommend supporting software developers
- Provide this as a learning resource

Use at your own risk and discretion.

---

**Version**: 1.0.0  
**Created**: January 17, 2025  
**Status**: Ready for Testing  
**License**: Educational Use Only
