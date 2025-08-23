#!/bin/bash
# Setup script for Shutdown Reminder Application

echo "🔧 Setting up Shutdown Reminder Application..."

# Check Python version
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | cut -d ' ' -f 2)
    echo "✅ Found Python: $PYTHON_VERSION"
else
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

# Check if we're on a supported platform
OS=$(uname -s)
case $OS in
    Linux*)     PLATFORM="Linux";;
    Darwin*)    PLATFORM="macOS";;
    CYGWIN*|MINGW*) PLATFORM="Windows";;
    *)          PLATFORM="Unknown";;
esac

echo "✅ Detected platform: $PLATFORM"

# Check for GUI support
if python3 -c "import tkinter" 2>/dev/null; then
    echo "✅ GUI support (tkinter) available"
    GUI_AVAILABLE=true
else
    echo "⚠️  GUI support (tkinter) not available, will use CLI version"
    GUI_AVAILABLE=false
    
    if [ "$PLATFORM" = "Linux" ]; then
        echo "💡 To enable GUI on Linux, install: sudo apt-get install python3-tk"
    fi
fi

# Make scripts executable
chmod +x shutdown_reminder.py shutdown_reminder_cli.py

echo "✅ Scripts are now executable"

# Run basic tests
echo "🧪 Running basic tests..."
if python3 test_shutdown_reminder.py; then
    echo "✅ Tests completed"
else
    echo "⚠️  Some tests failed, but this may be expected in some environments"
fi

# Show usage instructions
echo ""
echo "🎉 Setup complete!"
echo ""
echo "Usage options:"
echo "─────────────"

if [ "$GUI_AVAILABLE" = true ]; then
    echo "🖥️  GUI version (recommended):"
    echo "   python3 shutdown_reminder.py"
    echo ""
fi

echo "💻 CLI version:"
echo "   python3 shutdown_reminder_cli.py"
echo "   python3 shutdown_reminder_cli.py --help"
echo ""

if [ "$PLATFORM" = "Linux" ] || [ "$PLATFORM" = "macOS" ]; then
    echo "⚠️  Note: Shutdown commands may require sudo privileges"
fi

echo "📚 For more information, see README.md"