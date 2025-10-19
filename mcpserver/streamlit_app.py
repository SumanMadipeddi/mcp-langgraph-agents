import streamlit as st
import asyncio
import nest_asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client
from datetime import datetime

nest_asyncio.apply()

st.set_page_config(
    page_title="Weather Intelligence",
    page_icon="⛅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Session state
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False
if 'alerts_data' not in st.session_state:
    st.session_state.alerts_data = None
if 'available_tools' not in st.session_state:
    st.session_state.available_tools = None

# Valid state codes
VALID_STATES = {"AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"}

# Get colors based on theme
colors = {
    'bg': '#0f172a' if st.session_state.dark_mode else '#e0f2fe',
    'card': '#1e293b' if st.session_state.dark_mode else '#ffffff',
    'text': '#f1f5f9' if st.session_state.dark_mode else '#0f172a',
    'secondary': '#94a3b8' if st.session_state.dark_mode else '#475569',
    'accent': '#38bdf8',
    'input_bg': '#1e293b' if st.session_state.dark_mode else '#f8fafc',
    'border': '#334155' if st.session_state.dark_mode else '#cbd5e1',
}

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
* {{ font-family: 'Inter', sans-serif; }}
.main {{ 
    background: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)), 
                url('https://images.unsplash.com/photo-1504608524841-42fe6f032b4b?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    padding: 0; 
}}
.block-container {{ padding: 1rem 2rem !important; max-width: 100% !important; }}
#MainMenu, footer, header {{ visibility: hidden; }}
.stDeployButton {{ display: none; }}

.header {{ display: flex; justify-content: space-between; align-items: center; background: {colors['card']}; padding: 1rem; border-radius: 16px; margin-bottom: 1rem; }}
.logo {{ font-size: 1.5rem; font-weight: 700; color: {colors['accent']}; }}
.status {{ padding: 0.5rem 1rem; background: #10b981; color: white; border-radius: 20px; font-size: 0.9rem; }}

.grid {{ display: grid; grid-template-columns: 1fr 2fr; gap: 1rem; }}
.card {{ background: {colors['card']}; padding: 1.5rem; border-radius: 16px; }}
.title {{ font-size: 1.2rem; font-weight: 600; color: {colors['text']}; margin-bottom: 1rem; }}

.stTextInput input {{ background: {colors['input_bg']} !important; border: 2px solid {colors['border']} !important; border-radius: 12px !important; padding: 1rem !important; font-size: 1.5rem !important; text-align: center !important; text-transform: uppercase !important; color: {colors['text']} !important; }}
.stTextInput input:focus {{ border-color: {colors['accent']} !important; }}

.stButton button {{ background: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%) !important; color: white !important; border: none !important; border-radius: 12px !important; padding: 1rem 2rem !important; font-size: 1rem !important; width: 100% !important; }}

.stats {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-bottom: 1rem; }}
.stat {{ background: {colors['input_bg']}; padding: 1rem; border-radius: 12px; text-align: center; }}
.stat-value {{ font-size: 1.5rem; font-weight: 700; color: {colors['accent']}; }}
.stat-label {{ font-size: 0.8rem; color: {colors['secondary']}; text-transform: uppercase; }}

