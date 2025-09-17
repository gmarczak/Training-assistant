"""
Exercise templates and configurations.
Defines parameters and validation rules for different exercises.
"""

from typing import Dict, List, Any
from dataclasses import dataclass


@dataclass
class ExerciseConfig:
    """Configuration for an exercise type."""
    name: str
    display_name: str
    description: str
    primary_muscle_groups: List[str]
    min_angle_threshold: float
    max_angle_threshold: float
    primary_angle_type: str  # "arm" or "leg"
    movement_pattern: str  # "down_up" or "up_down"
    form_checks: List[str]
    difficulty_level: str  # "beginner", "intermediate", "advanced"
    instructions: List[str]


class ExerciseLibrary:
    """Library of exercise configurations and templates."""
    
    def __init__(self):
        """Initialize the exercise library."""
        self.exercises = self._load_exercise_configs()
    
    def _load_exercise_configs(self) -> Dict[str, ExerciseConfig]:
        """Load all exercise configurations."""
        configs = {}
        
        # Push-ups
        configs["pushups"] = ExerciseConfig(
            name="pushups",
            display_name="Push-ups",
            description="Upper body strength exercise targeting chest, shoulders, and triceps",
            primary_muscle_groups=["chest", "shoulders", "triceps"],
            min_angle_threshold=70,
            max_angle_threshold=160,
            primary_angle_type="arm",
            movement_pattern="down_up",
            form_checks=[
                "arm_symmetry",
                "depth_check",
                "back_straight"
            ],
            difficulty_level="beginner",
            instructions=[
                "Start in plank position with arms extended",
                "Lower your body by bending your arms",
                "Go down until chest nearly touches ground",
                "Push back up to starting position",
                "Keep your back straight throughout"
            ]
        )
        
        # Squats
        configs["squats"] = ExerciseConfig(
            name="squats",
            display_name="Squats",
            description="Lower body exercise targeting quadriceps, glutes, and hamstrings",
            primary_muscle_groups=["quadriceps", "glutes", "hamstrings"],
            min_angle_threshold=70,
            max_angle_threshold=160,
            primary_angle_type="leg",
            movement_pattern="down_up",
            form_checks=[
                "leg_symmetry",
                "depth_check",
                "knee_alignment"
            ],
            difficulty_level="beginner",
            instructions=[
                "Stand with feet shoulder-width apart",
                "Lower your body by bending your knees",
                "Go down until thighs are parallel to ground",
                "Push through heels to return to standing",
                "Keep your chest up and back straight"
            ]
        )
        
        # Pull-ups
        configs["pullups"] = ExerciseConfig(
            name="pullups",
            display_name="Pull-ups",
            description="Upper body exercise targeting back, biceps, and rear deltoids",
            primary_muscle_groups=["back", "biceps", "rear_deltoids"],
            min_angle_threshold=40,
            max_angle_threshold=160,
            primary_angle_type="arm",
            movement_pattern="up_down",
            form_checks=[
                "full_extension",
                "chin_over_bar",
                "arm_symmetry"
            ],
            difficulty_level="intermediate",
            instructions=[
                "Hang from pull-up bar with arms fully extended",
                "Pull your body up until chin goes over the bar",
                "Lower yourself back to full arm extension",
                "Avoid swinging or using momentum",
                "Engage your core throughout the movement"
            ]
        )
        
        # Lunges
        configs["lunges"] = ExerciseConfig(
            name="lunges",
            display_name="Lunges",
            description="Lower body exercise targeting quadriceps, glutes, and calves",
            primary_muscle_groups=["quadriceps", "glutes", "calves"],
            min_angle_threshold=80,
            max_angle_threshold=160,
            primary_angle_type="leg",
            movement_pattern="down_up",
            form_checks=[
                "front_knee_alignment",
                "depth_check",
                "balance"
            ],
            difficulty_level="beginner",
            instructions=[
                "Start standing with feet hip-width apart",
                "Step forward with one leg",
                "Lower your body until front thigh is parallel to ground",
                "Push back to starting position",
                "Keep front knee over ankle, not pushed out past toes"
            ]
        )
        
        # Bicep Curls
        configs["bicep_curls"] = ExerciseConfig(
            name="bicep_curls",
            display_name="Bicep Curls",
            description="Isolation exercise targeting biceps",
            primary_muscle_groups=["biceps"],
            min_angle_threshold=30,
            max_angle_threshold=160,
            primary_angle_type="arm",
            movement_pattern="up_down",
            form_checks=[
                "elbow_stability",
                "full_range_motion",
                "controlled_movement"
            ],
            difficulty_level="beginner",
            instructions=[
                "Stand with feet shoulder-width apart",
                "Hold weights with arms at your sides",
                "Curl weights up by bending your elbows",
                "Keep elbows close to your body",
                "Lower weights slowly to starting position"
            ]
        )
        
        # Shoulder Press
        configs["shoulder_press"] = ExerciseConfig(
            name="shoulder_press",
            display_name="Shoulder Press",
            description="Upper body exercise targeting shoulders and triceps",
            primary_muscle_groups=["shoulders", "triceps"],
            min_angle_threshold=45,
            max_angle_threshold=170,
            primary_angle_type="arm",
            movement_pattern="up_down",
            form_checks=[
                "arm_symmetry",
                "full_extension",
                "core_stability"
            ],
            difficulty_level="intermediate",
            instructions=[
                "Stand or sit with weights at shoulder level",
                "Press weights straight up overhead",
                "Extend arms fully without locking elbows",
                "Lower weights back to shoulder level",
                "Keep your core engaged throughout"
            ]
        )
        
        # Planks (special case - isometric exercise)
        configs["planks"] = ExerciseConfig(
            name="planks",
            display_name="Planks",
            description="Core stability exercise",
            primary_muscle_groups=["core", "shoulders"],
            min_angle_threshold=170,  # Body should be straight
            max_angle_threshold=190,
            primary_angle_type="body",
            movement_pattern="hold",
            form_checks=[
                "straight_back",
                "core_engagement",
                "breathing"
            ],
            difficulty_level="beginner",
            instructions=[
                "Start in push-up position",
                "Lower to forearms",
                "Keep body in straight line from head to heels",
                "Hold position while breathing normally",
                "Engage core muscles throughout"
            ]
        )
        
        return configs
    
    def get_exercise(self, exercise_name: str) -> ExerciseConfig:
        """
        Get exercise configuration by name.
        
        Args:
            exercise_name: Name of the exercise
            
        Returns:
            Exercise configuration
        """
        return self.exercises.get(exercise_name.lower())
    
    def get_all_exercises(self) -> Dict[str, ExerciseConfig]:
        """Get all exercise configurations."""
        return self.exercises
    
    def get_exercises_by_difficulty(self, difficulty: str) -> Dict[str, ExerciseConfig]:
        """
        Get exercises filtered by difficulty level.
        
        Args:
            difficulty: Difficulty level to filter by
            
        Returns:
            Dictionary of exercises matching the difficulty
        """
        return {
            name: config for name, config in self.exercises.items()
            if config.difficulty_level == difficulty.lower()
        }
    
    def get_exercises_by_muscle_group(self, muscle_group: str) -> Dict[str, ExerciseConfig]:
        """
        Get exercises that target a specific muscle group.
        
        Args:
            muscle_group: Target muscle group
            
        Returns:
            Dictionary of exercises targeting the muscle group
        """
        return {
            name: config for name, config in self.exercises.items()
            if muscle_group.lower() in [mg.lower() for mg in config.primary_muscle_groups]
        }
    
    def validate_exercise_name(self, exercise_name: str) -> bool:
        """
        Validate if an exercise name exists in the library.
        
        Args:
            exercise_name: Name to validate
            
        Returns:
            True if exercise exists
        """
        return exercise_name.lower() in self.exercises