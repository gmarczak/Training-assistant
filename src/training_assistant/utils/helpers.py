"""
Utility functions for the Training Assistant.
"""

import cv2
import numpy as np
from typing import Tuple, Optional
import tempfile
import os


def calculate_fps(start_time: float, frame_count: int) -> float:
    """
    Calculate frames per second.
    
    Args:
        start_time: Start time in seconds
        frame_count: Number of frames processed
        
    Returns:
        FPS value
    """
    import time
    elapsed_time = time.time() - start_time
    if elapsed_time > 0:
        return frame_count / elapsed_time
    return 0.0


def resize_image_keep_aspect(image: np.ndarray, target_size: Tuple[int, int]) -> np.ndarray:
    """
    Resize image while keeping aspect ratio.
    
    Args:
        image: Input image
        target_size: Target (width, height)
        
    Returns:
        Resized image
    """
    h, w = image.shape[:2]
    target_w, target_h = target_size
    
    # Calculate scaling factor
    scale = min(target_w / w, target_h / h)
    
    # Calculate new dimensions
    new_w = int(w * scale)
    new_h = int(h * scale)
    
    # Resize image
    resized = cv2.resize(image, (new_w, new_h))
    
    # Create padded image
    padded = np.zeros((target_h, target_w, 3), dtype=np.uint8)
    
    # Calculate padding
    y_offset = (target_h - new_h) // 2
    x_offset = (target_w - new_w) // 2
    
    # Place resized image in center
    padded[y_offset:y_offset + new_h, x_offset:x_offset + new_w] = resized
    
    return padded


def create_gradient_background(width: int, height: int, 
                             color1: Tuple[int, int, int] = (100, 100, 100),
                             color2: Tuple[int, int, int] = (50, 50, 50)) -> np.ndarray:
    """
    Create a gradient background.
    
    Args:
        width: Background width
        height: Background height
        color1: Start color (BGR)
        color2: End color (BGR)
        
    Returns:
        Gradient background image
    """
    background = np.zeros((height, width, 3), dtype=np.uint8)
    
    for i in range(height):
        ratio = i / height
        color = [
            int(color1[j] * (1 - ratio) + color2[j] * ratio)
            for j in range(3)
        ]
        background[i, :] = color
    
    return background


def validate_video_file(file_path: str) -> bool:
    """
    Validate if a file is a valid video file.
    
    Args:
        file_path: Path to the video file
        
    Returns:
        True if valid video file
    """
    try:
        cap = cv2.VideoCapture(file_path)
        if not cap.isOpened():
            return False
        
        ret, frame = cap.read()
        cap.release()
        
        return ret and frame is not None
    except:
        return False


def format_duration(seconds: float) -> str:
    """
    Format duration in seconds to human readable format.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted duration string
    """
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}:{secs:02d}"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours}:{minutes:02d}:{secs:02d}"


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    Safely divide two numbers.
    
    Args:
        numerator: Numerator value
        denominator: Denominator value
        default: Default value if division by zero
        
    Returns:
        Division result or default value
    """
    if denominator == 0:
        return default
    return numerator / denominator


def clamp(value: float, min_value: float, max_value: float) -> float:
    """
    Clamp a value between min and max.
    
    Args:
        value: Value to clamp
        min_value: Minimum value
        max_value: Maximum value
        
    Returns:
        Clamped value
    """
    return max(min_value, min(value, max_value))


def smooth_values(values: list, window_size: int = 5) -> list:
    """
    Apply moving average smoothing to a list of values.
    
    Args:
        values: List of values to smooth
        window_size: Size of smoothing window
        
    Returns:
        Smoothed values
    """
    if len(values) < window_size:
        return values
    
    smoothed = []
    for i in range(len(values)):
        start_idx = max(0, i - window_size // 2)
        end_idx = min(len(values), i + window_size // 2 + 1)
        window_values = values[start_idx:end_idx]
        smoothed.append(sum(window_values) / len(window_values))
    
    return smoothed


def create_temp_directory() -> str:
    """
    Create a temporary directory for processing.
    
    Returns:
        Path to temporary directory
    """
    temp_dir = tempfile.mkdtemp(prefix="training_assistant_")
    return temp_dir


def cleanup_temp_files(temp_dir: str):
    """
    Clean up temporary files and directory.
    
    Args:
        temp_dir: Path to temporary directory
    """
    import shutil
    try:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
    except Exception as e:
        print(f"Warning: Could not clean up temporary directory {temp_dir}: {e}")


def get_video_info(file_path: str) -> dict:
    """
    Get information about a video file.
    
    Args:
        file_path: Path to video file
        
    Returns:
        Dictionary with video information
    """
    try:
        cap = cv2.VideoCapture(file_path)
        
        if not cap.isOpened():
            return {}
        
        info = {
            'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            'fps': cap.get(cv2.CAP_PROP_FPS),
            'frame_count': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
            'duration': 0
        }
        
        if info['fps'] > 0:
            info['duration'] = info['frame_count'] / info['fps']
        
        cap.release()
        return info
        
    except Exception as e:
        print(f"Error getting video info: {e}")
        return {}