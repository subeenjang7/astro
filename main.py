import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import tempfile
import base64
import os
import matplotlib as mpl

# 🔤 한글 폰트 설정 (없으면 Arial로 대체)
mpl.rcParams['font.family'] = 'NanumGothic' if 'NanumGothic' in mpl.font_manager.get_font_names() else 'Arial'
mpl.rcParams['axes.unicode_minus'] = False

# 🛰️ 제목
st.title("🌍 케플러 법칙 기반 행성의 타원 궤도 시뮬레이션")

# 📌 사용자 입력
a = st.number_input("긴반지름 a (AU)", min_value=0.1, max_value=10.0, value=1.0, step=0.1)
b = st.number_input("짧은반지름 b (AU)", min_value=0.1, max_value=a, value=0.8, step=0.1)

# ⚙️ 이심률 및 초점 거리
e = np.sqrt(1 - (b**2 / a**2))
c = a * e  # 항성이 위치한 초점 거리

# 🔷 타원 궤도 (항성이 초점 = 원점 기준)
theta = np.linspace(0, 2 * np.pi, 1000)
x_orbit = a * np.cos(theta) - c
y_orbit = b * np.sin(theta)

# 🔴 행성 운동 계산
def solve_kepler(M, e):
    E = M
    for _ in range(10):
        E -= (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
    return E

t = np.linspace(0, 2 * np.pi, 300)
M = t  # 평균이각
E = np.array([solve_kepler(Mi, e) for Mi in M])
theta_planet = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2),
                              np.sqrt(1 - e) * np.cos(E / 2))
r = a * (1 - e**2) / (1 + e * np.cos(theta_planet))
x_planet = r * np.cos(theta_planet)
y_planet = r * np.sin(theta_planet)

# 📊 그래프 그리기
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_aspect('equal')
ax.plot(x_orbit, y_orbit, 'b-', label='타원 궤도')
ax.plot([0], [0], 'yo', markersize=15, label='항성 (초점)')
planet, = ax.plot([], [], 'ro', markersize=10, label='행성')
ax.legend()
ax.set_xlabel('X (AU)')
ax.set_ylabel('Y (AU)')
ax.set_title('케플러 궤도에서의 행성 운동 (초점 기준)')
ax.grid(True)

# 🔍 전체 궤도 보이도록 축 자동 설정
x_min = np.min(x_orbit) - 0.1 * a
x_max = np.max(x_orbit) + 0.1 * a
y_min = np.min(y_orbit) - 0.1 * b
y_max = np.max(y_orbit) + 0.1 * b
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)

# 🔄 애니메이션 업데이트 함수
def update(frame):
    planet.set_data([x_planet[frame]], [y_planet[frame]])
    return planet,

ani = FuncAnimation(fig, update, frames=len(t), interval=40, blit=True)

# 📤 애니메이션을 GIF로 저장 및 표시
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
        st.error(f"애니메이션 저장 중 오류 발생: {str(e)}")
        return None

# 🖼️ 애니메이션 출력
html = get_animation_html(ani)
if html:
    st.markdown(html, unsafe_allow_html=True)
else:
    st.warning("애니메이션 생성에 실패했습니다.")

# 리소스 해제
plt.close(fig)
