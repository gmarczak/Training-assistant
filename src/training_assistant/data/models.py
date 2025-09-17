"""
Data models for training sessions and storage.
"""

import sqlite3
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
import os


@dataclass
class WorkoutSession:
    """Represents a workout session."""
    id: Optional[int] = None
    exercise_type: str = ""
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    total_reps: int = 0
    duration_seconds: float = 0.0
    average_form_score: float = 0.0
    input_source: str = ""  # "camera" or "file"
    notes: str = ""
    rep_times: List[float] = None  # Time for each rep
    form_feedback_history: List[str] = None  # Form feedback throughout session
    
    def __post_init__(self):
        if self.rep_times is None:
            self.rep_times = []
        if self.form_feedback_history is None:
            self.form_feedback_history = []
        if self.start_time is None:
            self.start_time = datetime.now()


@dataclass
class ExerciseStats:
    """Statistics for a specific exercise type."""
    exercise_type: str
    total_sessions: int = 0
    total_reps: int = 0
    total_duration: float = 0.0
    average_reps_per_session: float = 0.0
    average_session_duration: float = 0.0
    best_session_reps: int = 0
    best_session_duration: float = 0.0
    average_form_score: float = 0.0
    last_session_date: Optional[datetime] = None


class WorkoutDatabase:
    """Handles workout data storage and retrieval."""
    
    def __init__(self, db_path: str = "data/workout_sessions.db"):
        """
        Initialize the workout database.
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._create_tables()
    
    def _create_tables(self):
        """Create database tables if they don't exist."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS workout_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    exercise_type TEXT NOT NULL,
                    start_time TEXT NOT NULL,
                    end_time TEXT,
                    total_reps INTEGER DEFAULT 0,
                    duration_seconds REAL DEFAULT 0.0,
                    average_form_score REAL DEFAULT 0.0,
                    input_source TEXT DEFAULT 'camera',
                    notes TEXT DEFAULT '',
                    rep_times TEXT DEFAULT '[]',
                    form_feedback_history TEXT DEFAULT '[]',
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS exercise_stats (
                    exercise_type TEXT PRIMARY KEY,
                    total_sessions INTEGER DEFAULT 0,
                    total_reps INTEGER DEFAULT 0,
                    total_duration REAL DEFAULT 0.0,
                    average_reps_per_session REAL DEFAULT 0.0,
                    average_session_duration REAL DEFAULT 0.0,
                    best_session_reps INTEGER DEFAULT 0,
                    best_session_duration REAL DEFAULT 0.0,
                    average_form_score REAL DEFAULT 0.0,
                    last_session_date TEXT,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
    
    def save_session(self, session: WorkoutSession) -> int:
        """
        Save a workout session to the database.
        
        Args:
            session: WorkoutSession to save
            
        Returns:
            ID of the saved session
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO workout_sessions (
                    exercise_type, start_time, end_time, total_reps,
                    duration_seconds, average_form_score, input_source,
                    notes, rep_times, form_feedback_history
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                session.exercise_type,
                session.start_time.isoformat() if session.start_time else None,
                session.end_time.isoformat() if session.end_time else None,
                session.total_reps,
                session.duration_seconds,
                session.average_form_score,
                session.input_source,
                session.notes,
                json.dumps(session.rep_times),
                json.dumps(session.form_feedback_history)
            ))
            
            session_id = cursor.lastrowid
            session.id = session_id
            
            # Update exercise statistics
            self._update_exercise_stats(session)
            
            return session_id
    
    def get_session(self, session_id: int) -> Optional[WorkoutSession]:
        """
        Retrieve a workout session by ID.
        
        Args:
            session_id: ID of the session to retrieve
            
        Returns:
            WorkoutSession object or None if not found
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM workout_sessions WHERE id = ?
            """, (session_id,))
            
            row = cursor.fetchone()
            if row:
                return self._row_to_session(row)
        
        return None
    
    def get_recent_sessions(self, limit: int = 10) -> List[WorkoutSession]:
        """
        Get recent workout sessions.
        
        Args:
            limit: Maximum number of sessions to return
            
        Returns:
            List of recent WorkoutSession objects
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM workout_sessions 
                ORDER BY start_time DESC 
                LIMIT ?
            """, (limit,))
            
            return [self._row_to_session(row) for row in cursor.fetchall()]
    
    def get_sessions_by_exercise(self, exercise_type: str, limit: int = 50) -> List[WorkoutSession]:
        """
        Get sessions for a specific exercise type.
        
        Args:
            exercise_type: Type of exercise
            limit: Maximum number of sessions to return
            
        Returns:
            List of WorkoutSession objects
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM workout_sessions 
                WHERE exercise_type = ?
                ORDER BY start_time DESC 
                LIMIT ?
            """, (exercise_type, limit))
            
            return [self._row_to_session(row) for row in cursor.fetchall()]
    
    def get_exercise_stats(self, exercise_type: str) -> Optional[ExerciseStats]:
        """
        Get statistics for a specific exercise type.
        
        Args:
            exercise_type: Type of exercise
            
        Returns:
            ExerciseStats object or None if not found
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM exercise_stats WHERE exercise_type = ?
            """, (exercise_type,))
            
            row = cursor.fetchone()
            if row:
                return ExerciseStats(
                    exercise_type=row[0],
                    total_sessions=row[1],
                    total_reps=row[2],
                    total_duration=row[3],
                    average_reps_per_session=row[4],
                    average_session_duration=row[5],
                    best_session_reps=row[6],
                    best_session_duration=row[7],
                    average_form_score=row[8],
                    last_session_date=datetime.fromisoformat(row[9]) if row[9] else None
                )
        
        return None
    
    def get_all_exercise_stats(self) -> List[ExerciseStats]:
        """
        Get statistics for all exercise types.
        
        Returns:
            List of ExerciseStats objects
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM exercise_stats ORDER BY total_sessions DESC")
            
            stats = []
            for row in cursor.fetchall():
                stats.append(ExerciseStats(
                    exercise_type=row[0],
                    total_sessions=row[1],
                    total_reps=row[2],
                    total_duration=row[3],
                    average_reps_per_session=row[4],
                    average_session_duration=row[5],
                    best_session_reps=row[6],
                    best_session_duration=row[7],
                    average_form_score=row[8],
                    last_session_date=datetime.fromisoformat(row[9]) if row[9] else None
                ))
            
            return stats
    
    def _row_to_session(self, row) -> WorkoutSession:
        """Convert database row to WorkoutSession object."""
        return WorkoutSession(
            id=row[0],
            exercise_type=row[1],
            start_time=datetime.fromisoformat(row[2]) if row[2] else None,
            end_time=datetime.fromisoformat(row[3]) if row[3] else None,
            total_reps=row[4],
            duration_seconds=row[5],
            average_form_score=row[6],
            input_source=row[7],
            notes=row[8],
            rep_times=json.loads(row[9]) if row[9] else [],
            form_feedback_history=json.loads(row[10]) if row[10] else []
        )
    
    def _update_exercise_stats(self, session: WorkoutSession):
        """Update exercise statistics after saving a session."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Get current stats
            cursor.execute("""
                SELECT total_sessions, total_reps, total_duration,
                       best_session_reps, best_session_duration, average_form_score
                FROM exercise_stats WHERE exercise_type = ?
            """, (session.exercise_type,))
            
            current_stats = cursor.fetchone()
            
            if current_stats:
                # Update existing stats
                total_sessions = current_stats[0] + 1
                total_reps = current_stats[1] + session.total_reps
                total_duration = current_stats[2] + session.duration_seconds
                best_reps = max(current_stats[3], session.total_reps)
                best_duration = max(current_stats[4], session.duration_seconds)
                
                # Calculate new averages
                avg_reps = total_reps / total_sessions
                avg_duration = total_duration / total_sessions
                
                # Update average form score
                old_avg_form = current_stats[5]
                new_avg_form = ((old_avg_form * (total_sessions - 1)) + session.average_form_score) / total_sessions
                
                cursor.execute("""
                    UPDATE exercise_stats SET
                        total_sessions = ?,
                        total_reps = ?,
                        total_duration = ?,
                        average_reps_per_session = ?,
                        average_session_duration = ?,
                        best_session_reps = ?,
                        best_session_duration = ?,
                        average_form_score = ?,
                        last_session_date = ?,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE exercise_type = ?
                """, (
                    total_sessions, total_reps, total_duration,
                    avg_reps, avg_duration, best_reps, best_duration,
                    new_avg_form, session.start_time.isoformat(),
                    session.exercise_type
                ))
            else:
                # Create new stats entry
                cursor.execute("""
                    INSERT INTO exercise_stats (
                        exercise_type, total_sessions, total_reps, total_duration,
                        average_reps_per_session, average_session_duration,
                        best_session_reps, best_session_duration, average_form_score,
                        last_session_date
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    session.exercise_type, 1, session.total_reps, session.duration_seconds,
                    session.total_reps, session.duration_seconds,
                    session.total_reps, session.duration_seconds, session.average_form_score,
                    session.start_time.isoformat()
                ))
    
    def delete_session(self, session_id: int) -> bool:
        """
        Delete a workout session.
        
        Args:
            session_id: ID of the session to delete
            
        Returns:
            True if session was deleted
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM workout_sessions WHERE id = ?", (session_id,))
            return cursor.rowcount > 0