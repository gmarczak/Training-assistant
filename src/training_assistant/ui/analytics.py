"""
Analytics and dashboard components for the Training Assistant.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import List, Dict, Any

from ..data.models import WorkoutDatabase, WorkoutSession, ExerciseStats


def create_analytics_view():
    """Create the analytics dashboard."""
    st.title("📊 Analytics Dashboard")
    
    database = st.session_state.database
    
    # Time range selector
    col1, col2 = st.columns([1, 1])
    with col1:
        time_range = st.selectbox(
            "Time Range",
            ["Last 7 days", "Last 30 days", "Last 90 days", "All time"]
        )
    
    with col2:
        refresh_data = st.button("Refresh Data", key="refresh_analytics")
    
    # Get data based on time range
    end_date = datetime.now()
    if time_range == "Last 7 days":
        start_date = end_date - timedelta(days=7)
    elif time_range == "Last 30 days":
        start_date = end_date - timedelta(days=30)
    elif time_range == "Last 90 days":
        start_date = end_date - timedelta(days=90)
    else:
        start_date = None  # All time
    
    # Get recent sessions and stats
    recent_sessions = database.get_recent_sessions(limit=100)
    exercise_stats = database.get_all_exercise_stats()
    
    if not recent_sessions:
        st.info("No workout data available yet. Complete some workouts to see analytics!")
        return
    
    # Filter sessions by time range
    if start_date:
        recent_sessions = [
            session for session in recent_sessions
            if session.start_time and session.start_time >= start_date
        ]
    
    # Overview metrics
    create_overview_metrics(recent_sessions, exercise_stats)
    
    st.markdown("---")
    
    # Charts and visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        create_workout_frequency_chart(recent_sessions)
        create_reps_by_exercise_chart(exercise_stats)
    
    with col2:
        create_progress_over_time_chart(recent_sessions)
        create_session_duration_chart(recent_sessions)
    
    st.markdown("---")
    
    # Detailed exercise breakdown
    create_exercise_breakdown(exercise_stats, database)


def create_overview_metrics(sessions: List[WorkoutSession], stats: List[ExerciseStats]):
    """Create overview metrics cards."""
    st.subheader("📈 Overview")
    
    # Calculate metrics
    total_sessions = len(sessions)
    total_reps = sum(session.total_reps for session in sessions)
    total_duration = sum(session.duration_seconds for session in sessions if session.duration_seconds)
    avg_session_duration = total_duration / total_sessions if total_sessions > 0 else 0
    
    # Unique exercises
    unique_exercises = len(set(session.exercise_type for session in sessions))
    
    # Display metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label="Total Sessions",
            value=total_sessions
        )
    
    with col2:
        st.metric(
            label="Total Reps",
            value=f"{total_reps:,}"
        )
    
    with col3:
        hours = int(total_duration // 3600)
        minutes = int((total_duration % 3600) // 60)
        st.metric(
            label="Total Time",
            value=f"{hours}h {minutes}m"
        )
    
    with col4:
        avg_minutes = int(avg_session_duration // 60)
        avg_seconds = int(avg_session_duration % 60)
        st.metric(
            label="Avg Session",
            value=f"{avg_minutes}:{avg_seconds:02d}"
        )
    
    with col5:
        st.metric(
            label="Exercises",
            value=unique_exercises
        )


def create_workout_frequency_chart(sessions: List[WorkoutSession]):
    """Create workout frequency chart."""
    st.subheader("🗓️ Workout Frequency")
    
    if not sessions:
        st.info("No session data available")
        return
    
    # Group sessions by date
    session_dates = [session.start_time.date() for session in sessions if session.start_time]
    date_counts = pd.Series(session_dates).value_counts().sort_index()
    
    # Create date range for the chart
    if len(date_counts) > 0:
        start_date = min(date_counts.index)
        end_date = max(date_counts.index)
        date_range = pd.date_range(start=start_date, end=end_date)
        
        # Fill missing dates with 0
        full_data = pd.Series(index=date_range, data=0)
        for date, count in date_counts.items():
            full_data[date] = count
        
        # Create chart
        fig = px.bar(
            x=full_data.index,
            y=full_data.values,
            title="Daily Workout Sessions",
            labels={'x': 'Date', 'y': 'Sessions'}
        )
        
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Number of Sessions",
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)


def create_progress_over_time_chart(sessions: List[WorkoutSession]):
    """Create progress over time chart."""
    st.subheader("📈 Progress Over Time")
    
    if not sessions:
        st.info("No session data available")
        return
    
    # Group by exercise type and date
    df_data = []
    for session in sessions:
        if session.start_time:
            df_data.append({
                'date': session.start_time.date(),
                'exercise': session.exercise_type.title(),
                'reps': session.total_reps,
                'duration': session.duration_seconds
            })
    
    if not df_data:
        st.info("No valid session data available")
        return
    
    df = pd.DataFrame(df_data)
    
    # Exercise selector
    selected_exercise = st.selectbox(
        "Select Exercise for Progress",
        options=df['exercise'].unique(),
        key="progress_exercise_selector"
    )
    
    # Filter data
    exercise_data = df[df['exercise'] == selected_exercise]
    
    if len(exercise_data) == 0:
        st.info(f"No data available for {selected_exercise}")
        return
    
    # Create line chart
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=exercise_data['date'],
        y=exercise_data['reps'],
        mode='lines+markers',
        name='Reps',
        line=dict(color='#1f77b4')
    ))
    
    fig.update_layout(
        title=f"{selected_exercise} Progress",
        xaxis_title="Date",
        yaxis_title="Repetitions",
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)


def create_reps_by_exercise_chart(stats: List[ExerciseStats]):
    """Create reps by exercise chart."""
    st.subheader("🏋️ Reps by Exercise")
    
    if not stats:
        st.info("No exercise statistics available")
        return
    
    # Prepare data
    exercise_names = [stat.exercise_type.title() for stat in stats]
    total_reps = [stat.total_reps for stat in stats]
    
    # Create pie chart
    fig = px.pie(
        values=total_reps,
        names=exercise_names,
        title="Total Reps Distribution"
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)


def create_session_duration_chart(sessions: List[WorkoutSession]):
    """Create session duration chart."""
    st.subheader("⏱️ Session Durations")
    
    if not sessions:
        st.info("No session data available")
        return
    
    # Prepare data
    durations = [session.duration_seconds / 60 for session in sessions if session.duration_seconds]  # Convert to minutes
    exercise_types = [session.exercise_type.title() for session in sessions if session.duration_seconds]
    
    if not durations:
        st.info("No duration data available")
        return
    
    # Create box plot
    df = pd.DataFrame({
        'exercise': exercise_types,
        'duration_minutes': durations
    })
    
    fig = px.box(
        df,
        x='exercise',
        y='duration_minutes',
        title="Session Duration by Exercise"
    )
    
    fig.update_layout(
        xaxis_title="Exercise",
        yaxis_title="Duration (minutes)",
        xaxis_tickangle=-45
    )
    
    st.plotly_chart(fig, use_container_width=True)


def create_exercise_breakdown(stats: List[ExerciseStats], database: WorkoutDatabase):
    """Create detailed exercise breakdown."""
    st.subheader("🔍 Exercise Breakdown")
    
    if not stats:
        st.info("No exercise statistics available")
        return
    
    # Create a detailed table
    breakdown_data = []
    for stat in stats:
        breakdown_data.append({
            'Exercise': stat.exercise_type.title(),
            'Total Sessions': stat.total_sessions,
            'Total Reps': f"{stat.total_reps:,}",
            'Avg Reps/Session': f"{stat.average_reps_per_session:.1f}",
            'Total Duration': f"{stat.total_duration / 60:.1f} min",
            'Avg Duration': f"{stat.average_session_duration / 60:.1f} min",
            'Best Session': f"{stat.best_session_reps} reps",
            'Avg Form Score': f"{stat.average_form_score:.1f}/10",
            'Last Session': stat.last_session_date.strftime('%Y-%m-%d') if stat.last_session_date else 'Never'
        })
    
    df = pd.DataFrame(breakdown_data)
    st.dataframe(df, use_container_width=True)
    
    # Exercise-specific details
    if len(stats) > 0:
        st.subheader("📋 Exercise Details")
        
        selected_exercise_detail = st.selectbox(
            "Select Exercise for Details",
            options=[stat.exercise_type for stat in stats],
            format_func=lambda x: x.title(),
            key="exercise_detail_selector"
        )
        
        # Get recent sessions for the selected exercise
        recent_exercise_sessions = database.get_sessions_by_exercise(selected_exercise_detail, limit=10)
        
        if recent_exercise_sessions:
            st.markdown(f"### Recent {selected_exercise_detail.title()} Sessions")
            
            session_data = []
            for session in recent_exercise_sessions:
                session_data.append({
                    'Date': session.start_time.strftime('%Y-%m-%d %H:%M') if session.start_time else 'Unknown',
                    'Reps': session.total_reps,
                    'Duration': f"{session.duration_seconds / 60:.1f} min" if session.duration_seconds else 'N/A',
                    'Source': session.input_source.title(),
                    'Form Score': f"{session.average_form_score:.1f}/10" if session.average_form_score else 'N/A'
                })
            
            session_df = pd.DataFrame(session_data)
            st.dataframe(session_df, use_container_width=True)
        else:
            st.info(f"No recent sessions found for {selected_exercise_detail.title()}")


def create_dashboard():
    """Create a quick dashboard overview."""
    st.title("📊 Dashboard")
    
    database = st.session_state.database
    
    # Get recent data
    recent_sessions = database.get_recent_sessions(limit=5)
    exercise_stats = database.get_all_exercise_stats()
    
    # Quick stats
    if recent_sessions:
        st.subheader("🎯 Quick Stats")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_sessions_today = len([
                s for s in recent_sessions 
                if s.start_time and s.start_time.date() == datetime.now().date()
            ])
            st.metric("Today's Sessions", total_sessions_today)
        
        with col2:
            last_session = recent_sessions[0] if recent_sessions else None
            if last_session and last_session.start_time:
                days_since = (datetime.now() - last_session.start_time).days
                st.metric("Days Since Last Workout", days_since)
            else:
                st.metric("Days Since Last Workout", "∞")
        
        with col3:
            weekly_sessions = len([
                s for s in recent_sessions 
                if s.start_time and s.start_time >= datetime.now() - timedelta(days=7)
            ])
            st.metric("This Week's Sessions", weekly_sessions)
        
        # Recent sessions
        st.subheader("🕐 Recent Sessions")
        
        for session in recent_sessions[:3]:
            with st.container():
                col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                
                with col1:
                    st.markdown(f"**{session.exercise_type.title()}**")
                
                with col2:
                    st.markdown(f"{session.total_reps} reps")
                
                with col3:
                    if session.duration_seconds:
                        minutes = int(session.duration_seconds // 60)
                        seconds = int(session.duration_seconds % 60)
                        st.markdown(f"{minutes}:{seconds:02d}")
                    else:
                        st.markdown("--:--")
                
                with col4:
                    if session.start_time:
                        st.markdown(session.start_time.strftime('%m/%d %H:%M'))
                    else:
                        st.markdown("Unknown")
                
                st.markdown("---")
    
    else:
        st.info("No workout data available yet. Start your first workout!")
    
    # Exercise recommendations
    if exercise_stats:
        st.subheader("💡 Recommendations")
        
        # Find least practiced exercise
        least_practiced = min(exercise_stats, key=lambda x: x.total_sessions)
        
        # Find exercise not done recently
        recent_exercises = {s.exercise_type for s in recent_sessions[:5]}
        exercise_library = st.session_state.exercise_library
        all_exercises = set(exercise_library.get_all_exercises().keys())
        not_recent = all_exercises - recent_exercises
        
        if not_recent:
            recommended = list(not_recent)[0]
            st.info(f"💪 Try **{recommended.title()}** - you haven't done this recently!")
        elif least_practiced:
            st.info(f"🎯 Consider practicing **{least_practiced.exercise_type.title()}** - only {least_practiced.total_sessions} sessions so far!")
        else:
            st.success("🌟 Great job! You're practicing all exercises regularly!")