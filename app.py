import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np

# Set Page Configuration
st.set_page_config(page_title="Rocket Launch Analytics Dashboard", layout="wide")

# --- STAGE 2: DATA LOADING & CLEANING ---
@st.cache_data
def load_and_clean():
    # Ensure this filename matches your uploaded file
    df = pd.read_csv('cleaned_rocket_missions.csv')
    df.columns = df.columns.str.strip()
    
    # Convert launch dates to proper date format
    df['Launch Date'] = pd.to_datetime(df['Launch Date'], errors='coerce')
    
    # Ensure numeric columns are in the correct number type
    numeric_cols = [
        'Mission Cost (billion USD)', 'Payload Weight (tons)', 
        'Fuel Consumption (tons)', 'Mission Duration (years)',
        'Distance from Earth (light-years)', 'Scientific Yield (points)',
        'Crew Size', 'Mission Success (%)'
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df.dropna(subset=['Payload Weight (tons)', 'Fuel Consumption (tons)'])

df = load_and_clean()

# --- SIDEBAR: INTERACTIVE CONTROLS ---
st.sidebar.header("Dashboard Filters")

# UPDATED: Slider starts from 2025
# We set the min_value to 2025 and the max_value to 2035 (or whatever your data supports)
start_year = 2025
end_year = 2035 

year_range = st.sidebar.slider(
    "Select Launch Year Range", 
    min_value=start_year, 
    max_value=end_year, 
    value=(2025, 2030) # Default selection range
)

# 2. Checkbox filters for Mission Type
st.sidebar.subheader("Mission Type")
unique_missions = df['Mission Type'].unique()
selected_missions = []
for mission in unique_missions:
    if st.sidebar.checkbox(mission, value=True):
        selected_missions.append(mission)

# Filter the dataset based on sidebar inputs
filtered_df = df[(df['Launch Date'].dt.year >= year_range[0]) & 
                 (df['Launch Date'].dt.year <= year_range[1]) &
                 (df['Mission Type'].isin(selected_missions))]

st.title("🚀 Rocket Launch Path Visualization & Analytics")

# --- STAGE 3: PHYSICS SIMULATION ---
st.header("Stage 3: Rocket Launch Physics Simulation")
st.markdown("Calculate acceleration as the difference between thrust and downward forces ($F=ma$).")

with st.expander("Adjust Simulation Parameters"):
    c1, c2 = st.columns(2)
    with c1:
        thrust_kn = st.slider("Engine Thrust (kN)", 1000, 8000, 5000)
        rocket_m = st.number_input("Rocket Base Mass (kg)", value=50000)
    with c2:
        fuel_m = st.number_input("Initial Fuel Mass (kg)", value=40000)
        burn_rate = st.slider("Fuel Burn Rate (kg/s)", 50, 500, 150)

def run_sim(m_r, m_f, t_kn, rate):
    g = 9.81
    dt = 1.0
    results = []
    v, h, curr_f = 0.0, 0.0, m_f
    thrust_n = t_kn * 1000 # Convert kN to Newtons
    
    for t in range(200):
        total_m = m_r + curr_f
        if curr_f > 0:
            accel = (thrust_n - (total_m * g)) / total_m
            curr_f = max(0, curr_f - rate)
        else:
            accel = -g
        
        v += accel * dt
        h = max(0, h + v * dt)
        results.append({"Time (s)": t, "Altitude (m)": h, "Velocity (m/s)": v, "Fuel (kg)": curr_f})
    return pd.DataFrame(results)

sim_results = run_sim(rocket_m, fuel_m, thrust_kn, burn_rate)
st.line_chart(sim_results, x="Time (s)", y="Altitude (m)")

# --- STAGE 4: COMPULSORY VISUALIZATIONS ---
st.header("Stage 4: Mission Data Insights")

# 1. Scatter Plot: Payload vs. Fuel
fig1 = px.scatter(filtered_df, x='Payload Weight (tons)', y='Fuel Consumption (tons)', 
                 color='Mission Success (%)', title="1. Payload Weight vs. Fuel Consumption")
st.plotly_chart(fig1, use_container_width=True)

# 2. Bar Chart: Cost Success vs Failure
filtered_df['Outcome'] = filtered_df['Mission Success (%)'].apply(lambda x: 'Success' if x >= 80 else 'Failure')
fig2 = px.bar(filtered_df, x='Outcome', y='Mission Cost (billion USD)', color='Outcome', 
             title="2. Mission Cost: Success vs. Failure")
st.plotly_chart(fig2, use_container_width=True)

col_a, col_b = st.columns(2)
with col_a:
    # 3. Line Chart: Duration vs Distance
    fig3 = px.line(filtered_df.sort_values('Distance from Earth (light-years)'), 
                  x='Distance from Earth (light-years)', y='Mission Duration (years)', 
                  title="3. Duration vs. Distance")
    st.plotly_chart(fig3)

with col_b:
    # 4. Box Plot: Crew Size vs Success %
    fig4 = px.box(filtered_df, x='Outcome', y='Crew Size', title="4. Crew Size vs. Mission Outcome")
    st.plotly_chart(fig4)

# 5. Scatter Chart: Scientific Yield vs Cost
fig5 = px.scatter(filtered_df, x='Mission Cost (billion USD)', y='Scientific Yield (points)', 
                 size='Payload Weight (tons)', color='Launch Vehicle', 
                 title="5. Scientific Yield vs. Mission Cost")
st.plotly_chart(fig5, use_container_width=True)

# Heatmap
st.subheader("Correlation Heatmap: Factors Relating to Success")
fig6, ax = plt.subplots()
sns.heatmap(filtered_df.select_dtypes(include=[np.number]).corr(), annot=True, cmap='coolwarm', ax=ax)
st.pyplot(fig6)
