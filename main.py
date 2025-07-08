import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import io
import base64

# Streamlit 앱 제목
st.title("케플러 법칙에 따른 행성 운동 시뮬레이션")

# 사용자 입력: 긴반지름(a)과 짧은반지름(b)
st.write("타원 궤도의 긴반지름(a)과 짧은반지름(b)을 입력하세요 (단위: 천문단위, AU):")
a = st.number_input("긴반지름 (a)", min_value=0.1, max_value=10.0, value=1.0, step=0.1)
b = st.number_input("짧은반지름 (b)", min_value=0.1, max_value=a, value=0.5, step=0.1)

# 케플러 제2법칙을 위한 설정
# 타원의 이심률 계산: e = sqrt(1 - (b^2 / a^2))
e = np.sqrt(1 - (b**2 / a**2))
# 초점 거리 c = a * e
c = a * e

# 타원 궤도와 행성 위치 계산
theta = np.linspace(0, 2 * np.pi, 100)
x_orbit = a * np.cos(theta)  # 타원 궤도의 x 좌표
y_orbit = b * np.sin(theta)  # 타원 궤도의 y 좌표

# 행성의 운동: 극좌표에서 시간에 따른 위치 계산 (케플러 제2법칙)
# 근점에서 시작한다고 가정
def get_r(theta, a, e):
    return a * (1 - e**2) / (1 + e * np.cos(theta))

# 시간 단계 설정
t = np.linspace(0, 2 * np.pi, 100)  # 한 바퀴 도는 시간
r = get_r(t, a, e)
x_planet = r * np.cos(t)  # 행성의 x 좌표
y_planet = r * np.sin(t)  # 행성의 y 좌표

# 애니메이션 생성
fig, ax = plt.subplots()
ax.set_aspect('equal')
ax.plot(x_orbit, y_orbit, 'b-', label='타원 궤도')  # 궤도 그리기
ax.plot([0], [0], 'yo', markersize=15, label='항성')  # 항성 (초점에 위치)
planet, = ax.plot([], [], 'ro', markersize=10, label='행성')  # 행성
ax.legend()
ax.set_xlabel('X (AU)')
ax.set_ylabel('Y (AU)')
ax.set_title('케플러 법칙에 따른 행성 운동')
ax.grid(True)

# 애니메이션 업데이트 함수
def update(frame):
    planet.set_data([x_planet[frame]], [y_planet[frame]])
    return planet,

# 애니메이션 객체 생성
ani = FuncAnimation(fig, update, frames=len(t), interval=50, blit=True)

# 애니메이션을 HTML로 변환하여 Streamlit에 표시
def get_animation_html(ani):
    buf = io.BytesIO()
    ani.save(buf, format='gif')
    buf.seek(0)
    return f'<img src="data:image/gif;base64,{base64.b64encode(buf.read()).decode()}"/>'

st.markdown(get_animation_html(ani), unsafe_allow_html=True)

plt.close(fig)
