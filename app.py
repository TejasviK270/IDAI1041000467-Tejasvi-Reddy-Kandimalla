import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Page Configuration
st.set_page_config(page_title="Rocket Path & Mission Analytics", layout="wide")

# --- STAGE 2 & 4: DATA LOADING ---
@st.cache_data
def load_and_clean_data():
    # Load your cleaned dataset
    df = pd.read_csv('cleaned_rocket_missions.csv')
    df.columns = df.columns.str.strip()
    return df

df = load_and_clean_data()

# --- SIDEBAR FILTERS ---
st.sidebar.header("Dashboard Filters")
mission_type = st.sidebar.selectbox("Select Mission Type", options=["All"] + list(df['Mission Type'].unique()))
dist_range = st.sidebar.slider("Distance from Earth (light-years)", 
                               int(df['Distance from Earth (light-years)'].min()), 
                               int(df['Distance from Earth (light-years)'].max()), 
                               (0, 500))

# Filter data based on selection
plot_df = df[(df['Distance from Earth (light-years)'] >= dist_range[0]) & 
            (df['Distance from Earth (light-years)'] <= dist_range[1])]
if mission_type != "All":
    plot_df = plot_df[plot_df['Mission Type'] == mission_type]

st.title("🚀 Space Rocket Path & Mission Analytics")

# --- STAGE 3: ROCKET LAUNCH SIMULATION ---
st.header("Stage 3: Rocket Launch Physics Simulation")
with st.expander("Adjust Simulation Parameters"):
    col1, col2 = st.columns(2)
    with col1:
        thrust = st.slider("Engine Thrust (kN)", 1000, 5000, 3000)
        rocket_mass = st.number_input("Initial Rocket Mass (kg)", value=50000)
    with col2:
        fuel_mass = st.number_input("Fuel Mass (kg)", value=30000)
        burn_rate = st.slider("Fuel Burn Rate (kg/s)", 10, 500, 100)

def run_simulation(m_rocket, m_fuel, force_thrust, rate):
    # Initial conditions
    g = 9.8  # Gravity 
    dt = 1.0 # Time step 
    time_steps = 200 # 
    
    results = []
    v = 0.0  # Velocity
    h = 0.0  # Altitude
    current_fuel = m_fuel
    
    for t in range(time_steps):
        current_total_mass = m_rocket + current_fuel
        
        if current_fuel > 0:
            # Acceleration = (Thrust - Weight) / Mass 
            accel = ((force_thrust * 1000) - (current_total_mass * g)) / current_total_mass
            current_fuel -= rate
        else:
            accel = -g # Falling under gravity 
            
        v += accel * dt # Update velocity 
        h += v * dt     # Update altitude 
        
        # Prevent rocket from going underground
        if h < 0: h = 0; v = 0 
            
        results.append({"Time": t, "Altitude": h, "Velocity": v, "Fuel": max(0, current_fuel)})
    return pd.DataFrame(results)

sim_data = run_simulation(rocket_mass, fuel_mass, thrust, burn_rate)
st.line_chart(sim_data, x="Time", y="Altitude", use_container_width=True)

# --- STAGE 4: COMPULSORY VISUALIZATIONS ---
st.header("Stage 4: Real-World Mission Insights")

row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.subheader("1. Payload vs. Fuel Consumption") # 
    fig1 = px.scatter(plot_df, x='Payload Weight (tons)', y='Fuel Consumption (tons)', 
                     color='Mission Success (%)', title="Seaborn-style Scatter")
    st.plotly_chart(fig1)

with row1_col2:
    st.subheader("2. Cost: Success vs. Failure") # 
    plot_df['Outcome'] = plot_df['Mission Success (%)'].apply(lambda x: 'Success' if x > 50 else 'Failure')
    fig2 = px.bar(plot_df, x='Outcome', y='Mission Cost (billion USD)', color='Outcome',
                 title="Matplotlib/Plotly Bar Chart")
    st.plotly_chart(fig2)

row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.subheader("3. Duration vs. Distance") # 
    fig3 = px.line(plot_df.sort_values('Distance from Earth (light-years)'), 
                  x='Distance from Earth (light-years)', y='Mission Duration (years)')
    st.plotly_chart(fig3)

with row2_col2:
    st.subheader("4. Crew Size vs. Success %") # 
    fig4 = px.box(plot_df, x='Outcome', y='Crew Size', title="Seaborn-style Boxplot")
    st.plotly_chart(fig4)

st.subheader("5. Scientific Yield vs. Mission Cost") # 
fig5 = px.scatter(plot_df, x='Mission Cost (billion USD)', y='Scientific Yield (points)', 
                 size='Crew Size', color='Launch Vehicle', hover_name='Mission Name')
st.plotly_chart(fig5, use_container_width=True)
