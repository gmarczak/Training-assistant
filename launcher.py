#!/usr/bin/env python3
"""
Simple launcher script for the Training Assistant
Provides multiple ways to run the application
"""

import sys
import subprocess
import os

def check_dependencies():
    """Check if all required dependencies are installed"""
    try:
        import cv2
        import mediapipe
        import streamlit
        import numpy
        import matplotlib
        import PIL
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def launch_streamlit():
    """Launch the Streamlit web application"""
    print("🚀 Launching Training Assistant Web App...")
    print("This will open in your web browser at http://localhost:8501")
    print("Press Ctrl+C to stop the server")
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "main.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Training Assistant stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start Streamlit: {e}")

def launch_demo():
    """Launch the simple demo script"""
    print("🎬 Launching Training Assistant Demo...")
    print("Press 'q' to quit, 'r' to reset count")
    
    try:
        subprocess.run([sys.executable, "demo.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Demo stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start demo: {e}")

def run_tests():
    """Run functionality tests"""
    print("🧪 Running functionality tests...")
    
    try:
        result = subprocess.run([sys.executable, "test_functionality.py"], check=True)
        print("✅ All tests completed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Tests failed: {e}")

def show_help():
    """Show help information"""
    print("""
💪 Training Assistant Launcher

Usage: python launcher.py [option]

Options:
  web, streamlit    Launch web application (recommended)
  demo             Launch simple camera demo
  test             Run functionality tests
  help             Show this help message

Examples:
  python launcher.py web        # Launch web app
  python launcher.py demo       # Launch camera demo
  python launcher.py test       # Run tests
  
For video analysis:
  python demo.py path/to/video.mp4

Requirements:
  - Python 3.8+
  - Webcam (for live analysis)
  - Install dependencies: pip install -r requirements.txt
""")

def main():
    """Main launcher function"""
    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Check dependencies first
    if not check_dependencies():
        return
    
    # Parse command line arguments
    if len(sys.argv) < 2:
        # Default action
        print("💪 Training Assistant")
        print("Select launch option:")
        print("1. Web Application (recommended)")
        print("2. Simple Demo")
        print("3. Run Tests")
        print("4. Help")
        
        try:
            choice = input("\nEnter choice (1-4): ").strip()
            
            if choice == "1":
                launch_streamlit()
            elif choice == "2":
                launch_demo()
            elif choice == "3":
                run_tests()
            elif choice == "4":
                show_help()
            else:
                print("Invalid choice")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
        
        return
    
    option = sys.argv[1].lower()
    
    if option in ["web", "streamlit"]:
        launch_streamlit()
    elif option == "demo":
        launch_demo()
    elif option == "test":
        run_tests()
    elif option == "help":
        show_help()
    else:
        print(f"Unknown option: {option}")
        show_help()

if __name__ == "__main__":
    main()