import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import tempfile
import base64
import os
import matplotlib as mpl

# Use standard English font
mpl.rcParams['font.family'] = 'Arial'
mpl.rcParams['axes.unicode_minus'] = False

# Title
st.title("🌍 Kepler's Law: Elliptical Orbit Simulation")

# User input
a = st.number_input("Semi-major axis a (AU)", min_value=0.1, max_value=10.0, value=1.0, step=0.1)
b = st.number_input("Semi-minor axis b (AU)", min_value=0.1, max_value=a, value=0.8, step=0.1)

# Eccentricity and focal distance
e = np.sqrt(1 - (b**2 / a**2))
c = a * e  # Distance from center to focus

# 🧮 Kepler's 3rd law: T^2 ∝ a^3 → T = sqrt(a^3)
T = np.sqrt(a**3)  # Orbital period in years
st.write(f"🕒 Estimated Orbital Period (Kepler's 3rd Law): **{T:.2f} years**")

# Elliptical orbit centered, shifted so star is at origin
theta = np.linspace(0, 2 * np.pi, 1000)
x_orbit = a * np.cos(theta) - c
y_orbit = b * np.sin(theta)

# Kepler's equation solver
def solve_kepler(M, e):
    E = M
    for _ in range(10):
        E -= (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
    return E

# Planet position over time
t = np.linspace(0, 2 * np.pi, 300)
M = t
E = np.array([solve_kepler(Mi, e) for Mi in M])
theta_planet = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2),
                              np.sqrt(1 - e) * np.cos(E / 2))
r = a * (1 - e**2) / (1 + e * np.cos(theta_planet))
x_planet = r * np.cos(theta_planet)
y_planet = r * np.sin(theta_planet)

# Plot
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_aspect('equal')
ax.plot(x_orbit, y_orbit, 'b-', label='Elliptical Orbit')
ax.plot([0], [0], 'yo', markersize=15, label='Star (Focus)')
planet, = ax.plot([], [], 'ro', markersize=10, label='Planet')
ax.legend()
ax.set_xlabel('X (AU)')
ax.set_ylabel('Y (AU)')
ax.set_title("Planetary Motion with Kepler's Laws")
ax.grid(True)

# Show orbital period on plot
ax.text(0.05, 0.95, f"Period ≈ {T:.2f} years", transform=ax.transAxes,
        fontsize=12, color='black', verticalalignment='top', bbox=dict(facecolor='white', alpha=0.6))

# Auto axis limits
x_min = np.min(x_orbit) - 0.1 * a
x_max = np.max(x_orbit) + 0.1 * a
y_min = np.min(y_orbit) - 0.1 * b
y_max = np.max(y_orbit) + 0.1 * b
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)

# Animation
def update(frame):
    planet.set_data([x_planet[frame]], [y_planet[frame]])
    return planet,

ani = FuncAnimation(fig, update, frames=len(t), interval=40, blit=True)

# GIF output
def get_animation_html(ani):
    try:
        with tempfile.NamedTemporaryFile(suffix='.gif', delete=False) as tmp_file:
            ani.save(tmp_file.name, writer=PillowWriter(fps=25))
            tmp_file.flush()
        with open(tmp_file.name, 'rb') as f:
            gif = f.read()
        os.remove(tmp_file.name)
        return f'<img src="data:image/gif;base64,{base64.b64encode(gif).decode()}" width="600"/>'
    except Exception as e:
        st.error(f"Error saving animation: {str(e)}")
        return None

# Display GIF in Streamlit
html = get_animation_html(ani)
if html:
    st.markdown(html, unsafe_allow_html=True)
else:
    st.warning("Failed to generate animation.")

plt.close(fig)
