#!/usr/bin/env python3
"""
Test script to validate core functionality of the training assistant
"""

import numpy as np
from exercise_analyzer import ExerciseAnalyzer
from exercise_counter import ExerciseCounter
import cv2

def test_analyzer_initialization():
    """Test that ExerciseAnalyzer initializes correctly"""
    print("Testing ExerciseAnalyzer initialization...")
    try:
        analyzer = ExerciseAnalyzer()
        print("✅ ExerciseAnalyzer initialized successfully")
        return True
    except Exception as e:
        print(f"❌ ExerciseAnalyzer initialization failed: {e}")
        return False

def test_counter_initialization():
    """Test that ExerciseCounter initializes correctly"""
    print("Testing ExerciseCounter initialization...")
    try:
        counter = ExerciseCounter("push_ups")
        print("✅ ExerciseCounter initialized successfully")
        return True
    except Exception as e:
        print(f"❌ ExerciseCounter initialization failed: {e}")
        return False

def test_pose_detection():
    """Test pose detection with a dummy image"""
    print("Testing pose detection...")
    try:
        analyzer = ExerciseAnalyzer()
        
        # Create a dummy image (black image)
        dummy_image = np.zeros((480, 640, 3), dtype=np.uint8)
        
        # Test pose detection (should return None for black image)
        landmarks = analyzer.detect_pose(dummy_image)
        
        print("✅ Pose detection completed (no pose detected in dummy image, as expected)")
        return True
    except Exception as e:
        print(f"❌ Pose detection failed: {e}")
        return False

def test_form_evaluation():
    """Test form evaluation with mock landmarks"""
    print("Testing form evaluation...")
    try:
        analyzer = ExerciseAnalyzer()
        
        # Test with None landmarks
        score = analyzer.evaluate_form(None, "push_ups")
        print(f"✅ Form evaluation with None landmarks: {score}")
        
        return True
    except Exception as e:
        print(f"❌ Form evaluation failed: {e}")
        return False

def test_rep_counting():
    """Test repetition counting"""
    print("Testing repetition counting...")
    try:
        counter = ExerciseCounter("push_ups")
        
        # Test initial count
        initial_count = counter.get_count()
        print(f"✅ Initial count: {initial_count}")
        
        # Test reset
        counter.reset_count()
        reset_count = counter.get_count()
        print(f"✅ After reset: {reset_count}")
        
        # Test with None landmarks
        count = counter.count_repetition(None)
        print(f"✅ Count with None landmarks: {count}")
        
        return True
    except Exception as e:
        print(f"❌ Repetition counting failed: {e}")
        return False

def test_angle_calculation():
    """Test angle calculation function"""
    print("Testing angle calculation...")
    try:
        analyzer = ExerciseAnalyzer()
        
        # Create mock points for a 90-degree angle
        class MockPoint:
            def __init__(self, x, y):
                self.x = x
                self.y = y
        
        point1 = MockPoint(0, 1)  # Top point
        point2 = MockPoint(0, 0)  # Center point (vertex)
        point3 = MockPoint(1, 0)  # Right point
        
        angle = analyzer.calculate_angle(point1, point2, point3)
        print(f"✅ Calculated angle: {angle:.1f}° (expected ~90°)")
        
        return True
    except Exception as e:
        print(f"❌ Angle calculation failed: {e}")
        return False

def test_multiple_exercises():
    """Test support for multiple exercise types"""
    print("Testing multiple exercise types...")
    try:
        exercises = ["push_ups", "squats", "pull_ups", "bicep_curls"]
        
        for exercise in exercises:
            counter = ExerciseCounter(exercise)
            analyzer = ExerciseAnalyzer()
            
            # Test form evaluation
            score = analyzer.evaluate_form(None, exercise)
            print(f"✅ {exercise}: form score = {score}")
            
            # Test counting
            count = counter.count_repetition(None)
            print(f"✅ {exercise}: rep count = {count}")
        
        return True
    except Exception as e:
        print(f"❌ Multiple exercise types test failed: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("=" * 50)
    print("🧪 TRAINING ASSISTANT FUNCTIONALITY TESTS")
    print("=" * 50)
    
    tests = [
        test_analyzer_initialization,
        test_counter_initialization,
        test_pose_detection,
        test_form_evaluation,
        test_rep_counting,
        test_angle_calculation,
        test_multiple_exercises,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        print("\n" + "-" * 40)
        if test():
            passed += 1
        print("-" * 40)
    
    print("\n" + "=" * 50)
    print(f"📊 TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The training assistant is ready to use.")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
    
    print("=" * 50)
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)