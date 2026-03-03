# IDAI1041000467-Tejasvi-Reddy-Kandimalla

Unit 4- Building Streamlit Web Apps for visualizing  Space Rocket Paths and Smart Elevators pathways

Tejasvi Reddy Kandimalla

Candidate Registration Number- 1000467

CRS Name: Artificial Intelligence

Course Name - Mathematics for AI I

School Name - Birla Open Minds International School, Kollur


Live app link: https://idai1041000467-tejasvi-reddy-kandimalla-skxrx52bkhrutvq7f9jk6x.streamlit.app/


**Project Overview**

This project serves as a dual-purpose aerospace tool designed to analyze historical launch data and simulate the physical requirements for achieving orbit. The research objective was to identify how economic factors (Mission Cost) and logistical factors (Payload Weight) correlate with the mathematical probability of mission success.


The application integrates Historical Data Analysis with a Dynamic Physics Engine, allowing users to observe how historical trends (like fuel-to-weight ratios) translate into real-time flight performance through a simulation.


**Research & Data Analysis**


**Guiding Research Questions**

Mass-Fuel Efficiency: How does the increase in payload weight affect fuel consumption across different launch vehicles?

Economic Risk: Does a higher mission budget directly correlate with a higher "Mission Success %"?

Human Factors: How does crew size impact the complexity and duration of deep-space missions?


**Data Cleaning Process**

The raw dataset was processed using the pandas library to ensure mathematical integrity:

Feature Engineering: Converted categorical "Success" metrics into a binary status for easier bar chart comparison.

Type Casting: Transformed mission costs from strings to floating-point numbers to enable statistical correlation.

Outlier Management: Filtered out missions with incomplete "Payload Weight" data to ensure the scatter plots remained accurate for research purposes.

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


**Key Research Findings**

After analyzing the mission dataset and running the flight simulation, the following conclusions were drawn:

**Fuel-Mass Efficiency Ratio**: The scatter plot analysis indicates that for every 1-ton increase in payload, fuel consumption increases by approximately 8-10%. This validates the Tsiolkovsky Rocket Equation, proving that as payload increases, the energy required to lift the extra fuel itself becomes a limiting factor.

**Economic ROI (Scientific Yield)**: There is a "sweet spot" in mission costs between $2 billion and $5 billion. Missions within this budget range showed the highest scientific yield per dollar spent, whereas ultra-expensive missions (> $10 billion) often yielded diminishing returns in terms of purely scientific data.

**Success Factors**: The correlation heatmap identified that Mission Success % is most strongly correlated with Fuel Consumption and Mission Duration, rather than Crew Size. This suggests that automated technical reliability is a stronger predictor of success than human intervention for these specific mission types.

**Simulation Validation**: The simulation proved that with a Thrust-to-Weight Ratio (TWR) of less than 1.2, the rocket fails to gain sufficient altitude before fuel depletion. This highlights the critical nature of engine efficiency in the early launch phase.


**Integration Details** 
This dashboard is a cohesive integration of data science and physics:

1. Mathematical Simulation IntegrationThe simulation is not just a static animation; it is a Numerical Integration model using Euler’s Method.

The Physics Engine: It calculates acceleration ($a$) based on the instantaneous sum of forces ($F_{net} = T - W$).

Integration Logic: 

$$v_{new} = v_{old} + a \cdot \Delta t$$$$h_{new} = h_{old} + v \cdot \Delta t$$


Dynamic Mass: The most critical integration detail is the Fuel Burn Loop. As the simulation runs, the rocket's mass decreases by the burn_rate every second, which realistically increases the acceleration ($a$) as the rocket climbs.


2. Visualization Logic: I integrated three distinct Python libraries to meet the project's visual requirements:

Seaborn/Matplotlib: Used for statistical distributions (Box Plots) and simple trend lines.

Plotly: Integrated to provide Interactivity. Users can hover over data points in the "Scientific Yield vs. Cost" chart to see specific mission names.

Streamlit Sidebar: Integrated as the primary control center, using checkboxes to allow users to isolate specific mission types for targeted research.



**Deployment Instructions**

Visit the Streamlit Cloud link at the top of this README.

Use the Sidebar Checkboxes to filter by mission type.

Adjust the Simulation Sliders to test if a rocket can lift off with your specific mass/thrust settings.
