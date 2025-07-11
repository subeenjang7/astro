import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import tempfile
import base64
import os
import matplotlib as mpl

mpl.rcParams['font.family'] = 'Arial'
mpl.rcParams['axes.unicode_minus'] = False

# 페이지 선택
page = st.sidebar.selectbox("Select Page", ["Custom Orbit Simulation", "Solar System Simulation"])

# 🌍 Page 1: 사용자 궤도 시뮬레이션
if page == "Custom Orbit Simulation":
    st.title("🌍 Kepler's Law: Custom Elliptical Orbit")

    a = st.number_input("Semi-major axis a (AU)", min_value=0.1, max_value=10.0, value=1.0, step=0.1)
    b = st.number_input("Semi-minor axis b (AU)", min_value=0.1, max_value=a, value=0.8, step=0.1)
    e = np.sqrt(1 - (b**2 / a**2))
    c = a * e
    T = np.sqrt(a**3)
    st.write(f"🕒 Estimated Orbital Period: **{T:.2f} years**")

    theta = np.linspace(0, 2 * np.pi, 1000)
    x_orbit = a * np.cos(theta) - c
    y_orbit = b * np.sin(theta)

    def solve_kepler(M, e):
        E = M
        for _ in range(10):
            E -= (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
        return E

    t = np.linspace(0, 2 * np.pi, 300)
    M = t
    E = np.array([solve_kepler(Mi, e) for Mi in M])
    theta_planet = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2),
                                  np.sqrt(1 - e) * np.cos(E / 2))
    r = a * (1 - e**2) / (1 + e * np.cos(theta_planet))
    x_planet = r * np.cos(theta_planet)
    y_planet = r * np.sin(theta_planet)

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_aspect('equal')
    ax.plot(x_orbit, y_orbit, 'b-', label='Elliptical Orbit')
    ax.plot([0], [0], 'yo', markersize=15, label='Star (Focus)')
    planet, = ax.plot([], [], 'ro', markersize=10, label='Planet')
    ax.legend()
    ax.set_xlabel('X (AU)')
    ax.set_ylabel('Y (AU)')
    ax.set_title("Custom Planetary Orbit")
    ax.grid(True)

    ax.text(0.05, 0.95, f"Period ≈ {T:.2f} years", transform=ax.transAxes,
            fontsize=12, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.6))

    ax.set_xlim(np.min(x_orbit) - 0.1 * a, np.max(x_orbit) + 0.1 * a)
    ax.set_ylim(np.min(y_orbit) - 0.1 * b, np.max(y_orbit) + 0.1 * b)

    def update(frame):
        planet.set_data([x_planet[frame]], [y_planet[frame]])
        return planet,

    ani = FuncAnimation(fig, update, frames=len(t), interval=40, blit=True)

# ☀️ Page 2: 태양계 행성 궤도 시뮬레이션
else:
    st.title("☀️ Solar System Simulation Based on Kepler's Laws")

    # 실제 태양계 행성 데이터 (a: AU, T: years)
    planet_data = [
        {"name": "Mercury", "a": 0.39, "T": 0.24, "color": "gray"},
        {"name": "Venus",   "a": 0.72, "T": 0.62, "color": "orange"},
        {"name": "Earth",   "a": 1.00, "T": 1.00, "color": "blue"},
        {"name": "Mars",    "a": 1.52, "T": 1.88, "color": "red"},
        {"name": "Jupiter", "a": 5.20, "T": 11.86, "color": "brown"},
        {"name": "Saturn",  "a": 9.58, "T": 29.46, "color": "gold"},
        {"name": "Uranus",  "a": 19.2, "T": 84.01, "color": "lightblue"},
        {"name": "Neptune", "a": 30.1, "T": 164.8, "color": "darkblue"},
    ]

    total_frames = 300
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_aspect('equal')
    ax.set_xlim(-32, 32)
    ax.set_ylim(-32, 32)
    ax.set_title("Keplerian Orbits of Solar System Planets")
    ax.set_xlabel("X (AU)")
    ax.set_ylabel("Y (AU)")
    ax.grid(True)
    ax.plot([0], [0], 'yo', markersize=12, label='Sun')

    orbit_lines = []
    planet_dots = []
    labels = []

    for planet in planet_data:
        a = planet["a"]
        T = planet["T"]
        theta = np.linspace(0, 2 * np.pi, 1000)
        x_orbit = a * np.cos(theta)
        y_orbit = a * np.sin(theta)  # 원형 궤도로 단순화
        line, = ax.plot(x_orbit, y_orbit, color=planet["color"], linestyle='--', alpha=0.5)
        dot, = ax.plot([], [], 'o', color=planet["color"], label=planet["name"])
        label = ax.text(a, 0.1, "", fontsize=8, ha='left')
        orbit_lines.append(line)
        planet_dots.append(dot)
        labels.append(label)

    ax.legend(loc='upper right', fontsize=8)

    def update(frame):
        for i, planet in enumerate(planet_data):
            a = planet["a"]
            T = planet["T"]
            angle = 2 * np.pi * (frame / total_frames) * (1 / T)
            x = a * np.cos(angle)
            y = a * np.sin(angle)
            planet_dots[i].set_data([x], [y])
            labels[i].set_position((x + 0.2, y))
            labels[i].set_text(planet["name"])
        return planet_dots + labels

    ani = FuncAnimation(fig, update, frames=total_frames, interval=50, blit=True)

# GIF 변환 및 출력 (두 페이지 공통)
def get_animation_html(ani):
    try:
        with tempfile.NamedTemporaryFile(suffix='.gif', delete=False) as tmp_file:
            ani.save(tmp_file.name, writer=PillowWriter(fps=25))
            tmp_file.flush()
        with open(tmp_file.name, 'rb') as f:
            gif = f.read()
        os.remove(tmp_file.name)
        return f'<img src="data:image/gif;base64,{base64.b64encode(gif).decode()}" width="700"/>'
    except Exception as e:
        st.error(f"Error saving animation: {str(e)}")
        return None

html = get_animation_html(ani)
if html:
    st.markdown(html, unsafe_allow_html=True)
else:
    st.warning("Failed to generate animation.")

plt.close(fig)

