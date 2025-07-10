import streamlit as st
import asyncio
import json
from datetime import datetime
from dotenv import load_dotenv
from crewai import Crew
from agents import MeetingPreparationAgents
from tasks import MeetingPreparationTasks

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="Meeting Prep Assistant",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1e3a8a;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    
    .section-header {
        font-size: 1.5rem;
        color: #3730a3;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #e5e7eb;
        padding-bottom: 0.5rem;
    }
    
    .info-box {
        background-color: #f8fafc;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #3b82f6;
        margin: 1rem 0;
    }
    
    .success-box {
        background-color: #f0fdf4;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #22c55e;
        margin: 1rem 0;
    }
    
    .warning-box {
        background-color: #fffbeb;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #f59e0b;
        margin: 1rem 0;
    }
    
    .stButton > button {
        width: 100%;
        background-color: #3b82f6;
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 0.5rem;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        background-color: #2563eb;
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'meeting_data' not in st.session_state:
        st.session_state.meeting_data = {}
    if 'crew_result' not in st.session_state:
        st.session_state.crew_result = None
    if 'processing' not in st.session_state:
        st.session_state.processing = False

def run_meeting_prep_crew(participants, context, objective):
    """Run the meeting preparation crew"""
    try:
        # Initialize tasks and agents
        tasks = MeetingPreparationTasks()
        agents = MeetingPreparationAgents()

        # Create Agents
        researcher_agent = agents.research_agent()
        industry_analyst_agent = agents.industry_analysis_agent()
        meeting_strategy_agent = agents.meeting_strategy_agent()
        summary_and_briefing_agent = agents.summary_and_briefing_agent()

        # Create Tasks
        research = tasks.research_task(researcher_agent, participants, context)
        industry_analysis = tasks.industry_analysis_task(industry_analyst_agent, participants, context)
        meeting_strategy = tasks.meeting_strategy_task(meeting_strategy_agent, context, objective)
        summary_and_briefing = tasks.summary_and_briefing_task(summary_and_briefing_agent, context, objective)

        # Set dependencies
        meeting_strategy.context = [research, industry_analysis]
        summary_and_briefing.context = [research, industry_analysis, meeting_strategy]

        # Create and run Crew
        crew = Crew(
            agents=[researcher_agent, industry_analyst_agent, meeting_strategy_agent, summary_and_briefing_agent],
            tasks=[research, industry_analysis, meeting_strategy, summary_and_briefing]
        )

        return crew.kickoff()
    
    except Exception as e:
        return f"Error running crew: {str(e)}"

def display_meeting_brief(result):
    """Display the meeting brief in a structured format"""
    st.markdown('<div class="section-header">📋 Meeting Brief</div>', unsafe_allow_html=True)
    
    # Try to parse JSON if result is structured
    try:
        if isinstance(result, str):
            # If it's a string, display it directly
            st.markdown(f'<div class="success-box">{result}</div>', unsafe_allow_html=True)
        else:
            # If it's structured data, format it nicely
            st.json(result)
    except:
        st.markdown(f'<div class="success-box">{str(result)}</div>', unsafe_allow_html=True)

def main():
    # Initialize session state
    initialize_session_state()
    
    # Main header
    st.markdown('<div class="main-header">📅 Meeting Preparation Assistant</div>', unsafe_allow_html=True)
    
    # Sidebar with information
    with st.sidebar:
        st.markdown("### 🤖 AI Agents")
        st.markdown("""
        - **Research Specialist**: Finds participant information
        - **Industry Analyst**: Analyzes market trends
        - **Strategy Advisor**: Develops talking points
        - **Briefing Coordinator**: Creates final summary
        """)
        
        st.markdown("### 🔧 Required API Keys")
        st.markdown("""
        - GEMINI_API_KEY
        - SERPER_API_KEY
        - EXA_API_KEY
        """)
        
        if st.button("🗑️ Clear Session"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="section-header">📝 Meeting Details</div>', unsafe_allow_html=True)
        
        # Input form
        with st.form("meeting_form"):
            participants = st.text_area(
                "👥 Meeting Participants",
                placeholder="Enter the names of participants (other than you), separated by commas...",
                help="List all participants who will be in the meeting"
            )
            
            context = st.text_area(
                "🎯 Meeting Context",
                placeholder="Describe the context and purpose of the meeting...",
                help="What is this meeting about? What's the background?"
            )
            
            objective = st.text_area(
                "🎯 Your Objective",
                placeholder="What do you want to achieve in this meeting?...",
                help="What are your specific goals for this meeting?"
            )
            
            submitted = st.form_submit_button("🚀 Generate Meeting Brief")
            
            if submitted:
                if not participants or not context or not objective:
                    st.error("⚠️ Please fill in all fields before generating the meeting brief.")
                else:
                    # Store form data
                    st.session_state.meeting_data = {
                        'participants': participants,
                        'context': context,
                        'objective': objective,
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    st.session_state.processing = True
                    st.rerun()
    
    with col2:
        st.markdown('<div class="section-header">ℹ️ How it Works</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="info-box">
        <ol>
        <li><strong>Research</strong>: AI searches for participant LinkedIn profiles</li>
        <li><strong>Analysis</strong>: Reviews industry trends and challenges</li>
        <li><strong>Strategy</strong>: Develops talking points and questions</li>
        <li><strong>Brief</strong>: Compiles everything into a comprehensive document</li>
        </ol>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.meeting_data:
            st.markdown('<div class="section-header">📊 Current Meeting</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="info-box">
            <strong>Participants:</strong> {st.session_state.meeting_data.get('participants', 'N/A')}<br>
            <strong>Context:</strong> {st.session_state.meeting_data.get('context', 'N/A')[:100]}...<br>
            <strong>Objective:</strong> {st.session_state.meeting_data.get('objective', 'N/A')[:100]}...<br>
            <strong>Created:</strong> {st.session_state.meeting_data.get('timestamp', 'N/A')}
            </div>
            """, unsafe_allow_html=True)
    
    # Processing section
    if st.session_state.processing and st.session_state.meeting_data:
        st.markdown('<div class="section-header">🔄 Processing Meeting Brief</div>', unsafe_allow_html=True)
        
        progress_placeholder = st.empty()
        status_placeholder = st.empty()
        
        with progress_placeholder.container():
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Simulate progress updates
            statuses = [
                "🔍 Researching participants...",
                "📊 Analyzing industry trends...",
                "💡 Developing meeting strategy...",
                "📋 Compiling final brief..."
            ]
            
            for i, status in enumerate(statuses):
                status_text.text(status)
                progress_bar.progress((i + 1) * 25)
                
                if i == len(statuses) - 1:  # Last step
                    # Run the actual crew
                    try:
                        result = run_meeting_prep_crew(
                            st.session_state.meeting_data['participants'],
                            st.session_state.meeting_data['context'],
                            st.session_state.meeting_data['objective']
                        )
                        st.session_state.crew_result = result
                        st.session_state.processing = False
                        progress_placeholder.empty()
                        status_placeholder.empty()
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error generating brief: {str(e)}")
                        st.session_state.processing = False
                        progress_placeholder.empty()
                        status_placeholder.empty()
                        break
    
    # Display results
    if st.session_state.crew_result and not st.session_state.processing:
        display_meeting_brief(st.session_state.crew_result)
        
        # Download button
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("💾 Save Brief"):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"meeting_brief_{timestamp}.txt"
                
                brief_content = f"""
MEETING PREPARATION BRIEF
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

PARTICIPANTS: {st.session_state.meeting_data.get('participants', 'N/A')}
CONTEXT: {st.session_state.meeting_data.get('context', 'N/A')}
OBJECTIVE: {st.session_state.meeting_data.get('objective', 'N/A')}

BRIEF:
{str(st.session_state.crew_result)}
                """
                
                st.download_button(
                    label="📄 Download Brief as TXT",
                    data=brief_content,
                    file_name=filename,
                    mime="text/plain"
                )

if __name__ == "__main__":
    main()
