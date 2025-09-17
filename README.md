# 💪 Training Assistant

An AI-powered exercise form analyzer and repetition counter that uses computer vision to help you improve your workout technique. The app can analyze exercises through live camera feed or uploaded MP4 video files, providing real-time feedback on form and automatically counting repetitions.

## 🌟 Features

- **Real-time pose detection** using MediaPipe
- **Automatic repetition counting** for multiple exercise types
- **Form evaluation and scoring** with detailed feedback
- **Support for multiple exercises**: Push-ups, Squats, Pull-ups, Bicep Curls
- **Camera and video file input** for flexible usage
- **Interactive web interface** built with Streamlit
- **Real-time feedback** on exercise technique

## 🎯 Supported Exercises

1. **Push-ups** - Analyzes arm angles, body alignment, and wrist positioning
2. **Squats** - Evaluates knee angles, hip-knee alignment, and back posture
3. **Pull-ups** - Monitors arm symmetry and body stability
4. **Bicep Curls** - Tracks elbow positioning and movement symmetry

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Webcam (for live analysis)
- MP4 video files (for video analysis)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/gmarczak/Training-assistant.git
cd Training-assistant
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Usage

#### Web Interface (Recommended)

Launch the Streamlit web app:
```bash
streamlit run main.py
```

This will open a web browser with the Training Assistant interface where you can:
- Select exercise type
- Choose between camera feed or video upload
- View real-time analysis and feedback

#### Command Line Demo

For basic testing, you can use the demo script:

**With camera:**
```bash
python demo.py
```

**With video file:**
```bash
python demo.py path/to/your/video.mp4
```

**Demo controls:**
- Press 'q' to quit
- Press 'r' to reset repetition count

## 📁 Project Structure

```
Training-assistant/
├── main.py                 # Streamlit web application
├── exercise_analyzer.py    # Core pose detection and form evaluation
├── exercise_counter.py     # Repetition counting logic
├── demo.py                # Simple command-line demo
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🔧 How It Works

### 1. Pose Detection
- Uses MediaPipe to detect 33 key body landmarks
- Tracks joint positions and movements in real-time
- Works with various camera angles and lighting conditions

### 2. Exercise Recognition
- Calculates angles between key joints (elbows, knees, hips)
- Identifies exercise phases (up/down positions)
- Tracks movement patterns specific to each exercise type

### 3. Form Evaluation
- Analyzes joint angles and body alignment
- Compares against ideal form parameters
- Provides percentage-based scoring (0-100%)

### 4. Repetition Counting
- Detects state changes between exercise phases
- Counts complete repetitions automatically
- Prevents double-counting with state tracking

## 📊 Form Evaluation Criteria

### Push-ups
- ✅ Proper arm angles (around 90° when lowered)
- ✅ Straight body alignment from head to feet
- ✅ Wrists positioned under shoulders
- ❌ Penalties for poor form reduce score

### Squats
- ✅ Knee angles (60-120° range)
- ✅ Knees tracking over toes
- ✅ Upright torso posture
- ❌ Penalties for knee cave-in or excessive forward lean

### Pull-ups
- ✅ Symmetric arm movement
- ✅ Minimal body swing
- ✅ Full range of motion
- ❌ Penalties for asymmetry or excessive momentum

### Bicep Curls
- ✅ Elbows close to body
- ✅ Symmetric movement between arms
- ✅ Controlled motion
- ❌ Penalties for elbow movement or asymmetry

## 🎨 Web Interface Features

- **Exercise Selection**: Choose from supported exercise types
- **Input Method**: Switch between live camera and video upload
- **Real-time Metrics**: See repetition count, form score, and status
- **Visual Feedback**: Pose landmarks overlaid on video feed
- **Session Summary**: Complete analysis with recommendations

## 🛠️ Technical Details

### Dependencies
- **OpenCV**: Video processing and display
- **MediaPipe**: Pose detection and landmark tracking
- **NumPy**: Mathematical calculations
- **Streamlit**: Web interface framework
- **Pillow**: Image processing
- **Matplotlib**: Data visualization

### Performance
- Runs at 30+ FPS on modern hardware
- Optimized for real-time analysis
- Lightweight pose detection model
- Efficient angle calculations

## 🔮 Future Enhancements

- [ ] Additional exercise types (planks, lunges, etc.)
- [ ] Advanced form analysis with detailed tips
- [ ] Workout session tracking and history
- [ ] Custom exercise parameter tuning
- [ ] Mobile app version
- [ ] Integration with fitness trackers
- [ ] Multi-person analysis
- [ ] 3D pose estimation

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🐛 Troubleshooting

### Common Issues

**Camera not working:**
- Ensure your webcam is connected and not used by another application
- Check camera permissions in your browser/system settings

**Low frame rate:**
- Close other applications using the camera
- Reduce video resolution if possible
- Ensure adequate lighting for better pose detection

**Inaccurate counting:**
- Ensure proper lighting and camera positioning
- Perform exercises within camera view
- Maintain consistent movement patterns

**Form score seems incorrect:**
- Check that the correct exercise type is selected
- Ensure clear view of key body parts for the exercise
- Calibrate your setup for optimal angle

## 📞 Support

If you encounter any issues or have questions, please:
1. Check the troubleshooting section above
2. Open an issue on GitHub
3. Provide details about your setup and the problem

---

**Made with ❤️ for the fitness community**