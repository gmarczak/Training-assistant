#!/usr/bin/env python3
"""
Training Assistant - AI-powered exercise form analyzer and counter
Supports live camera feed and MP4 video file analysis
"""

import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
from exercise_analyzer import ExerciseAnalyzer
from exercise_counter import ExerciseCounter
import tempfile
import os

def main():
    st.set_page_config(
        page_title="Training Assistant",
        page_icon="💪",
        layout="wide"
    )
    
    st.title("💪 Training Assistant")
    st.markdown("AI-powered exercise form analyzer and counter")
    
    # Sidebar for configuration
    st.sidebar.title("Settings")
    
    # Exercise type selection
    exercise_type = st.sidebar.selectbox(
        "Select Exercise Type",
        ["Push-ups", "Squats", "Pull-ups", "Bicep Curls"]
    )
    
    # Input method selection
    input_method = st.sidebar.radio(
        "Choose Input Method",
        ["Camera Feed", "Upload Video"]
    )
    
    # Initialize exercise analyzer and counter
    analyzer = ExerciseAnalyzer()
    counter = ExerciseCounter(exercise_type.lower().replace("-", "_"))
    
    if input_method == "Camera Feed":
        handle_camera_feed(analyzer, counter, exercise_type)
    else:
        handle_video_upload(analyzer, counter, exercise_type)

def handle_camera_feed(analyzer, counter, exercise_type):
    """Handle live camera feed analysis"""
    st.subheader("📹 Live Camera Analysis")
    
    # Camera controls
    col1, col2, col3 = st.columns(3)
    
    with col1:
        start_camera = st.button("Start Camera")
    with col2:
        stop_camera = st.button("Stop Camera")
    with col3:
        reset_count = st.button("Reset Count")
    
    # Placeholder for video feed
    video_placeholder = st.empty()
    
    # Stats display
    col1, col2, col3 = st.columns(3)
    
    with col1:
        rep_count = st.metric("Repetitions", "0")
    with col2:
        form_score = st.metric("Form Score", "0%")
    with col3:
        status = st.metric("Status", "Ready")
    
    if start_camera:
        st.info("Camera functionality requires local setup. Please use video upload for demo.")

def handle_video_upload(analyzer, counter, exercise_type):
    """Handle uploaded video file analysis"""
    st.subheader("📹 Video Upload Analysis")
    
    uploaded_file = st.file_uploader(
        "Choose a video file",
        type=['mp4', 'avi', 'mov', 'mkv']
    )
    
    if uploaded_file is not None:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_file:
            temp_file.write(uploaded_file.read())
            temp_path = temp_file.name
        
        try:
            analyze_video(temp_path, analyzer, counter, exercise_type)
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.unlink(temp_path)

def analyze_video(video_path, analyzer, counter, exercise_type):
    """Analyze uploaded video file"""
    st.subheader(f"Analyzing {exercise_type}")
    
    # Progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Results display
    col1, col2, col3 = st.columns(3)
    
    with col1:
        rep_count_display = st.empty()
    with col2:
        form_score_display = st.empty()
    with col3:
        feedback_display = st.empty()
    
    # Video analysis
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    frame_count = 0
    rep_count = 0
    form_scores = []
    
    # Video display
    video_placeholder = st.empty()
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Analyze frame
        landmarks = analyzer.detect_pose(frame)
        
        if landmarks is not None:
            # Count repetitions
            rep_count = counter.count_repetition(landmarks)
            
            # Evaluate form
            form_score = analyzer.evaluate_form(landmarks, exercise_type.lower().replace("-", "_"))
            form_scores.append(form_score)
            
            # Draw landmarks and feedback on frame
            annotated_frame = analyzer.draw_landmarks(frame, landmarks)
            
            # Display frame
            video_placeholder.image(annotated_frame, channels="BGR", use_column_width=True)
        
        # Update progress
        frame_count += 1
        progress = frame_count / total_frames
        progress_bar.progress(progress)
        status_text.text(f"Processing frame {frame_count}/{total_frames}")
        
        # Update metrics
        rep_count_display.metric("Repetitions", rep_count)
        avg_form_score = np.mean(form_scores) if form_scores else 0
        form_score_display.metric("Average Form Score", f"{avg_form_score:.1f}%")
        
        # Provide feedback
        if avg_form_score >= 80:
            feedback = "Excellent form! 🎉"
        elif avg_form_score >= 60:
            feedback = "Good form, minor improvements needed ✅"
        else:
            feedback = "Form needs improvement ⚠️"
        
        feedback_display.metric("Feedback", feedback)
    
    cap.release()
    
    # Final summary
    st.success("Analysis complete!")
    
    # Summary statistics
    st.subheader("📊 Summary Statistics")
    
    summary_col1, summary_col2, summary_col3 = st.columns(3)
    
    with summary_col1:
        st.metric("Total Repetitions", rep_count)
    with summary_col2:
        final_avg_score = np.mean(form_scores) if form_scores else 0
        st.metric("Overall Form Score", f"{final_avg_score:.1f}%")
    with summary_col3:
        if rep_count > 0:
            quality = "Excellent" if final_avg_score >= 80 else "Good" if final_avg_score >= 60 else "Needs Improvement"
            st.metric("Session Quality", quality)
    
    # Recommendations
    st.subheader("💡 Recommendations")
    if final_avg_score < 60:
        st.warning("Focus on proper form before increasing repetitions. Consider working with a trainer.")
    elif final_avg_score < 80:
        st.info("Good work! Pay attention to maintaining consistent form throughout the exercise.")
    else:
        st.success("Excellent form! You can consider increasing the difficulty or adding more repetitions.")

if __name__ == "__main__":
    main()