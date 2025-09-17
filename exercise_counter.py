"""
Exercise Counter - Module for counting exercise repetitions
Uses pose landmarks to detect movement patterns and count reps
"""

import numpy as np
import mediapipe as mp
from collections import deque

class ExerciseCounter:
    def __init__(self, exercise_type):
        """
        Initialize exercise counter
        
        Args:
            exercise_type: Type of exercise (push_ups, squats, etc.)
        """
        self.exercise_type = exercise_type
        self.rep_count = 0
        self.position_state = "unknown"  # up, down, transition
        self.movement_history = deque(maxlen=10)  # Track recent movements
        self.mp_pose = mp.solutions.pose
        
        # Thresholds for different exercises
        self.thresholds = {
            "push_ups": {"up": 160, "down": 90},
            "squats": {"up": 160, "down": 90}, 
            "pull_ups": {"up": 160, "down": 90},
            "bicep_curls": {"up": 160, "down": 45}
        }
        
        # State tracking
        self.last_state = "up"
        self.state_changed = False
    
    def count_repetition(self, landmarks):
        """
        Count repetitions based on pose landmarks
        
        Args:
            landmarks: MediaPipe pose landmarks
            
        Returns:
            rep_count: Current repetition count
        """
        if not landmarks:
            return self.rep_count
        
        if self.exercise_type == "push_ups":
            return self._count_pushup_reps(landmarks)
        elif self.exercise_type == "squats":
            return self._count_squat_reps(landmarks)
        elif self.exercise_type == "pull_ups":
            return self._count_pullup_reps(landmarks)
        elif self.exercise_type == "bicep_curls":
            return self._count_bicep_curl_reps(landmarks)
        else:
            return self.rep_count
    
    def _calculate_angle(self, point1, point2, point3):
        """Calculate angle between three points"""
        # Calculate vectors
        vector1 = np.array([point1.x - point2.x, point1.y - point2.y])
        vector2 = np.array([point3.x - point2.x, point3.y - point2.y])
        
        # Calculate angle
        cosine_angle = np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))
        angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))
        
        return np.degrees(angle)
    
    def _count_pushup_reps(self, landmarks):
        """Count push-up repetitions"""
        try:
            # Get elbow landmarks
            left_shoulder = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_SHOULDER]
            left_elbow = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_ELBOW]
            left_wrist = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_WRIST]
            
            right_shoulder = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_SHOULDER]
            right_elbow = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_ELBOW]
            right_wrist = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_WRIST]
            
            # Calculate elbow angles
            left_angle = self._calculate_angle(left_shoulder, left_elbow, left_wrist)
            right_angle = self._calculate_angle(right_shoulder, right_elbow, right_wrist)
            
            # Average the angles
            avg_angle = (left_angle + right_angle) / 2
            
            # Determine position state
            current_state = "up" if avg_angle > self.thresholds["push_ups"]["up"] else "down"
            
            # Count repetition on state change from down to up
            if self.last_state == "down" and current_state == "up":
                self.rep_count += 1
            
            self.last_state = current_state
            
            return self.rep_count
            
        except Exception:
            return self.rep_count
    
    def _count_squat_reps(self, landmarks):
        """Count squat repetitions"""
        try:
            # Get knee landmarks
            left_hip = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_HIP]
            left_knee = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_KNEE]
            left_ankle = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_ANKLE]
            
            right_hip = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_HIP]
            right_knee = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_KNEE]
            right_ankle = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_ANKLE]
            
            # Calculate knee angles
            left_angle = self._calculate_angle(left_hip, left_knee, left_ankle)
            right_angle = self._calculate_angle(right_hip, right_knee, right_ankle)
            
            # Average the angles
            avg_angle = (left_angle + right_angle) / 2
            
            # Determine position state
            current_state = "up" if avg_angle > self.thresholds["squats"]["up"] else "down"
            
            # Count repetition on state change from down to up
            if self.last_state == "down" and current_state == "up":
                self.rep_count += 1
            
            self.last_state = current_state
            
            return self.rep_count
            
        except Exception:
            return self.rep_count
    
    def _count_pullup_reps(self, landmarks):
        """Count pull-up repetitions"""
        try:
            # Get arm landmarks
            left_shoulder = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_SHOULDER]
            left_elbow = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_ELBOW]
            left_wrist = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_WRIST]
            
            right_shoulder = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_SHOULDER]
            right_elbow = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_ELBOW]
            right_wrist = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_WRIST]
            
            # Calculate elbow angles
            left_angle = self._calculate_angle(left_shoulder, left_elbow, left_wrist)
            right_angle = self._calculate_angle(right_shoulder, right_elbow, right_wrist)
            
            # Average the angles
            avg_angle = (left_angle + right_angle) / 2
            
            # For pull-ups, "up" position has smaller angles (arms bent)
            current_state = "up" if avg_angle < self.thresholds["pull_ups"]["down"] else "down"
            
            # Count repetition on state change from down to up
            if self.last_state == "down" and current_state == "up":
                self.rep_count += 1
            
            self.last_state = current_state
            
            return self.rep_count
            
        except Exception:
            return self.rep_count
    
    def _count_bicep_curl_reps(self, landmarks):
        """Count bicep curl repetitions"""
        try:
            # Get arm landmarks (focusing on one arm for simplicity)
            left_shoulder = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_SHOULDER]
            left_elbow = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_ELBOW]
            left_wrist = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_WRIST]
            
            right_shoulder = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_SHOULDER]
            right_elbow = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_ELBOW]
            right_wrist = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_WRIST]
            
            # Calculate elbow angles
            left_angle = self._calculate_angle(left_shoulder, left_elbow, left_wrist)
            right_angle = self._calculate_angle(right_shoulder, right_elbow, right_wrist)
            
            # Use the arm with more pronounced movement
            avg_angle = (left_angle + right_angle) / 2
            
            # For bicep curls, "up" position has smaller angles (arms bent)
            current_state = "up" if avg_angle < self.thresholds["bicep_curls"]["down"] else "down"
            
            # Count repetition on state change from down to up
            if self.last_state == "down" and current_state == "up":
                self.rep_count += 1
            
            self.last_state = current_state
            
            return self.rep_count
            
        except Exception:
            return self.rep_count
    
    def reset_count(self):
        """Reset repetition count"""
        self.rep_count = 0
        self.last_state = "up"
        self.movement_history.clear()
    
    def get_current_state(self):
        """Get current exercise state"""
        return self.last_state
    
    def get_count(self):
        """Get current repetition count"""
        return self.rep_count