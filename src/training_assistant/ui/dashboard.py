"""
Dashboard UI components.
"""

import streamlit as st
from datetime import datetime, timedelta
from ..data.models import WorkoutDatabase


def create_dashboard():
    """Create the main dashboard."""
    st.title("📊 Training Dashboard")
    
    database = st.session_state.database
    
    # Get recent data
    recent_sessions = database.get_recent_sessions(limit=10)
    exercise_stats = database.get_all_exercise_stats()
    
    if not recent_sessions:
        st.info("No workout data available yet. Complete some workouts to see your dashboard!")
        
        # Show getting started guide
        st.subheader("🚀 Getting Started")
        st.markdown("""
        1. **Select an Exercise** from the sidebar
        2. **Choose Input Source** (Camera or Upload Video)
        3. **Start Workout** and begin exercising
        4. **Get Real-time Feedback** on your form and rep count
        5. **View Analytics** to track your progress
        """)
        
        return
    
    # Quick overview metrics
    create_quick_metrics(recent_sessions, exercise_stats)
    
    st.markdown("---")
    
    # Today's activity
    create_todays_activity(recent_sessions)
    
    st.markdown("---")
    
    # Recent sessions
    create_recent_sessions_summary(recent_sessions)
    
    st.markdown("---")
    
    # Progress insights
    create_progress_insights(exercise_stats)


def create_quick_metrics(recent_sessions, exercise_stats):
    """Create quick overview metrics."""
    st.subheader("📈 Quick Overview")
    
    # Calculate metrics
    today = datetime.now().date()
    week_ago = datetime.now() - timedelta(days=7)
    
    todays_sessions = [s for s in recent_sessions if s.start_time and s.start_time.date() == today]
    weeks_sessions = [s for s in recent_sessions if s.start_time and s.start_time >= week_ago]
    
    total_reps_today = sum(s.total_reps for s in todays_sessions)
    total_reps_week = sum(s.total_reps for s in weeks_sessions)
    
    # Display metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Today's Sessions",
            value=len(todays_sessions),
            delta=f"+{len(todays_sessions)}" if len(todays_sessions) > 0 else None
        )
    
    with col2:
        st.metric(
            label="Today's Reps",
            value=total_reps_today,
            delta=f"+{total_reps_today}" if total_reps_today > 0 else None
        )
    
    with col3:
        st.metric(
            label="This Week",
            value=f"{len(weeks_sessions)} sessions",
            delta=f"{total_reps_week} reps"
        )
    
    with col4:
        if recent_sessions:
            last_session = recent_sessions[0]
            if last_session.start_time:
                days_ago = (datetime.now() - last_session.start_time).days
                if days_ago == 0:
                    last_workout = "Today"
                elif days_ago == 1:
                    last_workout = "Yesterday"
                else:
                    last_workout = f"{days_ago} days ago"
            else:
                last_workout = "Unknown"
        else:
            last_workout = "Never"
        
        st.metric(
            label="Last Workout",
            value=last_workout
        )


