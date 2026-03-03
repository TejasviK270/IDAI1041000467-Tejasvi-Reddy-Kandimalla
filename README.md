# IDAI1041000467-Tejasvi-Reddy-Kandimalla

Live app link: https://idai1041000467-tejasvi-reddy-kandimalla-skxrx52bkhrutvq7f9jk6x.streamlit.app/


**Project Overview**

This project was developed to bridge the gap between historical mission data and predictive physics simulations. By analyzing a dataset of over [X number of missions], I have created a tool that helps visualize how payload, fuel, and cost influence the success of a rocket launch.


**The Physics of Flight**

The core of this application is a Numerical Integration Simulation of a rocket launch. Unlike a simple static graph, this simulation uses a step-by-step approach to solve for the rocket's position:

Force Balance: 

I calculated acceleration using the formula:
$$a = \frac{T - (m \cdot g)}{m}$$

Where $T$ is Thrust in Newtons, $m$ is the instantaneous mass, and $g$ is gravity (9.81 $m/s^2$).

Variable Mass: A critical feature of this simulation is the Mass-Reduction model. As fuel burns, the total mass ($m$) decreases, which causes the acceleration to increase over time—mimicking real-world rocket behavior.

Euler's Method: At each 1-second interval, the velocity and altitude are updated based on the acceleration of the previous step.



Mission Data Insights

Using a combination of Seaborn, Plotly, and Matplotlib, I extracted several key findings from the mission dataset:

Fuel Efficiency: The scatter plot confirms a high correlation between payload weight and fuel consumption, justifying the need for multi-stage rockets for heavy satellites.

Economics of Space: The bar charts indicate that while higher costs generally correlate with more complex missions, they do not strictly guarantee a higher success percentage, suggesting that mission architecture is more vital than raw budget.

Crew Dynamics: The box plots reveal the distribution of crew sizes across different mission types, showing that crewed missions are generally more resource-heavy but have high scientific yields.


Code used to clean data

<img width="1807" height="695" alt="image" src="https://github.com/user-attachments/assets/ceb45d19-a1e5-4e47-93b1-d18baf17c123" />
