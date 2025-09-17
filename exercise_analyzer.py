"""
Exercise Analyzer - Core module for pose detection and form evaluation
Uses MediaPipe for pose estimation and custom algorithms for form analysis
"""

import cv2
import mediapipe as mp
import numpy as np
import math

class ExerciseAnalyzer:
    def __init__(self):
        """Initialize MediaPipe pose detection"""
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            smooth_landmarks=True,
            enable_segmentation=False,
            smooth_segmentation=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
    
    def detect_pose(self, frame):
        """
        Detect pose landmarks in a frame
        
        Args:
            frame: Input image frame
            
        Returns:
            landmarks: MediaPipe pose landmarks or None if no pose detected
        """
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame
        results = self.pose.process(rgb_frame)
        
        return results.pose_landmarks if results.pose_landmarks else None
    
    def draw_landmarks(self, frame, landmarks):
        """
        Draw pose landmarks on the frame
        
        Args:
            frame: Input image frame
            landmarks: MediaPipe pose landmarks
            
        Returns:
            annotated_frame: Frame with drawn landmarks
        """
        annotated_frame = frame.copy()
        
        if landmarks:
            self.mp_drawing.draw_landmarks(
                annotated_frame,
                landmarks,
                self.mp_pose.POSE_CONNECTIONS,
                self.mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                self.mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
            )
        
        return annotated_frame
    
    def calculate_angle(self, point1, point2, point3):
        """
        Calculate angle between three points
        
        Args:
            point1, point2, point3: Points with x, y coordinates
            
        Returns:
            angle: Angle in degrees
        """
        # Calculate vectors
        vector1 = np.array([point1.x - point2.x, point1.y - point2.y])
        vector2 = np.array([point3.x - point2.x, point3.y - point2.y])
        
        # Calculate angle
        cosine_angle = np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))
        angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))
        
        return math.degrees(angle)
    
    def evaluate_form(self, landmarks, exercise_type):
        """
        Evaluate exercise form based on pose landmarks
        
        Args:
            landmarks: MediaPipe pose landmarks
            exercise_type: Type of exercise (push_ups, squats, etc.)
            
        Returns:
            form_score: Score from 0-100 indicating form quality
        """
        if not landmarks:
            return 0
        
        if exercise_type == "push_ups":
            return self._evaluate_pushup_form(landmarks)
        elif exercise_type == "squats":
            return self._evaluate_squat_form(landmarks)
        elif exercise_type == "pull_ups":
            return self._evaluate_pullup_form(landmarks)
        elif exercise_type == "bicep_curls":
            return self._evaluate_bicep_curl_form(landmarks)
        else:
            return 50  # Default score for unknown exercises
    
    def _evaluate_pushup_form(self, landmarks):
        """Evaluate push-up form"""
        try:
            # Get key landmarks
            left_shoulder = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_SHOULDER]
            right_shoulder = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_SHOULDER]
            left_elbow = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_ELBOW]
            right_elbow = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_ELBOW]
            left_wrist = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_WRIST]
            right_wrist = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_WRIST]
            left_hip = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_HIP]
            right_hip = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_HIP]
            left_knee = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_KNEE]
            right_knee = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_KNEE]
            left_ankle = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_ANKLE]
            right_ankle = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_ANKLE]
            
            score = 100
            
            # Check arm angles (should be around 90 degrees when down)
            left_arm_angle = self.calculate_angle(left_shoulder, left_elbow, left_wrist)
            right_arm_angle = self.calculate_angle(right_shoulder, right_elbow, right_wrist)
            
            # Check body alignment (should be straight line)
            left_body_angle = self.calculate_angle(left_shoulder, left_hip, left_knee)
            right_body_angle = self.calculate_angle(right_shoulder, right_hip, right_knee)
            
            # Penalize poor arm form
            if abs(left_arm_angle - 90) > 30:
                score -= 20
            if abs(right_arm_angle - 90) > 30:
                score -= 20
            
            # Penalize poor body alignment
            if abs(left_body_angle - 180) > 20:
                score -= 15
            if abs(right_body_angle - 180) > 20:
                score -= 15
            
            # Check wrist position (should be under shoulders)
            shoulder_center_x = (left_shoulder.x + right_shoulder.x) / 2
            wrist_center_x = (left_wrist.x + right_wrist.x) / 2
            
            if abs(shoulder_center_x - wrist_center_x) > 0.1:
                score -= 10
            
            return max(0, score)
            
        except Exception:
            return 50
    
    def _evaluate_squat_form(self, landmarks):
        """Evaluate squat form"""
        try:
            # Get key landmarks
            left_hip = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_HIP]
            right_hip = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_HIP]
            left_knee = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_KNEE]
            right_knee = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_KNEE]
            left_ankle = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_ANKLE]
            right_ankle = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_ANKLE]
            left_shoulder = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_SHOULDER]
            right_shoulder = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_SHOULDER]
            
            score = 100
            
            # Check knee angles (should be around 90 degrees when down)
            left_knee_angle = self.calculate_angle(left_hip, left_knee, left_ankle)
            right_knee_angle = self.calculate_angle(right_hip, right_knee, right_ankle)
            
            # Check hip-knee alignment
            left_hip_knee_alignment = abs(left_hip.x - left_knee.x)
            right_hip_knee_alignment = abs(right_hip.x - right_knee.x)
            
            # Penalize poor knee angles
            if left_knee_angle > 120 or left_knee_angle < 60:
                score -= 20
            if right_knee_angle > 120 or right_knee_angle < 60:
                score -= 20
            
            # Penalize knee cave-in
            if left_hip_knee_alignment > 0.1:
                score -= 15
            if right_hip_knee_alignment > 0.1:
                score -= 15
            
            # Check back posture (shoulders should be relatively upright)
            shoulder_center_y = (left_shoulder.y + right_shoulder.y) / 2
            hip_center_y = (left_hip.y + right_hip.y) / 2
            
            if shoulder_center_y > hip_center_y + 0.2:  # Too much forward lean
                score -= 10
            
            return max(0, score)
            
        except Exception:
            return 50
    
    def _evaluate_pullup_form(self, landmarks):
        """Evaluate pull-up form"""
        try:
            # Get key landmarks
            left_shoulder = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_SHOULDER]
            right_shoulder = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_SHOULDER]
            left_elbow = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_ELBOW]
            right_elbow = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_ELBOW]
            left_wrist = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_WRIST]
            right_wrist = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_WRIST]
            left_hip = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_HIP]
            right_hip = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_HIP]
            
            score = 100
            
            # Check arm angles
            left_arm_angle = self.calculate_angle(left_shoulder, left_elbow, left_wrist)
            right_arm_angle = self.calculate_angle(right_shoulder, right_elbow, right_wrist)
            
            # Check body position (should be relatively straight)
            left_body_angle = self.calculate_angle(left_shoulder, left_hip, landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_KNEE])
            right_body_angle = self.calculate_angle(right_shoulder, right_hip, landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_KNEE])
            
            # Penalize asymmetric arm movement
            if abs(left_arm_angle - right_arm_angle) > 20:
                score -= 15
            
            # Penalize excessive swinging
            if abs(left_body_angle - 180) > 30:
                score -= 15
            if abs(right_body_angle - 180) > 30:
                score -= 15
            
            return max(0, score)
            
        except Exception:
            return 50
    
    def _evaluate_bicep_curl_form(self, landmarks):
        """Evaluate bicep curl form"""
        try:
            # Get key landmarks for both arms
            left_shoulder = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_SHOULDER]
            right_shoulder = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_SHOULDER]
            left_elbow = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_ELBOW]
            right_elbow = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_ELBOW]
            left_wrist = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_WRIST]
            right_wrist = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_WRIST]
            
            score = 100
            
            # Check elbow angles
            left_elbow_angle = self.calculate_angle(left_shoulder, left_elbow, left_wrist)
            right_elbow_angle = self.calculate_angle(right_shoulder, right_elbow, right_wrist)
            
            # Check elbow position stability (elbows should stay close to body)
            left_elbow_distance = abs(left_elbow.x - left_shoulder.x)
            right_elbow_distance = abs(right_elbow.x - right_shoulder.x)
            
            # Penalize elbow movement away from body
            if left_elbow_distance > 0.15:
                score -= 15
            if right_elbow_distance > 0.15:
                score -= 15
            
            # Penalize asymmetric movement
            if abs(left_elbow_angle - right_elbow_angle) > 25:
                score -= 20
            
            return max(0, score)
            
        except Exception:
            return 50