import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import tempfile
import base64
import os

# Streamlit 앱 제목
st.title("케플러 법칙에 따른 행성 운동 시뮬레이션")

# 사용자 입력: 긴반지름(a)과 짧은반지름(b)
st.write("타원 궤도의 긴반지름(a)과 짧은반지름(b)을 입력하세요 (단위: 천문단위, AU):")
a = st.number_input("긴반지름 (a)", min_value=0.1, max_value=10.0, value=1.0, step=0.1)
b = st.number_input("짧은반지름 (b)", min_value=0.1, max_value=a, value=0.5, step=0.1)

# 이심률과 초점 거리
e = np.sqrt(1 - (b**2 / a**2))  # 이심률
c = a * e  # 초점 거리

# 궤도 중심 기준 좌표
theta = np.linspace(0, 2 * np.pi, 1000)
x_orbit = a * np.cos(theta)
y_orbit = b * np.sin(theta)

# 행성 궤도 계산 (항성이 초점 (–c, 0)에 위치)
def solve_kepler(M, e):
    E = M
    for _ in range(10):
        E -= (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
    return E

t = np.linspace(0, 2 * np.pi, 200)
M = t
E = np.array([solve_kepler(Mi, e) for Mi in M])
theta_planet = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2),
                              np.sqrt(1 - e) * np.cos(E / 2))
r = a * (1 - e**2) / (1 + e * np.cos(theta_planet))
x_planet = r * np.cos(theta_planet)
y_planet = r * np.sin(theta_planet)

# 중심 기준 좌표에서 초점 기준으로 평행이동 (항성을 –c로)
x_orbit -= c
x_planet -= c

# 그래프 그리기
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_aspect('equal')
ax.plot(x_orbit, y_orbit, 'b-', label='타원 궤도')
ax.plot([-c], [0], 'yo', markersize=15, label='항성')  # 초점(–c, 0)
planet, = ax.plot([], [], 'ro', markersize=10, label='행성')
ax.legend()
ax.set_xlabel('X (AU)')
ax.set_ylabel('Y (AU)')
ax.set_title('케플러 법칙에 따른 행성 운동')
ax.grid(True)
ax.set_xlim(-1.5 * a, 1.5 * a)
ax.set_ylim(-1.5 * b, 1.5 * b)

# 애니메이션 프레임 업데이트 함수
def update(frame):
    planet.set_data([x_planet[frame]], [y_planet[frame]])
    return planet,

ani = FuncAnimation(fig, update, frames=len(t), interval=50, blit=True)

# 애니메이션을 gif로 저장하여 표시
def get_animation_html(ani):
    try:
        with tempfile.NamedTemporaryFile(suffix='.gif', delete=False) as tmp_file:
            tmp_path = tmp_file.name
            ani.save(tmp_path, writer=PillowWriter(fps=20))
        with open(tmp_path, 'rb') as f:
            video = f.read()
        os.remove(tmp_path)
        video_base64 = base64.b64encode(video).decode()
        return f'<img src="data:image/gif;base64,{video_base64}" width="600"/>'
    except Exception as e:
        st.error(f"애니메이션 저장 중 오류 발생: {str(e)}")
        return None

# 애니메이션 표시
html = get_animation_html(ani)
if html:
    st.markdown(html, unsafe_allow_html=True)
else:
    st.warning("애니메이션 생성에 실패했습니다. `pillow>=9.0.0`, `matplotlib>=3.5.0`이 설치되어 있는지 확인하세요.")

plt.close(fig)
