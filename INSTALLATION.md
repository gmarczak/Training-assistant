# Training Assistant - Installation & Usage Guide

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Webcam (for live training) or MP4 video files
- 2GB+ RAM recommended

### Installation

1. **Clone the Repository**
```bash
git clone https://github.com/gmarczak/Training-assistant.git
cd Training-assistant
```

2. **Automatic Setup** (Recommended)
```bash
chmod +x setup.sh
./setup.sh
```

3. **Manual Setup**
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create data directories
mkdir -p data/sessions data/videos data/exports
```

### Running the Application

```bash
# Activate virtual environment (if not already active)
source venv/bin/activate

# Start the application
streamlit run src/training_assistant/app.py
```

The application will open in your web browser at `http://localhost:8501`

## 🏋️ How to Use

### 1. Starting a Workout

1. **Select Exercise Type** from the sidebar:
   - Push-ups
   - Squats
   - Pull-ups
   - Lunges
   - Bicep Curls
   - Shoulder Press
   - Planks

2. **Choose Input Source**:
   - **Camera**: Real-time workout with webcam
   - **Upload Video**: Analyze pre-recorded MP4 files

3. **Click "Start Workout"** to begin

### 2. During Your Workout

- **Real-time Feedback**: See your form analysis on screen
- **Rep Counting**: Automatic repetition counting
- **Form Tips**: Get instant feedback on your technique
- **Progress Tracking**: Watch your reps accumulate

### 3. After Your Workout

- **Session Summary**: View your completed reps and duration
- **Analytics**: Check your progress over time
- **Exercise History**: Review past workout sessions

## 📊 Features Overview

### Core Features

#### Exercise Detection
- **Pose Estimation**: Uses MediaPipe for accurate body tracking
- **Rep Counting**: Smart algorithm detects complete repetitions
- **Form Analysis**: Real-time feedback on exercise technique

#### Supported Exercises
| Exercise | Difficulty | Primary Muscles |
|----------|------------|-----------------|
| Push-ups | Beginner | Chest, Shoulders, Triceps |
| Squats | Beginner | Quadriceps, Glutes, Hamstrings |
| Pull-ups | Intermediate | Back, Biceps, Rear Deltoids |
| Lunges | Beginner | Quadriceps, Glutes, Calves |
| Bicep Curls | Beginner | Biceps |
| Shoulder Press | Intermediate | Shoulders, Triceps |
| Planks | Beginner | Core, Shoulders |

#### Analytics Dashboard
- **Session History**: Track all your workouts
- **Progress Charts**: Visual progress over time
- **Exercise Statistics**: Detailed breakdown by exercise type
- **Performance Metrics**: Reps, duration, form scores

### Input Methods

#### Live Camera Feed
- Real-time pose detection
- Instant feedback during exercise
- Perfect for live training sessions

#### MP4 Video Analysis
- Upload pre-recorded workout videos
- Analyze technique after training
- Great for form review and improvement

## 🎯 Exercise Instructions

### Push-ups
1. Start in plank position with arms extended
2. Lower your body by bending your arms
3. Go down until chest nearly touches ground
4. Push back up to starting position
5. Keep your back straight throughout

**Form Tips:**
- Keep arms symmetric
- Maintain straight back
- Full range of motion

### Squats
1. Stand with feet shoulder-width apart
2. Lower your body by bending your knees
3. Go down until thighs are parallel to ground
4. Push through heels to return to standing
5. Keep your chest up and back straight

**Form Tips:**
- Knees track over toes
- Weight on heels
- Chest up, core engaged

### Pull-ups
1. Hang from pull-up bar with arms fully extended
2. Pull your body up until chin goes over the bar
3. Lower yourself back to full arm extension
4. Avoid swinging or using momentum
5. Engage your core throughout the movement

**Form Tips:**
- Full arm extension at bottom
- Chin over bar at top
- Controlled movement

## 📈 Analytics & Progress Tracking

### Dashboard Features
- **Today's Activity**: Quick overview of current day
- **Recent Sessions**: Last completed workouts
- **Progress Insights**: Personalized recommendations
- **Exercise Statistics**: Detailed performance metrics

### Analytics Views
- **Workout Frequency**: Training consistency over time
- **Progress Charts**: Rep counts and improvements
- **Exercise Breakdown**: Performance by exercise type
- **Session Duration**: Time analysis

## 🔧 Troubleshooting

### Common Issues

#### Camera Not Working
- Check camera permissions in browser
- Ensure no other applications are using the camera
- Try refreshing the page

#### Pose Detection Problems
- Ensure good lighting
- Stand in full view of camera
- Wear contrasting clothing
- Remove background clutter

#### Performance Issues
- Close unnecessary browser tabs
- Reduce video resolution if possible
- Ensure stable internet connection

#### Dependencies Issues
```bash
# Reinstall dependencies
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

### Supported Browsers
- Chrome (Recommended)
- Firefox
- Safari
- Edge

## 🛠️ Advanced Configuration

### Settings Customization
- **Detection Confidence**: Adjust pose detection sensitivity
- **Tracking Confidence**: Modify tracking stability
- **Form Feedback**: Customize feedback sensitivity

### Database Management
- **Export Data**: Save workout sessions
- **Clear History**: Reset all data
- **Backup**: Manual data backup options

## 📱 Tips for Best Results

### Camera Setup
- **Position**: Place camera at chest level
- **Distance**: Stand 6-8 feet from camera
- **Lighting**: Ensure even, bright lighting
- **Background**: Use plain, uncluttered background

### Exercise Performance
- **Clothing**: Wear fitted, contrasting clothes
- **Space**: Ensure adequate room for movement
- **Warm-up**: Always warm up before intense exercises
- **Form First**: Focus on proper form over speed

### Progress Tracking
- **Consistency**: Regular workout sessions
- **Variety**: Try different exercises
- **Goals**: Set achievable targets
- **Review**: Check analytics regularly

## 🤝 Support & Contributing

### Getting Help
- Check this documentation first
- Review troubleshooting section
- Open an issue on GitHub for bugs

### Contributing
- Fork the repository
- Create a feature branch
- Submit pull requests
- Follow coding standards

## 📄 License

MIT License - see LICENSE file for details.

---

**Happy Training! 🏋️‍♀️🏋️‍♂️**