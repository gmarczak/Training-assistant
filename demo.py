#!/usr/bin/env python3
"""
Simple demo script for testing the training assistant without Streamlit
Can be used for basic testing and development
"""

import cv2
from exercise_analyzer import ExerciseAnalyzer
from exercise_counter import ExerciseCounter
import time

def demo_camera():
    """Demo with live camera feed"""
    print("Starting camera demo...")
    print("Press 'q' to quit, 'r' to reset count")
    
    # Initialize components
    analyzer = ExerciseAnalyzer()
    counter = ExerciseCounter("push_ups")  # Default to push-ups
    
    # Initialize camera
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open camera")
        return
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Flip frame horizontally for mirror effect
        frame = cv2.flip(frame, 1)
        
        # Analyze frame
        landmarks = analyzer.detect_pose(frame)
        
        if landmarks:
            # Count repetitions
            rep_count = counter.count_repetition(landmarks)
            
            # Evaluate form
            form_score = analyzer.evaluate_form(landmarks, "push_ups")
            
            # Draw landmarks
            frame = analyzer.draw_landmarks(frame, landmarks)
            
            # Add text overlay
            cv2.putText(frame, f"Reps: {rep_count}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f"Form: {form_score:.1f}%", (10, 70), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f"State: {counter.get_current_state()}", (10, 110), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Display frame
        cv2.imshow('Training Assistant Demo', frame)
        
        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('r'):
            counter.reset_count()
            print("Count reset!")
    
    cap.release()
    cv2.destroyAllWindows()

def demo_video(video_path):
    """Demo with video file"""
    print(f"Analyzing video: {video_path}")
    
    # Initialize components
    analyzer = ExerciseAnalyzer()
    counter = ExerciseCounter("push_ups")  # Default to push-ups
    
    # Initialize video capture
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return
    
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    print(f"Video info: {total_frames} frames, {fps:.2f} FPS")
    
    frame_count = 0
    form_scores = []
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_count += 1
        
        # Analyze frame
        landmarks = analyzer.detect_pose(frame)
        
        if landmarks:
            # Count repetitions
            rep_count = counter.count_repetition(landmarks)
            
            # Evaluate form
            form_score = analyzer.evaluate_form(landmarks, "push_ups")
            form_scores.append(form_score)
            
            # Draw landmarks
            frame = analyzer.draw_landmarks(frame, landmarks)
            
            # Add text overlay
            cv2.putText(frame, f"Reps: {rep_count}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f"Form: {form_score:.1f}%", (10, 70), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f"Frame: {frame_count}/{total_frames}", (10, 110), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Display frame
        cv2.imshow('Training Assistant Video Demo', frame)
        
        # Control playback speed
        if cv2.waitKey(int(1000/fps)) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    # Print summary
    print(f"\nAnalysis complete!")
    print(f"Total repetitions: {counter.get_count()}")
    if form_scores:
        avg_form_score = sum(form_scores) / len(form_scores)
        print(f"Average form score: {avg_form_score:.1f}%")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Video file provided
        video_path = sys.argv[1]
        demo_video(video_path)
    else:
        # Use camera
        demo_camera()