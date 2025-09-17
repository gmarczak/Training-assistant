"""
Core pose estimation module using MediaPipe.
Handles pose detection and landmark extraction from video frames.
"""

import cv2
import mediapipe as mp
import numpy as np
from typing import Optional, List, Tuple, Dict, Any


class PoseEstimator:
    """Handles pose detection and landmark extraction using MediaPipe."""
    
    def __init__(self, 
                 min_detection_confidence: float = 0.5,
                 min_tracking_confidence: float = 0.5):
        """
        Initialize the pose estimator.
        
        Args:
            min_detection_confidence: Minimum confidence for pose detection
            min_tracking_confidence: Minimum confidence for pose tracking
        """
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        
    def detect_pose(self, frame: np.ndarray) -> Optional[Dict[str, Any]]:
        """
        Detect pose landmarks in a frame.
        
        Args:
            frame: Input video frame
            
        Returns:
            Dictionary containing pose landmarks and metadata, or None if no pose detected
        """
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame
        results = self.pose.process(rgb_frame)
        
        if results.pose_landmarks:
            # Extract landmark coordinates
            landmarks = []
            for landmark in results.pose_landmarks.landmark:
                landmarks.append({
                    'x': landmark.x,
                    'y': landmark.y,
                    'z': landmark.z,
                    'visibility': landmark.visibility
                })
            
            return {
                'landmarks': landmarks,
                'pose_landmarks': results.pose_landmarks,
                'frame_shape': frame.shape
            }
        
        return None
    
    def draw_landmarks(self, frame: np.ndarray, pose_data: Dict[str, Any]) -> np.ndarray:
        """
        Draw pose landmarks on the frame.
        
        Args:
            frame: Input frame
            pose_data: Pose detection results
            
        Returns:
            Frame with drawn landmarks
        """
        if pose_data and 'pose_landmarks' in pose_data:
            self.mp_drawing.draw_landmarks(
                frame, 
                pose_data['pose_landmarks'], 
                self.mp_pose.POSE_CONNECTIONS
            )
        return frame
    
    def get_landmark_coords(self, pose_data: Dict[str, Any], landmark_idx: int) -> Optional[Tuple[float, float]]:
        """
        Get normalized coordinates for a specific landmark.
        
        Args:
            pose_data: Pose detection results
            landmark_idx: Index of the landmark
            
        Returns:
            Tuple of (x, y) coordinates or None if landmark not available
        """
        if not pose_data or 'landmarks' not in pose_data:
            return None
            
        if landmark_idx < len(pose_data['landmarks']):
            landmark = pose_data['landmarks'][landmark_idx]
            return (landmark['x'], landmark['y'])
        
        return None
    
    def calculate_angle(self, point1: Tuple[float, float], 
                       point2: Tuple[float, float], 
                       point3: Tuple[float, float]) -> float:
        """
        Calculate angle between three points.
        
        Args:
            point1: First point coordinates
            point2: Vertex point coordinates  
            point3: Third point coordinates
            
        Returns:
            Angle in degrees
        """
        # Convert to numpy arrays
        a = np.array(point1)
        b = np.array(point2)
        c = np.array(point3)
        
        # Calculate vectors
        ba = a - b
        bc = c - b
        
        # Calculate angle
        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))
        
        return np.degrees(angle)
    
    def get_key_angles(self, pose_data: Dict[str, Any]) -> Dict[str, float]:
        """
        Calculate key body angles for exercise analysis.
        
        Args:
            pose_data: Pose detection results
            
        Returns:
            Dictionary of calculated angles
        """
        angles = {}
        
        if not pose_data or 'landmarks' not in pose_data:
            return angles
        
        # Define landmark indices
        LEFT_SHOULDER = 11
        LEFT_ELBOW = 13
        LEFT_WRIST = 15
        RIGHT_SHOULDER = 12
        RIGHT_ELBOW = 14
        RIGHT_WRIST = 16
        LEFT_HIP = 23
        LEFT_KNEE = 25
        LEFT_ANKLE = 27
        RIGHT_HIP = 24
        RIGHT_KNEE = 26
        RIGHT_ANKLE = 28
        
        try:
            # Left arm angle (shoulder-elbow-wrist)
            left_shoulder = self.get_landmark_coords(pose_data, LEFT_SHOULDER)
            left_elbow = self.get_landmark_coords(pose_data, LEFT_ELBOW)
            left_wrist = self.get_landmark_coords(pose_data, LEFT_WRIST)
            
            if all([left_shoulder, left_elbow, left_wrist]):
                angles['left_arm'] = self.calculate_angle(left_shoulder, left_elbow, left_wrist)
            
            # Right arm angle
            right_shoulder = self.get_landmark_coords(pose_data, RIGHT_SHOULDER)
            right_elbow = self.get_landmark_coords(pose_data, RIGHT_ELBOW)
            right_wrist = self.get_landmark_coords(pose_data, RIGHT_WRIST)
            
            if all([right_shoulder, right_elbow, right_wrist]):
                angles['right_arm'] = self.calculate_angle(right_shoulder, right_elbow, right_wrist)
            
            # Left leg angle (hip-knee-ankle)
            left_hip = self.get_landmark_coords(pose_data, LEFT_HIP)
            left_knee = self.get_landmark_coords(pose_data, LEFT_KNEE)
            left_ankle = self.get_landmark_coords(pose_data, LEFT_ANKLE)
            
            if all([left_hip, left_knee, left_ankle]):
                angles['left_leg'] = self.calculate_angle(left_hip, left_knee, left_ankle)
            
            # Right leg angle
            right_hip = self.get_landmark_coords(pose_data, RIGHT_HIP)
            right_knee = self.get_landmark_coords(pose_data, RIGHT_KNEE)
            right_ankle = self.get_landmark_coords(pose_data, RIGHT_ANKLE)
            
            if all([right_hip, right_knee, right_ankle]):
                angles['right_leg'] = self.calculate_angle(right_hip, right_knee, right_ankle)
                
        except Exception as e:
            print(f"Error calculating angles: {e}")
        
        return angles