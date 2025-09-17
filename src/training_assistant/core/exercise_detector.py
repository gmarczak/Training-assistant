"""
Exercise detection and repetition counting module.
Handles the logic for detecting different exercises and counting repetitions.
"""

import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from collections import deque
import time


class RepetitionCounter:
    """Handles repetition counting for various exercises."""
    
    def __init__(self, exercise_type: str, smoothing_window: int = 5):
        """
        Initialize the repetition counter.
        
        Args:
            exercise_type: Type of exercise to count
            smoothing_window: Number of frames for smoothing calculations
        """
        self.exercise_type = exercise_type.lower()
        self.smoothing_window = smoothing_window
        self.angle_history = deque(maxlen=smoothing_window)
        self.rep_count = 0
        self.in_rep = False
        self.last_direction = None
        self.min_angle_threshold = None
        self.max_angle_threshold = None
        self.current_phase = "ready"  # ready, down, up
        self.form_feedback = []
        
        # Set exercise-specific parameters
        self._setup_exercise_parameters()
    
    def _setup_exercise_parameters(self):
        """Setup exercise-specific parameters for counting and form evaluation."""
        
        if self.exercise_type == "pushups":
            self.min_angle_threshold = 70  # Arms bent (down position)
            self.max_angle_threshold = 160  # Arms extended (up position)
            self.primary_angle = "arm"
            
        elif self.exercise_type == "squats":
            self.min_angle_threshold = 70  # Legs bent (down position)
            self.max_angle_threshold = 160  # Legs extended (up position)
            self.primary_angle = "leg"
            
        elif self.exercise_type == "pullups":
            self.min_angle_threshold = 40  # Arms bent (up position)
            self.max_angle_threshold = 160  # Arms extended (down position)
            self.primary_angle = "arm"
            
        elif self.exercise_type == "lunges":
            self.min_angle_threshold = 80  # Front leg bent
            self.max_angle_threshold = 160  # Front leg extended
            self.primary_angle = "leg"
            
        elif self.exercise_type == "bicep_curls":
            self.min_angle_threshold = 30  # Arms bent (up position)
            self.max_angle_threshold = 160  # Arms extended (down position)
            self.primary_angle = "arm"
            
        else:
            # Default parameters
            self.min_angle_threshold = 70
            self.max_angle_threshold = 160
            self.primary_angle = "arm"
    
    def get_primary_angle(self, angles: Dict[str, float]) -> Optional[float]:
        """
        Get the primary angle for the current exercise.
        
        Args:
            angles: Dictionary of calculated angles
            
        Returns:
            Primary angle value or None if not available
        """
        if self.primary_angle == "arm":
            # Use average of both arms if available
            left_arm = angles.get('left_arm')
            right_arm = angles.get('right_arm')
            
            if left_arm is not None and right_arm is not None:
                return (left_arm + right_arm) / 2
            elif left_arm is not None:
                return left_arm
            elif right_arm is not None:
                return right_arm
                
        elif self.primary_angle == "leg":
            # Use average of both legs if available
            left_leg = angles.get('left_leg')
            right_leg = angles.get('right_leg')
            
            if left_leg is not None and right_leg is not None:
                return (left_leg + right_leg) / 2
            elif left_leg is not None:
                return left_leg
            elif right_leg is not None:
                return right_leg
        
        return None
    
    def smooth_angle(self, angle: float) -> float:
        """
        Apply smoothing to reduce noise in angle measurements.
        
        Args:
            angle: Current angle measurement
            
        Returns:
            Smoothed angle value
        """
        self.angle_history.append(angle)
        return np.mean(list(self.angle_history))
    
    def update(self, angles: Dict[str, float]) -> Dict[str, Any]:
        """
        Update the repetition counter with new angle measurements.
        
        Args:
            angles: Dictionary of current angle measurements
            
        Returns:
            Dictionary containing count updates and feedback
        """
        primary_angle = self.get_primary_angle(angles)
        
        if primary_angle is None:
            return {
                'rep_count': self.rep_count,
                'current_phase': self.current_phase,
                'form_feedback': ["Unable to detect pose"],
                'angle': None
            }
        
        # Smooth the angle
        smoothed_angle = self.smooth_angle(primary_angle)
        
        # Update repetition count based on exercise type
        rep_detected = self._detect_repetition(smoothed_angle)
        
        # Generate form feedback
        form_feedback = self._evaluate_form(angles, smoothed_angle)
        
        return {
            'rep_count': self.rep_count,
            'current_phase': self.current_phase,
            'form_feedback': form_feedback,
            'angle': smoothed_angle,
            'rep_detected': rep_detected
        }
    
    def _detect_repetition(self, angle: float) -> bool:
        """
        Detect if a repetition has been completed.
        
        Args:
            angle: Current smoothed angle
            
        Returns:
            True if a repetition was detected
        """
        rep_detected = False
        
        # State machine for repetition counting
        if self.exercise_type in ["pushups", "squats", "lunges"]:
            # Down-up movement pattern
            if self.current_phase == "ready":
                if angle < self.min_angle_threshold:
                    self.current_phase = "down"
            elif self.current_phase == "down":
                if angle > self.max_angle_threshold:
                    self.current_phase = "up"
                    self.rep_count += 1
                    rep_detected = True
                    self.current_phase = "ready"
                    
        elif self.exercise_type in ["pullups", "bicep_curls"]:
            # Up-down movement pattern
            if self.current_phase == "ready":
                if angle < self.min_angle_threshold:
                    self.current_phase = "up"
            elif self.current_phase == "up":
                if angle > self.max_angle_threshold:
                    self.current_phase = "down"
                    self.rep_count += 1
                    rep_detected = True
                    self.current_phase = "ready"
        
        return rep_detected
    
    def _evaluate_form(self, angles: Dict[str, float], primary_angle: float) -> List[str]:
        """
        Evaluate exercise form and provide feedback.
        
        Args:
            angles: All calculated angles
            primary_angle: Primary angle for the exercise
            
        Returns:
            List of form feedback messages
        """
        feedback = []
        
        if self.exercise_type == "pushups":
            feedback.extend(self._evaluate_pushup_form(angles, primary_angle))
        elif self.exercise_type == "squats":
            feedback.extend(self._evaluate_squat_form(angles, primary_angle))
        elif self.exercise_type == "pullups":
            feedback.extend(self._evaluate_pullup_form(angles, primary_angle))
        else:
            # Generic feedback
            if self.current_phase == "down" and primary_angle > self.min_angle_threshold + 20:
                feedback.append("Go deeper")
            elif self.current_phase == "up" and primary_angle < self.max_angle_threshold - 20:
                feedback.append("Full extension")
        
        if not feedback:
            if self.current_phase == "ready":
                feedback.append("Good form! Ready for next rep")
            else:
                feedback.append("Keep going!")
        
        return feedback
    
    def _evaluate_pushup_form(self, angles: Dict[str, float], primary_angle: float) -> List[str]:
        """Evaluate pushup-specific form."""
        feedback = []
        
        # Check arm symmetry
        left_arm = angles.get('left_arm')
        right_arm = angles.get('right_arm')
        
        if left_arm and right_arm and abs(left_arm - right_arm) > 15:
            feedback.append("Keep arms symmetric")
        
        # Check depth
        if self.current_phase == "down" and primary_angle > 90:
            feedback.append("Go lower - chest to ground")
        
        return feedback
    
    def _evaluate_squat_form(self, angles: Dict[str, float], primary_angle: float) -> List[str]:
        """Evaluate squat-specific form."""
        feedback = []
        
        # Check depth
        if self.current_phase == "down" and primary_angle > 90:
            feedback.append("Squat deeper - thighs parallel to ground")
        
        # Check leg symmetry
        left_leg = angles.get('left_leg')
        right_leg = angles.get('right_leg')
        
        if left_leg and right_leg and abs(left_leg - right_leg) > 20:
            feedback.append("Balance both legs evenly")
        
        return feedback
    
    def _evaluate_pullup_form(self, angles: Dict[str, float], primary_angle: float) -> List[str]:
        """Evaluate pullup-specific form."""
        feedback = []
        
        # Check if arms are fully extended at bottom
        if self.current_phase == "ready" and primary_angle < 150:
            feedback.append("Full arm extension at bottom")
        
        # Check if chin goes over bar (approximated by arm angle)
        if self.current_phase == "up" and primary_angle > 50:
            feedback.append("Pull chin over the bar")
        
        return feedback
    
    def reset(self):
        """Reset the repetition counter."""
        self.rep_count = 0
        self.current_phase = "ready"
        self.angle_history.clear()
        self.form_feedback = []