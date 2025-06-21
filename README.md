# Hayday Bot - Automated Farm Management Tool

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)
![Android](https://img.shields.io/badge/Android-ADB-green.svg)
![GUI](https://img.shields.io/badge/GUI-PyQt6-orange.svg)

## 📋 Table of Contents

- [About](#about)
- [Features](#features)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)
- [Template Management](#template-management)
- [Advanced Configuration](#advanced-configuration)
- [FAQ](#faq)
- [Contributing](#contributing)
- [Disclaimer](#disclaimer)

## 🎯 About

Hayday Bot is an advanced automation tool designed to help players manage their farms in the popular mobile game Hay Day. Using computer vision and ADB (Android Debug Bridge), this bot can automatically perform farming tasks such as planting wheat, harvesting crops, and managing market operations.

### Key Capabilities
- **Automated Farming**: Plant and harvest wheat automatically
- **Market Management**: Create offers, collect sold items, and manage advertisements
- **Template-Based Detection**: Uses image recognition to interact with game elements
- **Customizable Zones**: Define specific field areas for farming operations
- **Real-time Monitoring**: GUI with live status updates and logging

## ✨ Features

### 🌾 Farming Automation
- **Smart Field Detection**: Uses decoration-based navigation to locate field centers
- **Polygon Field Zones**: Define custom field boundaries for precise farming
- **Harvest & Plant Cycles**: Automated wheat farming with optimal timing
- **Human-like Movements**: Natural drag patterns to avoid detection

### 🏪 Market Operations
- **Automated Selling**: Create wheat offers at optimal prices
- **Collection System**: Automatically collect sold items and coins
- **Advertisement Management**: Create and manage newspaper advertisements
- **Price Optimization**: Choose between low/high pricing strategies

### 🎮 Device Control
- **ADB Integration**: Full Android device control via USB
- **Minitouch Support**: Fast and accurate touch input
- **Screenshot Analysis**: Real-time game state detection
- **Multi-device Support**: Connect to different Android devices

### 🖥️ User Interface
- **Connection Tab**: Device management and game launching
- **Bot Control**: Start/stop automation with real-time status
- **Farm Configuration**: Visual field setup and decoration selection
- **Template Manager**: Manage detection templates and thresholds

## 💻 System Requirements

### Hardware
- **Computer**: Windows 10/11 (64-bit recommended)
- **RAM**: Minimum 4GB, 8GB recommended
- **Storage**: At least 500MB free space

### Software
- **Python**: Version 3.8 or higher
- **Emulator**: Memu Play (recommended)

### Required Emulator Settings
- **Resolution**: 1920x1080 (MUST be set exactly)
- **Graphics Engine**: DirectX
- **Graphics Renderer**: OpenGL
- **Performance Settings**: At least 2 CPU cores and 2GB RAM allocated

### Tested Emulators
- Memu Play (Recommended)
  - Ensure resolution is set to 1920x1080
  - Templates are optimized for this resolution
  - Other resolutions will cause detection issues

## 🚀 Installation

### Step 1: Download and Extract
1. Download the repository
2. Extract all files to a folder (e.g., `C:\HaydayBot\`)

### Step 2: Install Dependencies
Run the installation script as Administrator:

```batch
install.bat
```

This will:
- Check Python installation
- Install required packages (PyQt6, OpenCV, NumPy, Pillow)
- Test ADB functionality

### Step 3: Emulator Setup
1. Install Memu Play emulator
2. Configure emulator settings:
   - Set resolution to 1920x1080 (Required)
   - Allocate sufficient CPU and RAM
   - Use OpenGL renderer for best performance
3. Install and launch Hay Day in the emulator

### Step 4: First Launch
1. Start the bot:
   ```batch
   start.bat
   ```
2. Use the Connection tab to connect to your emulator
3. Follow the configuration steps in the Farm Config tab

## ⚙️ Configuration

### Initial Setup

1. **Launch the Application**:
   ```batch
   start.bat
   ```

2. **Connect Your Device**:
   - Use the Connection tab
   - Select your device from the dropdown
   - Click "Connect Device"
   - Test connection and launch Hay Day

3. **Configure Your Farm**:
   - Navigate to the Farm Config tab
   - Select your navigation decoration
   - Define your field area using polygon selection
   - Set tool offsets for planting and harvesting

### Field Configuration

#### Navigation Decoration
Choose a decoration near your fields that will serve as a reference point:
- **Gnome**: Most reliable for detection
- **Purple Flower**: Alternative option
- **Custom**: Add your own decoration templates

#### Field Zone Setup
1. Click "Select Field Area" in Farm Config
2. Click points around your field perimeter
3. Ensure the polygon covers all your wheat fields
4. Click "Finish Selection" to save

#### Tool Offsets
Adjust where tools appear relative to your field center:
- **Harvest Offset**: Position for the scythe tool
- **Plant Offset**: Position for the seed bag tool

### Template Configuration

Templates are images used for game element detection. Each template has:
- **Image File**: PNG image of the game element
- **Threshold**: Detection sensitivity (0.1-1.0)
- **Category**: main, market, offer, advert, decorations

## 🎮 Usage

### Basic Operation

1. **Start the Bot**:
   - Ensure Hay Day is running and visible
   - Go to Bot Control tab
   - Click "Start Bot"

2. **Monitor Progress**:
   - Watch the log for status updates
   - View detection overlays in real-time
   - Check cycle progress indicators

3. **Stop the Bot**:
   - Click "Stop Bot" in Bot Control
   - Bot will finish current action before stopping

### Farming Cycle

The bot follows this automated sequence:

1. **Field Detection**: Locates field center using decoration
2. **State Analysis**: Determines if fields need harvesting or planting
3. **Harvesting**: Collects mature wheat using natural movements
4. **Planting**: Plants new wheat seeds in empty fields
5. **Market Operations**: Manages selling and advertisements
6. **Wait Period**: Monitors market while wheat grows (2 minutes)

### Market Management

During farming cycles, the bot will:
- Collect sold wheat and coins
- Create new offers when slots are available
- Manage newspaper advertisements
- Optimize pricing based on your settings

## 🔧 Troubleshooting

### Common Issues

#### Bot Won't Start
**Problem**: "No device connected" or "No configuration selected"
**Solutions**:
- Verify emulator is running and Hay Day is launched
- Check that Memu Play is properly installed
- Restart the emulator
- Restart the application

#### Detection Issues
**Problem**: Bot can't find game elements
**Solutions**:
- Verify emulator resolution is exactly 1920x1080
- Ensure game window is fully visible and not minimized
- Check that game is running in full screen
- Templates are designed for 1920x1080 - other resolutions will fail

#### Connection Problems
**Problem**: Emulator connects but commands fail
**Solutions**:
- Restart Memu Play
- Close and relaunch Hay Day
- Restart the bot application
- Try running `adb kill-server` then start the bot again

#### Field Detection Failures
**Problem**: Can't find field center or navigation decoration
**Solutions**:
- Verify game resolution is 1920x1080
- Check that decoration matches template exactly
- Ensure field is fully visible on screen
- Try repositioning the decoration

### Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| "Python not found" | Python not installed/in PATH | Install Python 3.8+ and add to PATH |
| "ADB devices empty" | Emulator not detected | Restart Memu Play |
| "Template not found" | Missing template files | Verify templates folder structure |
| "Field zone invalid" | Polygon not defined | Use "Select Field Area" to define zone |
| "Resolution mismatch" | Wrong emulator settings | Set resolution to 1920x1080 |

### Performance Issues

#### Slow Detection
- Ensure emulator has enough allocated resources
- Close other resource-intensive applications
- Use OpenGL renderer in Memu settings
- Reduce background processes

#### High CPU Usage
- Increase detection intervals
- Lower screenshot frequency
- Close other programs
- Allocate more CPU cores to the emulator

## 🖼️ Template Management

### Template Structure
```
templates/
├── decorations/     # Navigation decorations
│   ├── gnome.png
│   └── flower_purple.png
├── main/           # Main game elements
│   ├── wheat.png
│   ├── soil.png
│   ├── market.png
│   └── escape.png
├── market/         # Market interface
│   ├── in_market.png
│   ├── new_offer.png
│   └── sold.png
├── offer/          # Offer creation
│   ├── wheat_offer.png
│   └── create_offer.png
└── advert/         # Advertisement
    └── paper_button.png
```

### Adding Custom Templates

1. **Capture Screenshots**: Use bot's screenshot feature
2. **Extract Elements**: Crop specific game elements (20-100px recommended)
3. **Save as PNG**: Use descriptive names in appropriate folders
4. **Set Thresholds**: Start with 0.75, adjust as needed
5. **Test Detection**: Use Template Manager to verify

### Template Best Practices

- **High Contrast**: Choose elements with distinct colors
- **Consistent Size**: Templates should match actual game size
- **Clean Borders**: Avoid overlapping UI elements
- **Multiple Variants**: Create templates for different game states

## 🔧 Advanced Configuration

### Configuration Files

#### `configs/default.json`
Main configuration containing:
- Field zone polygon coordinates
- Navigation decoration settings
- Tool offset positions
- Detection thresholds
- Timing parameters

#### Timing Optimization
Adjust these values for better performance:

```json
{
  "market_timing": {
    "escape_wait": 0.3,
    "market_open_wait": 0.8,
    "collection_wait": 0.2,
    "offer_page_wait": 0.8,
    "quantity_click_delay": 0.1,
    "price_set_wait": 0.3,
    "offer_create_wait": 0.8,
    "page_close_wait": 0.2,
    "verification_wait": 0.3,
    "advert_page_wait": 0.8,
    "max_verification_attempts": 2
  }
}
```

### Custom Scripts

You can extend functionality by modifying:
- `core/cycle_manager.py`: Farming logic
- `core/market_manager.py`: Market operations
- `gui/`: User interface components

### Multiple Configurations

Create multiple config files for different farms:
1. Copy `configs/default.json`
2. Rename and modify for specific farm layout
3. Load different configs via Farm Config tab

## ❓ FAQ

**Q: Which emulator should I use?**
A: Memu Play is the recommended and tested emulator. The bot is specifically designed for Memu Play with 1920x1080 resolution.

**Q: Why isn't the bot detecting game elements?**
A: The most common cause is incorrect resolution. Make sure your Memu Play emulator is set to exactly 1920x1080 resolution, as all templates are designed for this specific resolution.

**Q: Can I use this on a real Android device?**
A: The bot is designed and tested for Memu Play emulator. While technically possible, we don't recommend or support using it on physical devices.

**Q: How do I set up Memu Play correctly?**
A: Install Memu Play, set resolution to 1920x1080, use OpenGL renderer, allocate at least 2 CPU cores and 2GB RAM, then install Hay Day.

**Q: Can I use a different resolution?**
A: No, the templates are specifically designed for 1920x1080. Other resolutions will cause detection failures.

**Q: How fast is the farming cycle?**
A: Complete cycles take approximately 2-3 minutes depending on field size and emulator performance.

**Q: Can I modify the bot behavior?**
A: Yes, the code is open source and can be customized for specific needs.

**Q: What if Hay Day updates break the bot?**
A: Templates may need updating if the game UI changes. The Template Manager helps with this.

**Q: How do I backup my configuration?**
A: Copy the entire `configs/` folder to preserve your settings.

## 🤝 Contributing

We welcome contributions! To contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Areas for Contribution
- Additional template sets
- Performance optimizations
- UI improvements
- Documentation updates
- Bug fixes and testing

## ⚠️ Disclaimer

This software is provided for educational purposes only. Use of automation tools may violate game terms of service. Users assume all risks and responsibilities for their use of this software. The developers are not responsible for any consequences including but not limited to account suspension or termination.

**Use at your own risk and discretion.**

---

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Search existing issues
3. Create a new issue with detailed information
4. Include log files and configuration details

---

**Happy Farming! 🌾🚜** 