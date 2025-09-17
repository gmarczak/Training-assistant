"""
Video processing module for handling camera feed and MP4 files.
"""

import cv2
import numpy as np
from typing import Generator, Optional, Tuple, Dict, Any
import tempfile
import os


class VideoProcessor:
    """Handles video input from camera or MP4 files."""
    
    def __init__(self):
        """Initialize the video processor."""
        self.cap = None
        self.is_camera = False
        self.total_frames = 0
        self.current_frame = 0
        self.fps = 30
        
    def open_camera(self, camera_index: int = 0) -> bool:
        """
        Open camera for live video feed.
        
        Args:
            camera_index: Index of the camera to use
            
        Returns:
            True if camera opened successfully
        """
        self.cap = cv2.VideoCapture(camera_index)
        if self.cap.isOpened():
            self.is_camera = True
            self.fps = self.cap.get(cv2.CAP_PROP_FPS) or 30
            return True
        return False
    
    def open_video_file(self, file_path: str) -> bool:
        """
        Open MP4 file for processing.
        
        Args:
            file_path: Path to the video file
            
        Returns:
            True if file opened successfully
        """
        if not os.path.exists(file_path):
            return False
            
        self.cap = cv2.VideoCapture(file_path)
        if self.cap.isOpened():
            self.is_camera = False
            self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            self.fps = self.cap.get(cv2.CAP_PROP_FPS) or 30
            self.current_frame = 0
            return True
        return False
    
    def get_frame(self) -> Optional[np.ndarray]:
        """
        Get the next frame from the video source.
        
        Returns:
            Frame as numpy array or None if no frame available
        """
        if not self.cap or not self.cap.isOpened():
            return None
            
        ret, frame = self.cap.read()
        if ret:
            if not self.is_camera:
                self.current_frame += 1
            return frame
        return None
    
    def get_frame_info(self) -> Dict[str, Any]:
        """
        Get information about the current video source.
        
        Returns:
            Dictionary with video information
        """
        if not self.cap:
            return {}
            
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        info = {
            'width': width,
            'height': height,
            'fps': self.fps,
            'is_camera': self.is_camera
        }
        
        if not self.is_camera:
            info['total_frames'] = self.total_frames
            info['current_frame'] = self.current_frame
            info['progress'] = self.current_frame / self.total_frames if self.total_frames > 0 else 0
        
        return info
    
    def seek_frame(self, frame_number: int) -> bool:
        """
        Seek to a specific frame (only for video files).
        
        Args:
            frame_number: Frame number to seek to
            
        Returns:
            True if seek was successful
        """
        if self.is_camera or not self.cap:
            return False
            
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        self.current_frame = frame_number
        return True
    
    def close(self):
        """Close the video source."""
        if self.cap:
            self.cap.release()
            self.cap = None
    
    def __del__(self):
        """Cleanup when object is destroyed."""
        self.close()


class FrameProcessor:
    """Handles frame preprocessing and optimization."""
    
    @staticmethod
    def resize_frame(frame: np.ndarray, 
                    target_width: int = 640, 
                    maintain_aspect: bool = True) -> np.ndarray:
        """
        Resize frame for processing optimization.
        
        Args:
            frame: Input frame
            target_width: Target width for resizing
            maintain_aspect: Whether to maintain aspect ratio
            
        Returns:
            Resized frame
        """
        if maintain_aspect:
            height, width = frame.shape[:2]
            aspect_ratio = height / width
            target_height = int(target_width * aspect_ratio)
            return cv2.resize(frame, (target_width, target_height))
        else:
            return cv2.resize(frame, (target_width, target_width))
    
    @staticmethod
    def enhance_frame(frame: np.ndarray) -> np.ndarray:
        """
        Enhance frame quality for better pose detection.
        
        Args:
            frame: Input frame
            
        Returns:
            Enhanced frame
        """
        # Convert to LAB color space for better lighting normalization
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        
        # Apply CLAHE to L channel
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        lab[:, :, 0] = clahe.apply(lab[:, :, 0])
        
        # Convert back to BGR
        enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        
        return enhanced
    
    @staticmethod
    def add_info_overlay(frame: np.ndarray, 
                        rep_count: int, 
                        exercise_type: str,
                        current_phase: str,
                        form_feedback: list,
                        angle: Optional[float] = None) -> np.ndarray:
        """
        Add information overlay to the frame.
        
        Args:
            frame: Input frame
            rep_count: Current repetition count
            exercise_type: Type of exercise
            current_phase: Current phase of exercise
            form_feedback: List of feedback messages
            angle: Current angle measurement
            
        Returns:
            Frame with overlay information
        """
        overlay_frame = frame.copy()
        height, width = frame.shape[:2]
        
        # Define colors
        GREEN = (0, 255, 0)
        RED = (0, 0, 255)
        BLUE = (255, 0, 0)
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        
        # Add semi-transparent background for text
        overlay = overlay_frame.copy()
        cv2.rectangle(overlay, (10, 10), (400, 200), BLACK, -1)
        cv2.addWeighted(overlay, 0.7, overlay_frame, 0.3, 0, overlay_frame)
        
        # Add exercise info
        cv2.putText(overlay_frame, f"Exercise: {exercise_type.title()}", 
                   (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, WHITE, 2)
        
        cv2.putText(overlay_frame, f"Reps: {rep_count}", 
                   (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.8, GREEN, 2)
        
        cv2.putText(overlay_frame, f"Phase: {current_phase.title()}", 
                   (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.6, BLUE, 2)
        
        if angle is not None:
            cv2.putText(overlay_frame, f"Angle: {angle:.1f}°", 
                       (20, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.6, WHITE, 2)
        
        # Add form feedback
        y_offset = 160
        for i, feedback in enumerate(form_feedback[:2]):  # Show max 2 feedback messages
            color = RED if any(word in feedback.lower() for word in ['deeper', 'lower', 'symmetric', 'balance']) else GREEN
            cv2.putText(overlay_frame, feedback, 
                       (20, y_offset + i * 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        
        return overlay_frame
    
    @staticmethod
    def save_frame_as_image(frame: np.ndarray, filename: str) -> bool:
        """
        Save frame as image file.
        
        Args:
            frame: Frame to save
            filename: Output filename
            
        Returns:
            True if saved successfully
        """
        try:
            return cv2.imwrite(filename, frame)
        except Exception as e:
            print(f"Error saving frame: {e}")
            return False


def create_temp_video_file(uploaded_file) -> str:
    """
    Create a temporary file from uploaded video for processing.
    
    Args:
        uploaded_file: Streamlit uploaded file object
        
    Returns:
        Path to temporary file
    """
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    temp_file.write(uploaded_file.read())
    temp_file.close()
    return temp_file.name