def create_todays_activity(recent_sessions):
    """Create today's activity section."""
    st.subheader("📅 Today's Activity")
    
    today = datetime.now().date()
    todays_sessions = [s for s in recent_sessions if s.start_time and s.start_time.date() == today]
    
    if not todays_sessions:
        st.info("No workouts completed today yet. Start your first session!")
        
        # Motivational suggestions
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 💪 Quick Workout Ideas")
            st.markdown("- 2 minutes of push-ups")
            st.markdown("- 5 minutes of squats")
            st.markdown("- 3 minutes of planks")
        
        with col2:
            st.markdown("### 🎯 Daily Goals")
            st.markdown("- Complete 1 exercise session")
            st.markdown("- Try a new exercise type")
            st.markdown("- Beat yesterday's rep count")
        
        return
    
    # Show today's sessions
    st.markdown(f"**{len(todays_sessions)} session(s) completed today:**")
    
    for i, session in enumerate(todays_sessions, 1):
        with st.container():
            col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
            
            with col1:
                st.markdown(f"**{i}. {session.exercise_type.title()}**")
            
            with col2:
                st.markdown(f"🔄 {session.total_reps} reps")
            
            with col3:
                if session.duration_seconds:
                    minutes = int(session.duration_seconds // 60)
                    seconds = int(session.duration_seconds % 60)
                    st.markdown(f"⏱️ {minutes}:{seconds:02d}")
                else:
                    st.markdown("⏱️ --:--")
            
            with col4:
                if session.start_time:
                    time_str = session.start_time.strftime('%H:%M')
                    st.markdown(f"🕐 {time_str}")
                else:
                    st.markdown("🕐 --:--")


def create_recent_sessions_summary(recent_sessions):
    """Create recent sessions summary."""
    st.subheader("🕐 Recent Sessions")
    
    # Show last 5 sessions
    for session in recent_sessions[:5]:
        with st.expander(
            f"{session.exercise_type.title()} - {session.total_reps} reps "
            f"({session.start_time.strftime('%m/%d %H:%M') if session.start_time else 'Unknown time'})"
        ):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Exercise:** {session.exercise_type.title()}")
                st.markdown(f"**Repetitions:** {session.total_reps}")
                if session.duration_seconds:
                    minutes = int(session.duration_seconds // 60)
                    seconds = int(session.duration_seconds % 60)
                    st.markdown(f"**Duration:** {minutes}:{seconds:02d}")
                st.markdown(f"**Input Source:** {session.input_source.title()}")
            
            with col2:
                if session.start_time:
                    st.markdown(f"**Date:** {session.start_time.strftime('%Y-%m-%d')}")
                    st.markdown(f"**Time:** {session.start_time.strftime('%H:%M:%S')}")
                
                if session.average_form_score > 0:
                    st.markdown(f"**Form Score:** {session.average_form_score:.1f}/10")
                
                if session.notes:
                    st.markdown(f"**Notes:** {session.notes}")


def create_progress_insights(exercise_stats):
    """Create progress insights and recommendations."""
    st.subheader("💡 Progress Insights")
    
    if not exercise_stats:
        st.info("Complete more workouts to see personalized insights!")
        return
    
    # Find best performing exercise
    best_exercise = max(exercise_stats, key=lambda x: x.total_reps)
    
    # Find most frequent exercise
    most_frequent = max(exercise_stats, key=lambda x: x.total_sessions)
    
    # Find least practiced exercise
    least_practiced = min(exercise_stats, key=lambda x: x.total_sessions)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🏆 Your Strengths")
        
        st.success(
            f"**Most Total Reps:** {best_exercise.exercise_type.title()} "
            f"({best_exercise.total_reps:,} reps)"
        )
        
        st.success(
            f"**Most Practiced:** {most_frequent.exercise_type.title()} "
            f"({most_frequent.total_sessions} sessions)"
        )
        
        # Calculate consistency
        total_sessions = sum(stat.total_sessions for stat in exercise_stats)
        if total_sessions >= 5:
            st.success("**Consistency:** Great job maintaining a regular workout routine!")
        elif total_sessions >= 2:
            st.info("**Consistency:** Good start! Try to workout more regularly.")
        else:
            st.warning("**Consistency:** Consider establishing a regular workout schedule.")
    
    with col2:
        st.markdown("### 🎯 Recommendations")
        
        # Recommend least practiced exercise
        if least_practiced.total_sessions < most_frequent.total_sessions / 2:
            st.info(
                f"**Try More:** {least_practiced.exercise_type.title()} "
                f"(only {least_practiced.total_sessions} sessions)"
            )
        
        # Recommend based on recent activity
        st.info("**Challenge Yourself:** Try to beat your personal best!")
        
        # Form improvement suggestion
        avg_form_scores = [stat.average_form_score for stat in exercise_stats if stat.average_form_score > 0]
        if avg_form_scores:
            avg_form = sum(avg_form_scores) / len(avg_form_scores)
            if avg_form < 7:
                st.warning("**Focus on Form:** Consider slowing down to improve technique.")
            else:
                st.success("**Great Form:** Your technique is excellent!")
        
        # Weekly goal suggestion
        current_week_sessions = sum(1 for stat in exercise_stats if stat.last_session_date and 
                                  (datetime.now() - stat.last_session_date).days <= 7)
        
        if current_week_sessions < 3:
            st.info("**Weekly Goal:** Aim for 3+ workout sessions this week!")
        else:
            st.success(f"**Weekly Goal:** Excellent! {current_week_sessions} sessions this week!")


def create_workout_summary_card(session):
    """Create a summary card for a workout session."""
    with st.container():
        st.markdown(f"""
        <div style="
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 16px;
            margin: 8px 0;
            background-color: #f9f9f9;
        ">
            <h4>{session.exercise_type.title()}</h4>
            <p><strong>Reps:</strong> {session.total_reps}</p>
            <p><strong>Duration:</strong> {session.duration_seconds / 60:.1f} minutes</p>
            <p><strong>Date:</strong> {session.start_time.strftime('%Y-%m-%d %H:%M') if session.start_time else 'Unknown'}</p>
        </div>
        """, unsafe_allow_html=True)