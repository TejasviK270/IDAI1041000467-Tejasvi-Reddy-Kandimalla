import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Set Page Title
st.set_page_config(page_title="Rocket Launch Analytics")

# 1. Load the cleaned data 
# Ensure 'cleaned_rocket_missions.csv' is in the same folder as this script
@st.cache_data
def load_data():
    df = pd.read_csv('cleaned_rocket_missions.csv')
    return df

df = load_data()

# 2. Sidebar Controls (Interactivity) 
st.sidebar.header("Filter Missions")
cost_filter = st.sidebar.slider("Select Max Mission Cost (Billion USD)", 
                                min_value=float(df['Mission Cost (billion USD)'].min()), 
                                max_value=float(df['Mission Cost (billion USD)'].max()), 
                                value=float(df['Mission Cost (billion USD)'].max()))

filtered_df = df[df['Mission Cost (billion USD)'] <= cost_filter]

# 3. Main Dashboard UI
st.title("🚀 Rocket Launch Path Visualization")
st.markdown("Exploring the relationship between resources, costs, and success rates. ")

# --- Visualization 1: Scatter Plot (Interactive) ---
st.subheader("Payload Weight vs. Fuel Consumption ")
fig1 = px.scatter(filtered_df, x='Payload Weight (tons)', y='Fuel Consumption (tons)', 
                 color='Mission Success (%)', hover_name='Mission Name',
                 title="How Payload impacts Fuel Needs")
st.plotly_chart(fig1)

# --- Visualization 2: Bar Chart ---
st.subheader("Average Mission Cost: Success vs. Failure ")
# Create status column for visualization
filtered_df['Status'] = filtered_df['Mission Success (%)'].apply(lambda x: 'Success' if x > 50 else 'Failure')
fig2 = px.bar(filtered_df, x='Status', y='Mission Cost (billion USD)', 
             title="Financial Comparison of Mission Outcomes", barmode='group')
st.plotly_chart(fig2)

# --- Visualization 3: Correlation Heatmap ---
st.subheader("Factor Correlation Heatmap ")
fig3, ax = plt.subplots()
numeric_df = filtered_df.select_dtypes(include=['number'])
sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', ax=ax)
st.pyplot(fig3)