.alert {{ background: {colors['input_bg']}; padding: 1rem; border-radius: 12px; margin-bottom: 0.8rem; border-left: 4px solid; }}
.alert.severe {{ border-left-color: #ef4444; }}
.alert.moderate {{ border-left-color: #f59e0b; }}
.alert.minor {{ border-left-color: #10b981; }}
.alert-title {{ font-weight: 600; color: {colors['text']}; margin-bottom: 0.5rem; }}
.alert-text {{ color: {colors['secondary']}; font-size: 0.9rem; }}

.empty {{ text-align: center; padding: 3rem; color: {colors['secondary']}; }}
</style>
""", unsafe_allow_html=True)

async def get_alerts(state_code):
    try:
        async with sse_client("http://localhost:8000/sse") as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                result = await session.call_tool("get_alerts", arguments={"state": state_code})
                return result.content[0].text
    except Exception as e:
        return f"Error: {str(e)}"

async def get_available_tools():
    try:
        async with sse_client("http://localhost:8000/sse") as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                tools_result = await session.list_tools()
                return [{"name": tool.name, "description": tool.description} for tool in tools_result.tools]
    except Exception as e:
        return []

def parse_alert(alert_text):
    lines = alert_text.strip().split('\n')
    data = {}
    for line in lines:
        if ':' in line:
            key, value = line.split(':', 1)
            data[key.strip()] = value.strip()
    return data

def get_severity(severity):
    s = severity.lower()
    if 'extreme' in s or 'severe' in s:
        return 'severe', '🔴'
    elif 'moderate' in s:
        return 'moderate', '🟡'
    else:
        return 'minor', '🟢'

# Load available tools on first run
if st.session_state.available_tools is None:
    with st.spinner("Loading MCP tools..."):
        st.session_state.available_tools = asyncio.run(get_available_tools())

# Header
col1, col2 = st.columns([1, 2])
with col1:
    if st.button("🌓" if st.session_state.dark_mode else "☀️", key="theme", use_container_width=False):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()
with col2:
    st.markdown(f'<div class="header"><div class="logo">⛅ Weather Intelligence</div></div>', unsafe_allow_html=True)

# Main content
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown('<div class="card"><div class="title">Check Weather Alerts</div>', unsafe_allow_html=True)
    
    state_code = st.text_input("State Code", placeholder="CA", max_chars=2, key="state", label_visibility="collapsed").upper()
    
    # Auto-fetch when state code is entered
    if state_code and len(state_code) == 2:
        if 'last_state' not in st.session_state or st.session_state.last_state != state_code:
            with st.spinner("Loading..."):
                alerts = asyncio.run(get_alerts(state_code))
                st.session_state.alerts_data = {
                    'state': state_code,
                    'alerts': alerts,
                    'time': datetime.now().strftime('%I:%M%p')
                }
                st.session_state.last_state = state_code
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Show available tools
    if st.session_state.available_tools:
        st.markdown('<div class="card"><div class="title">Available Tools</div>', unsafe_allow_html=True)
        for tool in st.session_state.available_tools:
            st.markdown(f"""
            <div style="background: {colors['input_bg']}; padding: 0.8rem; border-radius: 8px; margin-bottom: 0.5rem;">
                <div style="font-weight: 600; color: {colors['accent']};">{tool['name']}</div>
                <div style="font-size: 0.85rem; color: {colors['secondary']};">{tool['description']}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    if st.session_state.alerts_data:
        alerts_text = st.session_state.alerts_data['alerts']
        individual_alerts = alerts_text.split("---") if "---" in alerts_text else [alerts_text]
        num_alerts = len([a for a in individual_alerts if a.strip() and "No active" not in a and "Error" not in a])
        
        # Stats
        st.markdown(f"""
        <div class="stats">
            <div class="stat"><div class="stat-value">{st.session_state.alerts_data['state']}</div><div class="stat-label">State</div></div>
            <div class="stat"><div class="stat-value">{num_alerts}</div><div class="stat-label">Alerts</div></div>
            <div class="stat"><div class="stat-value">{st.session_state.alerts_data['time']}</div><div class="stat-label">Updated</div></div>
        </div>
        """, unsafe_allow_html=True)
        
        # Alerts
        if "No active alerts" in alerts_text:
            st.markdown('<div class="empty"><div style="font-size: 3rem;">✓</div><div style="font-size: 1.2rem; font-weight: 600;">All Clear</div></div>', unsafe_allow_html=True)
        elif "Error" in alerts_text:
            st.error("Unable to fetch alerts")
        else:
            for alert in individual_alerts:
                if alert.strip():
                    data = parse_alert(alert)
                    severity_class, icon = get_severity(data.get('Severity', 'Unknown'))
                    
                    st.markdown(f"""
                    <div class="alert {severity_class}">
                        <div class="alert-title">{icon} {data.get('Event', 'Alert')}</div>
                        <div class="alert-text">📍 {data.get('Area', 'Unknown')}</div>
                        <div class="alert-text">⚠️ {data.get('Severity', 'Unknown')}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    with st.expander("Details"):
                        st.write(f"**Description:** {data.get('Description', 'N/A')}")
                        st.write(f"**Instructions:** {data.get('Instructions', 'N/A')}")
    else:
        st.markdown('<div class="empty"><div style="font-size: 3rem;">🔍</div><div style="font-size: 1.2rem; font-weight: 600;">Ready to Search</div></div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)