# THE PROJECT IN THE MAINTAIN AND CURRENT VERSION HAS BEEN REMOVED BECAUSE IT'S NOW SHIT AF. WILL BE UPDATED WHEN THE NEW VERSION IS AVAILABLE. YOU CAN CHECK PICTURES BELOW THERE. STAY TUNED.

# 🌾 Hayday Bot - Automated Farm Management Tool

## ⚠️ IMPORTANT DISCLAIMER

**This bot is 100% FREE!** If you paid for it, you have been scammed. The official source is available at the repository linked in the application.

**USE AT YOUR OWN RISK:** This bot automates gameplay which may violate the game's Terms of Service. We are not responsible for any account bans or other consequences. Use responsibly and at your own discretion.

## 📋 What This Bot Does

The Hayday Bot is an advanced automation tool designed to help with farming activities in Hay Day. It uses computer vision and template matching to:

- **Automate Farming Cycles**: Plant and harvest crops automatically
- **Detect Game States**: Recognize when fields need planting or harvesting
- **Handle Market Operations**: Navigate and interact with the market
- **Manage Multiple Accounts**: Switch between different farm configurations
- **Real-time Detection**: Live screenshot analysis with visual feedback
- **Template-based Recognition**: Uses image templates for precise game element detection

## 🖥️ Display Requirements

**CRITICAL**: This bot is designed specifically for **640x480 resolution 120 DPI**. Your emulator MUST be set to this resolution for the templates to work correctly.

## 🔧 Installation & Setup

### Prerequisites

