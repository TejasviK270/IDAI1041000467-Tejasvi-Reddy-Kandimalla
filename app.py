import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Set Page Configuration
st.set_page_config(page_title="Rocket Launch Analytics Dashboard", layout="wide")

# --- STAGE 2: DATA LOADING & CLEANING ---
@st.cache_data
def load_and_clean():
    # Load the cleaned dataset 
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
    
    return df.dropna(subset=['Payload Weight (tons)', 'Fuel Consumption (tons)', 'Mission Success (%)'])

df = load_and_clean()

# --- SIDEBAR: INTERACTIVE CONTROLS  ---
st.sidebar.header("Dashboard Filters")

# Filter by Year (st.slider) 
year_range = st.sidebar.slider("Select Launch Year Range", 
                               int(df['Launch Date'].dt.year.min(2024)), 
                               int(df['Launch Date'].dt.year.max()), 
                    

# Filter by Mission Type (Checkboxes) 
st.sidebar.subheader("Mission Type")
unique_missions = df['Mission Type'].unique()
selected_missions = []
for mission in unique_missions:
    if st.sidebar.checkbox(mission, value=True):
        selected_missions.append(mission)

# Apply filters
filtered_df = df[(df['Launch Date'].dt.year >= year_range[0]) & 
                 (df['Launch Date'].dt.year <= year_range[1]) &
                 (df['Mission Type'].isin(selected_missions))]

st.title("🚀 Rocket Launch Path Visualization & Analytics")

# --- STAGE 3: PHYSICS SIMULATION  ---
st.header("Stage 3: Rocket Launch Physics Simulation")
st.markdown("Calculating altitude using Newton’s Second Law: $Acceleration = (Thrust - Weight) / Mass$ ")

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
            # Acceleration calculation 
            accel = (thrust_n - (total_m * g)) / total_m
            curr_f = max(0, curr_f - rate)
        else:
            accel = -g # Gravity takes over
        
        v += accel * dt
        h = max(0, h + v * dt)
        results.append({"Time (s)": t, "Altitude (m)": h})
    return pd.DataFrame(results)

sim_data = run_sim(rocket_m, fuel_m, thrust_kn, burn_rate)
st.line_chart(sim_data, x="Time (s)", y="Altitude (m)")

# --- STAGE 4: COMPULSORY VISUALIZATIONS  ---
st.header("Stage 4: Compulsory Mission Visualizations")

# 1. Scatter Plot → Payload Weight vs. Fuel Consumption (Seaborn) 
st.subheader("1. Payload Weight vs. Fuel Consumption")
fig1, ax1 = plt.subplots(figsize=(10, 5))
sns.scatterplot(data=filtered_df, x='Payload Weight (tons)', y='Fuel Consumption (tons)', 
                hue='Mission Success (%)', palette='viridis', ax=ax1)
ax1.set_title("Payload vs. Fuel (Seaborn)")
st.pyplot(fig1)

# 2. Bar Chart → Mission Cost: Success vs. Failure (Plotly) 
st.subheader("2. Mission Cost: Success vs. Failure")
filtered_df['Outcome'] = filtered_df['Mission Success (%)'].apply(lambda x: 'Success' if x >= 80 else 'Failure')
fig2 = px.bar(filtered_df, x='Outcome', y='Mission Cost (billion USD)', 
             color='Outcome', title="Mission Cost Comparison (Plotly)")
st.plotly_chart(fig2, use_container_width=True)

# 3. Line Chart → Mission Duration vs. Distance from Earth (Seaborn) 
st.subheader("3. Mission Duration vs. Distance from Earth")
fig3, ax3 = plt.subplots(figsize=(10, 5))
sns.lineplot(data=filtered_df.sort_values('Distance from Earth (light-years)'), 
             x='Distance from Earth (light-years)', y='Mission Duration (years)', ax=ax3)
ax3.set_title("Duration vs. Distance (Seaborn)")
st.pyplot(fig3)

col_left, col_right = st.columns(2)

with col_left:
    # 4. Box Plot → Crew Size vs. Mission Success % (Plotly) 
    st.subheader("4. Crew Size vs. Mission Outcome")
    fig4 = px.box(filtered_df, x='Outcome', y='Crew Size', 
                  points="all", title="Crew Size Distribution (Plotly)")
    st.plotly_chart(fig4)

with col_right:
    # 5. Scatter/Bar Chart → Scientific Yield vs. Mission Cost (Matplotlib) 
    st.subheader("5. Scientific Yield vs. Mission Cost")
    fig5, ax5 = plt.subplots()
    ax5.scatter(filtered_df['Mission Cost (billion USD)'], filtered_df['Scientific Yield (points)'], alpha=0.5)
    ax5.set_xlabel("Cost (billion USD)")
    ax5.set_ylabel("Scientific Yield (points)")
    ax5.set_title("Yield vs. Cost (Matplotlib)")
    st.pyplot(fig5)

# Bonus: Correlation Heatmap 
st.subheader("Correlation Heatmap: Success Factors")
fig6, ax6 = plt.subplots()
sns.heatmap(filtered_df.select_dtypes(include=[np.number]).corr(), annot=True, cmap='RdBu', ax=ax6)
st.pyplot(fig6)
