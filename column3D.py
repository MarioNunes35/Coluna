import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.title("🌌 3D Dashboard Test")

# Simple test data
x = [1, 2, 3, 4, 5]
y = [1, 4, 2, 8, 5]
z = [1, 2, 3, 2, 4]

# Create 3D scatter plot
fig = go.Figure(data=go.Scatter3d(
    x=x, y=y, z=z,
    mode='markers',
    marker=dict(
        size=12,
        color=z,
        colorscale='Viridis',
        opacity=0.8
    )
))

fig.update_layout(
    title='Simple 3D Test',
    scene=dict(
        xaxis_title='X Axis',
        yaxis_title='Y Axis',
        zaxis_title='Z Axis'
    ),
    height=500
)

st.plotly_chart(fig, use_container_width=True)

if st.button("Test Button"):
    st.success("Deployment is working! ✅")