1. **Python 3.13+** - Download from [python.org](https://python.org)
   - ⚠️ Make sure to check "Add Python to PATH" during installation
2. **Emulator** with Root and ADB enabled

### Quick Installation

1. **Clone or download** this bot to your computer
2. **Run the installer**:
   ```
   install.bat
   ```
3. **Start the application**:
   ```
   start.bat
   ```

### Manual Installation (if install.bat fails)

1. Open Command Prompt as Administrator
2. Navigate to the bot folder
3. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Launch the bot:
   ```
   python main.py
   ```

## 📱 Device Setup

### Recommended Emulators:
- **MEmu**
- Set resolution to **640x480**
- Set DPI to **120**
- Set engine to **DirectX**
- Enable Root in emulator settings
- Enable ADB in emulator settings

## 🎮 Application Interface Guide

### 🔌 Connection Tab

<img width="1222" height="832" alt="image" src="https://github.com/user-attachments/assets/c554a520-6d5d-46f2-900f-30b186ae8dbd" />

**Purpose**: Establish connection between bot and your device/emulator

**Features**:
- **Device Detection**: Automatically finds connected devices
- **Manual Device ID**: Enter device ID manually if auto-detection fails
- **Connection Status**: Real-time connection monitoring
- **Connection Testing**: Verify your device connection
- **Auto-refresh**: Automatically refresh device list

**How to Use**:
1. Connect your device/emulator
2. Click "Refresh Devices" to scan for devices
3. Select your device from the dropdown
4. Click "Connect" to establish connection
5. Use "Test Connection" to verify everything works

### 👤 Account Manager Tab

<img width="1222" height="832" alt="image" src="https://github.com/user-attachments/assets/5211dcef-f1c3-472a-a66d-897610b48242" />
<img width="752" height="682" alt="image" src="https://github.com/user-attachments/assets/c7202174-f9a4-4f36-a808-e39716854148" />

**Purpose**: Manage multiple farm configurations and accounts

**Features**:
- **Multiple Profiles**: Save different farm setups
- **Account Switching**: Quick switching between configurations
- **Settings Management**: Store account-specific settings
- **Configuration Management**: Create, copy, rename, and delete multiple farm configurations

**How to Use**:
1. Create a new profile for each farm account
2. Configure settings specific to each account
3. Switch between profiles as needed
4. Save configurations for future use

### 🤖 Bot Control Tab

<img width="1222" height="832" alt="image" src="https://github.com/user-attachments/assets/87979abe-613e-471a-ab75-3a6e7440ece4" />

**Purpose**: Main control center for bot operations

**Features**:
- **Game Controls**: Launch/stop Hay Day
- **Bot Start/Stop**: Control automation
- **Live Detection**: Real-time screenshot analysis
- **Activity Log**: Monitor bot activities and errors
- **Visual Feedback**: See what the bot detects in real-time

**How to Use**:
1. Ensure device is connected
2. Launch Hay Day using "Launch Game"
3. Start "Live Detection" to see what bot sees
4. Configure your farm settings
5. Click "Start Bot" to begin automation
6. Monitor progress in Activity Log

### ⚙️ Farm Config Tab

<img width="1222" height="832" alt="image" src="https://github.com/user-attachments/assets/8d801791-2059-4970-8be1-e157bf728dbf" />

**Purpose**: Configure farming settings and field locations

**Features**:
- **Field Selection**: Define which fields to farm
- **Crop Selection**: Choose what crops to plant
- **Timing Settings**: Configure planting/harvesting delays
- **Detection Areas**: Set up field detection zones
- **Navigation Setup**: Configure navigation points

**How to Use**:
1. Take a screenshot of your farm
2. Select field locations by clicking on them
3. Choose your preferred crops
4. Set timing intervals between actions
5. Configure thresholds
6. Save your configuration

### 🖼️ Template Manager Tab

<img width="1222" height="832" alt="image" src="https://github.com/user-attachments/assets/66e6aff9-6899-4548-baa8-bb3dda1d359d" />

**Purpose**: Manage image templates for game element recognition

**Features**:
- **Template Library**: View all available templates
- **Custom Templates**: Add your own image templates
- **Template Testing**: Test template recognition
- **Resolution Matching**: Ensure templates match your screen resolution

**How to Use**:
1. Browse existing templates
2. Add new templates for better recognition
3. Test templates against screenshots
4. Organize templates by category

## 📁 Template System

The bot uses image templates stored in the `templates/` folder:

```
templates/
├── main/           # Main game UI elements
├── market/         # Market interface elements
├── offer/          # Offer/deal recognition
└── advert/         # Advertisement detection
└── plants/         # Plant detection
```

**Resolution**: All templates are designed for **640x480** resolution.

## 🚀 Getting Started - Step by Step

### Step 1: Initial Setup
1. Run `install.bat` to install dependencies
2. Ensure your device/emulator is set to 640x480 120 DPI resolution
3. Enable root on your device

### Step 2: Connect Device
1. Open the bot with `start.bat`
2. Go to **Connection** tab
3. Select device and click "Connect"
4. Test connection to ensure it works

### Step 3: Configure Your Farm
1. Go to **Farm Config** tab
2. Take a screenshot of your farm
3. Mark field locations by clicking on them
4. Select crops you want to farm
5. Set other preferences
6. Save your configuration

### Step 4: Start Botting
1. Go to **Bot Control** tab
2. Click "Start Bot" to begin automation
3. Monitor the Activity Log for progress

## 🔧 Troubleshooting

### Common Issues:

**"No devices found"**
- Restart ADB: `adb kill-server` then `adb start-server`

**"Connection failed"**
- Device may be unauthorized - check for debugging prompt
- Try `adb devices` in command prompt to see device status
- Restart both device and computer if needed

**"Bot not detecting fields/elements"**
- Ensure screen resolution is exactly 640x480 120 DPI
- Check template images match your game version
- Verify field locations are correctly marked
- Try taking new template screenshots

**"Python not found"**
- Reinstall Python with "Add to PATH" option checked
- Run `install.bat` as Administrator
- Manually add Python to system PATH

**"Game crashes or bot stops working"**
- Check Activity Log for error messages
- Restart the game and bot
- Verify device connection is stable
- Update bot to latest version

### Performance Tips:

- **Close unnecessary apps** on your device/emulator
- **Keep emulator settings optimized** for performance
- **Monitor system resources** while bot is running

## 🐛 Known Issues

### Too Much Stuff
- Which you cant even figure it out

Please report any other issues you encounter to help improve the bot.

## ❓ Frequently Asked Questions

**Q: Is this bot safe to use?**
A: The bot operates externally and doesn't modify game files, but automation may violate ToS. Use at your own risk.

**Q: Can I use this on mobile?**
A: No, this bot is designed specifically for MEmu on PC.

**Q: Why does my bot click in wrong places?**
A: Make sure your screen resolution is exactly 640x480 120 DPI. Different resolutions will cause coordinate misalignment.

**Q: Can I run multiple multi cycles for different accounts?**
A: Yes, but you'll need separate device connections like multiple emulator instances.

**Q: How do I edit the templates?**
A: Use the Template Manager tab to edit templates, or manually add image files to the appropriate templates subfolder.

**Q: The bot is too fast/slow, can I adjust speed?**
A: Yes, use the Farm Config tab to adjust timing intervals between actions.

## 🛠️ Advanced Configuration

### Fine-tuning Detection
- Adjust detection thresholds in configuration files
- Customize field detection areas for better accuracy

## 📞 Support

- Check the Activity Log for error messages
- Ensure all requirements are met (resolution, drivers, etc.)
- Try the troubleshooting steps above
- Review the FAQ section

## 🔄 Updates and Maintenance

- Keep your Python installation updated
- Check for bot updates regularly
- Backup your configurations before major updates

## 🔮 Future Planning Implementations

> *"Like my mind's endless wheat fields of ideas, this road ahead is paved with dreams, unfinished tasks, and that one suspicious gnome who keeps watching my master plan unfold* 🌾🤪 *"*

---

**Remember**: This tool is for educational purposes. Always respect the game's Terms of Service and use automation responsibly.

## 🙏 Special Thanks

Thanks to @Gercekefsane for providing and contributing hints about some critical ideas and methods.
