#!/usr/bin/env python3
"""
Demo script for Training Assistant - shows core functionality without UI
"""

import sys
import os
import time
import numpy as np

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from training_assistant.exercises.exercise_library import ExerciseLibrary
from training_assistant.core.exercise_detector import RepetitionCounter
from training_assistant.data.models import WorkoutSession, WorkoutDatabase


def demo_exercise_library():
    """Demonstrate the exercise library functionality."""
    print("🏋️ Training Assistant Demo")
    print("=" * 50)
    
    print("\n📚 Exercise Library:")
    library = ExerciseLibrary()
    exercises = library.get_all_exercises()
    
    for name, config in exercises.items():
        print(f"  • {config.display_name} ({config.difficulty_level})")
        print(f"    {config.description}")
        print(f"    Muscles: {', '.join(config.primary_muscle_groups)}")
        print()


def demo_repetition_counter():
    """Demonstrate the repetition counting functionality."""
    print("🔄 Repetition Counter Demo:")
    print("-" * 30)
    
    # Simulate push-up angles
    print("Simulating push-up exercise with angle changes...")
    
    counter = RepetitionCounter("pushups")
    
    # Simulate a series of push-ups with angle changes
    angle_sequence = [
        (170, "Starting position - arms extended"),
        (160, "Slight bend"),
        (120, "Going down"),
        (80, "Bottom position"),
        (120, "Coming up"),
        (160, "Almost up"),
        (170, "Complete rep 1!"),
        (150, "Starting rep 2"),
        (90, "Down position"),
        (75, "Deeper"),
        (100, "Coming up"),
        (170, "Complete rep 2!"),
    ]
    
    for angle, description in angle_sequence:
        # Simulate both arms having similar angles
        angles = {
            'left_arm': angle + np.random.uniform(-5, 5),
            'right_arm': angle + np.random.uniform(-5, 5),
        }
        
        result = counter.update(angles)
        
        print(f"  Angle: {angle:3d}° | Reps: {result['rep_count']} | Phase: {result['current_phase']} | {description}")
        
        if result['form_feedback']:
            print(f"    💡 Feedback: {result['form_feedback'][0]}")
        
        if result.get('rep_detected'):
            print("    🎉 REP COMPLETED!")
        
        time.sleep(0.5)  # Simulate real-time
    
    print(f"\n✅ Final count: {counter.rep_count} repetitions")


def demo_workout_session():
    """Demonstrate workout session tracking."""
    print("\n📊 Workout Session Demo:")
    print("-" * 30)
    
    # Create a workout session
    session = WorkoutSession(
        exercise_type="pushups",
        total_reps=15,
        duration_seconds=120.5,
        input_source="demo"
    )
    
    print(f"Created workout session:")
    print(f"  Exercise: {session.exercise_type.title()}")
    print(f"  Reps: {session.total_reps}")
    print(f"  Duration: {session.duration_seconds:.1f} seconds")
    print(f"  Start time: {session.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Save to database
    db = WorkoutDatabase("data/demo_workouts.db")
    session_id = db.save_session(session)
    print(f"  Saved to database with ID: {session_id}")
    
    # Retrieve and show stats
    stats = db.get_exercise_stats("pushups")
    if stats:
        print(f"\n📈 Exercise Statistics:")
        print(f"  Total sessions: {stats.total_sessions}")
        print(f"  Total reps: {stats.total_reps}")
        print(f"  Average reps/session: {stats.average_reps_per_session:.1f}")
        print(f"  Best session: {stats.best_session_reps} reps")
    
    # Clean up demo database
    if os.path.exists("data/demo_workouts.db"):
        os.remove("data/demo_workouts.db")
        print("\n🧹 Demo database cleaned up")


def demo_exercise_configurations():
    """Show exercise-specific configurations."""
    print("\n⚙️ Exercise Configurations:")
    print("-" * 30)
    
    library = ExerciseLibrary()
    
    # Show detailed config for a few exercises
    for exercise_name in ["pushups", "squats", "pullups"]:
        config = library.get_exercise(exercise_name)
        print(f"\n{config.display_name}:")
        print(f"  Movement: {config.movement_pattern.replace('_', ' ').title()}")
        print(f"  Angle range: {config.min_angle_threshold}° - {config.max_angle_threshold}°")
        print(f"  Primary angle: {config.primary_angle_type.title()}")
        print(f"  Form checks: {', '.join(config.form_checks)}")


def main():
    """Run the complete demo."""
    try:
        demo_exercise_library()
        demo_repetition_counter()
        demo_workout_session()
        demo_exercise_configurations()
        
        print("\n🎉 Demo completed successfully!")
        print("\nTo run the full application:")
        print("  streamlit run src/training_assistant/app.py")
        
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")


if __name__ == "__main__":
    main()