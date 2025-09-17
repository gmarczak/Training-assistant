"""
Main Streamlit application for the Training Assistant.
"""

import streamlit as st
import cv2
import numpy as np
from datetime import datetime, timedelta
import time
import os
import sys

# Add the src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from training_assistant.core.pose_estimation import PoseEstimator
from training_assistant.core.exercise_detector import RepetitionCounter
from training_assistant.core.video_processor import VideoProcessor, FrameProcessor, create_temp_video_file
from training_assistant.exercises.exercise_library import ExerciseLibrary
from training_assistant.data.models import WorkoutDatabase, WorkoutSession
from training_assistant.ui.dashboard import create_dashboard
from training_assistant.ui.analytics import create_analytics_view


def init_session_state():
    """Initialize Streamlit session state variables."""
    if 'workout_active' not in st.session_state:
        st.session_state.workout_active = False
    if 'current_session' not in st.session_state:
        st.session_state.current_session = None
    if 'pose_estimator' not in st.session_state:
        st.session_state.pose_estimator = PoseEstimator()
    if 'video_processor' not in st.session_state:
        st.session_state.video_processor = VideoProcessor()
    if 'exercise_library' not in st.session_state:
        st.session_state.exercise_library = ExerciseLibrary()
    if 'database' not in st.session_state:
        st.session_state.database = WorkoutDatabase()
    if 'rep_counter' not in st.session_state:
        st.session_state.rep_counter = None


