# Training Assistant

A comprehensive gym training assistant that uses computer vision to count exercise repetitions and evaluate technique in real-time using your camera or MP4 video files.

## Features

- **Real-time Exercise Recognition**: Uses MediaPipe pose estimation to detect and track exercises
- **Repetition Counting**: Automatically counts reps for various exercises
- **Technique Evaluation**: Provides feedback on exercise form and technique
- **Multi-input Support**: Works with live camera feed or MP4 video files
- **Exercise Library**: Pre-configured templates for common gym exercises
- **Progress Tracking**: Session history and analytics
- **User-friendly Interface**: Clean Streamlit-based web interface

## Supported Exercises

- Push-ups
- Squats
- Pull-ups/Chin-ups
- Lunges
- Planks
- Bicep Curls
- Shoulder Press

## Installation

1. Clone the repository:
```bash
git clone https://github.com/gmarczak/Training-assistant.git
cd Training-assistant
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run src/training_assistant/app.py
```

## Usage

1. **Select Exercise Type**: Choose from the available exercise templates
2. **Choose Input Source**: 
   - Use live camera feed for real-time training
   - Upload MP4 file for analysis
3. **Start Training**: Begin your workout and get real-time feedback
4. **Review Results**: Check your session statistics and form analysis

## Project Structure

```
Training-assistant/
├── src/training_assistant/
│   ├── core/           # Core computer vision and ML modules
│   ├── exercises/      # Exercise-specific logic and templates
│   ├── ui/            # User interface components
│   ├── data/          # Data models and storage
│   └── utils/         # Utility functions
├── data/              # Data storage (sessions, videos, exports)
├── tests/             # Unit tests
└── static/            # Static assets
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

MIT License - see LICENSE file for details.