# IDAI1041000467-Tejasvi-Reddy-Kandimalla

Unit 4- Building Streamlit Web Apps for visualizing  Space Rocket Paths and Smart Elevators pathways

Tejasvi Reddy Kandimalla

Candidate Registration Number- 1000467

CRS Name: Artificial Intelligence

Course Name - Mathematics for AI I

School Name - Birla Open Minds International School, Kollur


Live app link: https://idai1041000467-tejasvi-reddy-kandimalla-skxrx52bkhrutvq7f9jk6x.streamlit.app/


**Project Overview**

This project is a comprehensive data science and physics-based application designed to analyze historical space mission data and simulate rocket flight dynamics. The objective is to evaluate how variables like Payload Weight, Fuel Consumption, and Engine Thrust impact mission success and altitude performance.

The project is divided into two core components:

Exploratory Data Analysis (EDA): A dashboard visualizing trends from a historical dataset of space launches.

Physics Simulation: A flight model based on differential equations and Newton’s laws of motion.


**Data Preprocessing & Cleaning**

Before analysis, the raw dataset underwent a rigorous cleaning process using pandas to ensure mathematical consistency:

Type Conversion: Columns such as Mission Cost, Payload, and Fuel were converted from strings to numeric float64 types.

DateTime Normalization: The Launch Date column was transformed into Python datetime objects to allow for chronological filtering.

Handling Missing Values: Rows with null values in critical parameters (Success Rate, Weight) were dropped to prevent skewed statistical results.

Unit Standardization: All headers were stripped of hidden whitespace to ensure "Key-Error" free coding.

Code used to clean data

<img width="1807" height="695" alt="image" src="https://github.com/user-attachments/assets/ceb45d19-a1e5-4e47-93b1-d18baf17c123" />


**Mathematical Physics Simulation**

The simulation module calculates a rocket's trajectory using Euler’s method to solve differential equations of motion.

1. The Force Equation
We apply Newton's Second Law ($F = ma$) to determine acceleration $$a = \frac{T_{total} - (m \cdot g)}{m}$$

Where:

$T_{total}$:Engine Thrust (converted from $kN$ to Newtons).

$m$: Instantaneous mass of the rocket (Base Mass + Current Fuel).

$g$: Acceleration due to gravity ($9.81 m/s^2$).


2. Variable Mass Logic

Unlike a static object, a rocket becomes lighter as it ascends. My code updates the mass at every 1-second interval:

$$m_{t+1} = m_t - (Burn Rate \times \Delta t)$$

As mass decreases, the Thrust-to-Weight ratio increases, causing the rocket to accelerate faster the higher it goes—a phenomenon accurately captured in the interactive line chart.


**Compulsory Visualizations & Insights**

The dashboard includes five mandatory visualizations, each serving a specific analytical purpose:

**Payload Weight vs. Fuel Consumption (Seaborn Scatter):**

Observation: Shows a strong positive correlation ($r \approx 0.85$).

Insight: Heavier payloads require exponential increases in fuel, justifying the shift toward reusable "Heavy" launch vehicles.


**Mission Cost: Success vs. Failure (Plotly Bar):**

Observation: Compares the average budget of successful missions against failures.

Insight: Higher budgets often correlate with higher success, but "Failed" missions still represent billions in lost investment.


**Mission Duration vs. Distance from Earth (Seaborn Line):**

Observation: A linear trend that helps predict mission lifespan based on target destination (Moon vs. Mars).


**Crew Size vs. Mission Outcome (Plotly Box Plot):**

Observation: Analyzes if larger crews impact the likelihood of success.

Insight: Crewed missions tend to have higher success rates due to more rigorous pre-flight safety checks.


**Scientific Yield vs. Mission Cost (Matplotlib Scatter):**

Observation: Measures "Value for Money" (ROI).