def create_sidebar():
    """Create the application sidebar."""
    st.sidebar.title("🏋️ Training Assistant")
    
    # Navigation
    page = st.sidebar.selectbox(
        "Navigate",
        ["Workout", "Analytics", "Exercise Library", "Settings"]
    )
    
    st.sidebar.markdown("---")
    
    # Exercise selection
    exercise_library = st.session_state.exercise_library
    exercises = exercise_library.get_all_exercises()
    
    selected_exercise = st.sidebar.selectbox(
        "Select Exercise",
        options=list(exercises.keys()),
        format_func=lambda x: exercises[x].display_name
    )
    
    # Input source selection
    input_source = st.sidebar.radio(
        "Input Source",
        ["Camera", "Upload Video"]
    )
    
    st.sidebar.markdown("---")
    
    # Workout controls
    if not st.session_state.workout_active:
        if st.sidebar.button("Start Workout", type="primary"):
            start_workout(selected_exercise, input_source.lower())
    else:
        if st.sidebar.button("Stop Workout", type="secondary"):
            stop_workout()
        
        # Show current workout info
        if st.session_state.current_session:
            session = st.session_state.current_session
            st.sidebar.markdown(f"**Exercise:** {session.exercise_type.title()}")
            st.sidebar.markdown(f"**Reps:** {session.total_reps}")
            if session.start_time:
                duration = datetime.now() - session.start_time
                minutes = int(duration.total_seconds() // 60)
                seconds = int(duration.total_seconds() % 60)
                st.sidebar.markdown(f"**Duration:** {minutes:02d}:{seconds:02d}")
    
    return page, selected_exercise, input_source


def start_workout(exercise_type: str, input_source: str):
    """Start a new workout session."""
    try:
        # Initialize workout session
        session = WorkoutSession(
            exercise_type=exercise_type,
            start_time=datetime.now(),
            input_source=input_source
        )
        
        # Initialize repetition counter
        rep_counter = RepetitionCounter(exercise_type)
        
        # Setup video source
        video_processor = st.session_state.video_processor
        
        if input_source == "camera":
            if not video_processor.open_camera():
                st.error("Failed to open camera. Please check your camera connection.")
                return False
        
        # Update session state
        st.session_state.current_session = session
        st.session_state.rep_counter = rep_counter
        st.session_state.workout_active = True
        
        st.success(f"Started {exercise_type.title()} workout!")
        return True
        
    except Exception as e:
        st.error(f"Failed to start workout: {str(e)}")
        return False


def stop_workout():
    """Stop the current workout session."""
    try:
        if st.session_state.current_session and st.session_state.rep_counter:
            # Finalize session
            session = st.session_state.current_session
            session.end_time = datetime.now()
            session.total_reps = st.session_state.rep_counter.rep_count
            
            if session.start_time and session.end_time:
                session.duration_seconds = (session.end_time - session.start_time).total_seconds()
            
            # Save session to database
            database = st.session_state.database
            session_id = database.save_session(session)
            
            # Cleanup
            st.session_state.video_processor.close()
            st.session_state.workout_active = False
            st.session_state.current_session = None
            st.session_state.rep_counter = None
            
            st.success(f"Workout completed! {session.total_reps} reps in {session.duration_seconds:.1f} seconds")
        
    except Exception as e:
        st.error(f"Error stopping workout: {str(e)}")


def workout_page():
    """Main workout page."""
    st.title("🏋️ Training Assistant")
    
    if not st.session_state.workout_active:
        st.info("Select an exercise and input source from the sidebar to start your workout.")
        
        # Show exercise library preview
        exercise_library = st.session_state.exercise_library
        exercises = exercise_library.get_all_exercises()
        
        st.subheader("Available Exercises")
        
        cols = st.columns(3)
        for idx, (name, config) in enumerate(exercises.items()):
            with cols[idx % 3]:
                with st.container():
                    st.markdown(f"**{config.display_name}**")
                    st.markdown(f"*{config.difficulty_level.title()}*")
                    st.markdown(f"{config.description}")
                    st.markdown(f"**Targets:** {', '.join(config.primary_muscle_groups)}")
                    
                    with st.expander("Instructions"):
                        for instruction in config.instructions:
                            st.markdown(f"• {instruction}")
    else:
        # Active workout interface
        workout_interface()


def workout_interface():
    """Interface for active workout session."""
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Video feed area
        video_placeholder = st.empty()
        
        # Check if using uploaded video
        if st.session_state.current_session.input_source == "upload video":
            uploaded_file = st.file_uploader(
                "Upload MP4 video",
                type=['mp4', 'avi', 'mov'],
                key="video_upload"
            )
            
            if uploaded_file is not None:
                # Create temporary file and process
                temp_file_path = create_temp_video_file(uploaded_file)
                if st.session_state.video_processor.open_video_file(temp_file_path):
                    process_video_file(video_placeholder, temp_file_path)
                else:
                    st.error("Failed to process uploaded video file.")
        else:
            # Live camera feed
            process_camera_feed(video_placeholder)
    
    with col2:
        # Workout stats and feedback
        display_workout_stats()


def process_camera_feed(video_placeholder):
    """Process live camera feed."""
    pose_estimator = st.session_state.pose_estimator
    rep_counter = st.session_state.rep_counter
    video_processor = st.session_state.video_processor
    
    # Get frame from camera
    frame = video_processor.get_frame()
    
    if frame is not None:
        # Resize frame for processing
        processed_frame = FrameProcessor.resize_frame(frame, target_width=640)
        
        # Enhance frame quality
        enhanced_frame = FrameProcessor.enhance_frame(processed_frame)
        
        # Detect pose
        pose_data = pose_estimator.detect_pose(enhanced_frame)
        
        if pose_data:
            # Draw pose landmarks
            enhanced_frame = pose_estimator.draw_landmarks(enhanced_frame, pose_data)
            
            # Calculate angles and update rep counter
            angles = pose_estimator.get_key_angles(pose_data)
            rep_update = rep_counter.update(angles)
            
            # Update session stats
            if rep_update['rep_detected']:
                st.session_state.current_session.total_reps = rep_counter.rep_count
            
            # Add overlay information
            enhanced_frame = FrameProcessor.add_info_overlay(
                enhanced_frame,
                rep_counter.rep_count,
                st.session_state.current_session.exercise_type,
                rep_update['current_phase'],
                rep_update['form_feedback'],
                rep_update.get('angle')
            )
        
        # Convert BGR to RGB for display
        display_frame = cv2.cvtColor(enhanced_frame, cv2.COLOR_BGR2RGB)
        video_placeholder.image(display_frame, channels="RGB", use_column_width=True)


def process_video_file(video_placeholder, file_path):
    """Process uploaded video file."""
    pose_estimator = st.session_state.pose_estimator
    rep_counter = st.session_state.rep_counter
    video_processor = st.session_state.video_processor
    
    # Progress bar for video processing
    progress_bar = st.progress(0)
    
    while True:
        frame = video_processor.get_frame()
        
        if frame is None:
            break
        
        # Update progress
        video_info = video_processor.get_frame_info()
        if 'progress' in video_info:
            progress_bar.progress(video_info['progress'])
        
        # Process frame (similar to camera feed)
        processed_frame = FrameProcessor.resize_frame(frame, target_width=640)
        enhanced_frame = FrameProcessor.enhance_frame(processed_frame)
        
        pose_data = pose_estimator.detect_pose(enhanced_frame)
        
        if pose_data:
            enhanced_frame = pose_estimator.draw_landmarks(enhanced_frame, pose_data)
            angles = pose_estimator.get_key_angles(pose_data)
            rep_update = rep_counter.update(angles)
            
            if rep_update['rep_detected']:
                st.session_state.current_session.total_reps = rep_counter.rep_count
            
            enhanced_frame = FrameProcessor.add_info_overlay(
                enhanced_frame,
                rep_counter.rep_count,
                st.session_state.current_session.exercise_type,
                rep_update['current_phase'],
                rep_update['form_feedback'],
                rep_update.get('angle')
            )
        
        # Display frame
        display_frame = cv2.cvtColor(enhanced_frame, cv2.COLOR_BGR2RGB)
        video_placeholder.image(display_frame, channels="RGB", use_column_width=True)
        
        # Small delay for video playback
        time.sleep(0.033)  # ~30 FPS
    
    # Clean up temporary file
    if os.path.exists(file_path):
        os.unlink(file_path)


def display_workout_stats():
    """Display current workout statistics."""
    if st.session_state.current_session and st.session_state.rep_counter:
        session = st.session_state.current_session
        rep_counter = st.session_state.rep_counter
        
        st.subheader("Workout Stats")
        
        # Current stats
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Reps", rep_counter.rep_count)
        
        with col2:
            if session.start_time:
                duration = datetime.now() - session.start_time
                minutes = int(duration.total_seconds() // 60)
                seconds = int(duration.total_seconds() % 60)
                st.metric("Duration", f"{minutes:02d}:{seconds:02d}")
        
        # Current phase
        st.markdown(f"**Phase:** {rep_counter.current_phase.title()}")
        
        # Form feedback
        st.subheader("Form Feedback")
        if hasattr(rep_counter, 'form_feedback') and rep_counter.form_feedback:
            for feedback in rep_counter.form_feedback:
                if any(word in feedback.lower() for word in ['good', 'ready', 'keep']):
                    st.success(feedback)
                else:
                    st.warning(feedback)
        else:
            st.info("Keep going! Maintain good form.")


def main():
    """Main application function."""
    st.set_page_config(
        page_title="Training Assistant",
        page_icon="🏋️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    init_session_state()
    
    # Create sidebar and get navigation
    page, selected_exercise, input_source = create_sidebar()
    
    # Route to different pages
    if page == "Workout":
        workout_page()
    elif page == "Analytics":
        create_analytics_view()
    elif page == "Exercise Library":
        display_exercise_library()
    elif page == "Settings":
        display_settings()


def display_exercise_library():
    """Display the exercise library page."""
    st.title("📚 Exercise Library")
    
    exercise_library = st.session_state.exercise_library
    exercises = exercise_library.get_all_exercises()
    
    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        difficulty_filter = st.selectbox(
            "Filter by Difficulty",
            ["All", "Beginner", "Intermediate", "Advanced"]
        )
    
    with col2:
        muscle_groups = set()
        for config in exercises.values():
            muscle_groups.update(config.primary_muscle_groups)
        
        muscle_filter = st.selectbox(
            "Filter by Muscle Group",
            ["All"] + sorted(list(muscle_groups))
        )
    
    # Apply filters
    filtered_exercises = exercises
    if difficulty_filter != "All":
        filtered_exercises = exercise_library.get_exercises_by_difficulty(difficulty_filter.lower())
    if muscle_filter != "All":
        filtered_exercises = exercise_library.get_exercises_by_muscle_group(muscle_filter.lower())
    
    # Display exercises
    for name, config in filtered_exercises.items():
        with st.expander(f"{config.display_name} ({config.difficulty_level.title()})"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Description:** {config.description}")
                st.markdown(f"**Primary Muscles:** {', '.join(config.primary_muscle_groups)}")
                
                st.markdown("**Instructions:**")
                for i, instruction in enumerate(config.instructions, 1):
                    st.markdown(f"{i}. {instruction}")
            
            with col2:
                st.markdown(f"**Movement Pattern:** {config.movement_pattern.replace('_', ' ').title()}")
                st.markdown(f"**Angle Range:** {config.min_angle_threshold}° - {config.max_angle_threshold}°")
                st.markdown(f"**Primary Angle:** {config.primary_angle_type.title()}")


def display_settings():
    """Display the settings page."""
    st.title("⚙️ Settings")
    
    st.subheader("Detection Settings")
    
    col1, col2 = st.columns(2)
    with col1:
        min_detection_confidence = st.slider(
            "Minimum Detection Confidence",
            min_value=0.1,
            max_value=1.0,
            value=0.5,
            step=0.1
        )
    
    with col2:
        min_tracking_confidence = st.slider(
            "Minimum Tracking Confidence",
            min_value=0.1,
            max_value=1.0,
            value=0.5,
            step=0.1
        )
    
    if st.button("Update Settings"):
        # Reinitialize pose estimator with new settings
        st.session_state.pose_estimator = PoseEstimator(
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        st.success("Settings updated successfully!")
    
    st.subheader("Data Management")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Export Session Data"):
            st.info("Export functionality coming soon!")
    
    with col2:
        if st.button("Clear All Data", type="secondary"):
            st.warning("This action cannot be undone!")


if __name__ == "__main__":
    main()