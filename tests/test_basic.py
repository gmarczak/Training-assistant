"""
Basic tests for the Training Assistant application.
"""

import unittest
import sys
import os
from datetime import datetime

# Add src to path for testing
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from training_assistant.exercises.exercise_library import ExerciseLibrary


class TestExerciseLibrary(unittest.TestCase):
    """Test the exercise library functionality."""
    
    def setUp(self):
        self.library = ExerciseLibrary()
    
    def test_get_exercise(self):
        """Test getting exercise configurations."""
        pushups = self.library.get_exercise("pushups")
        self.assertIsNotNone(pushups)
        self.assertEqual(pushups.name, "pushups")
        self.assertEqual(pushups.display_name, "Push-ups")
    
    def test_validate_exercise_name(self):
        """Test exercise name validation."""
        self.assertTrue(self.library.validate_exercise_name("pushups"))
        self.assertTrue(self.library.validate_exercise_name("squats"))
        self.assertFalse(self.library.validate_exercise_name("invalid_exercise"))
    
    def test_get_exercises_by_difficulty(self):
        """Test filtering exercises by difficulty."""
        beginner = self.library.get_exercises_by_difficulty("beginner")
        self.assertIn("pushups", beginner)
        self.assertIn("squats", beginner)
        
        intermediate = self.library.get_exercises_by_difficulty("intermediate")
        self.assertIn("pullups", intermediate)


class TestBasicStructure(unittest.TestCase):
    """Test basic project structure."""
    
    def test_project_structure(self):
        """Test that basic project structure exists."""
        base_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'training_assistant')
        
        # Check that main modules exist
        self.assertTrue(os.path.exists(os.path.join(base_path, '__init__.py')))
        self.assertTrue(os.path.exists(os.path.join(base_path, 'app.py')))
        self.assertTrue(os.path.exists(os.path.join(base_path, 'core')))
        self.assertTrue(os.path.exists(os.path.join(base_path, 'exercises')))
        self.assertTrue(os.path.exists(os.path.join(base_path, 'data')))
        self.assertTrue(os.path.exists(os.path.join(base_path, 'ui')))


if __name__ == '__main__':
    unittest.main()