import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import tempfile
import base64
import os
import matplotlib as mpl

# ------------------------
# 글꼴 설정: NanumGothic 설치되어 있지 않으면 Arial 사용
mpl.rcParams['font.family'] = 'NanumGothic' if 'NanumGothic' in mpl.font_manager.findSystemFonts(fontpaths=None, fontext='ttf') else 'Arial'
mpl.rcParams['axes.unicode_minus'] = False  # 음수 깨짐 방지
# ------------------------

st.title("🌍 케플러 법칙에 따른 행성의 타원 궤도")

# 사용자 입력: 긴반지름 a, 짧은반지름 b
st.write("🔧 타원 궤도의 긴반지름(a)과 짧은반지름(b)을 입력하세요:")
a = st.number_input("긴반지름 a (AU)", min_value=0.1, max_value=10.0, value=1.0, step=0.1)
b = st.number_input("짧은반지름 b (AU)", min_value=0.1, max_value=a, value=0.8, step=0.1)

# 이심률과 초점 거리
e = np.sqrt(1 - (b**2 / a**2))  # 이심률
c = a * e  # 항성이 위치한 초점 거리

# ------------------------
# 타원 궤도 생성 (중심 기준), 이후 평행이동으로 초점(항성)이 원점에 위치
theta = np.linspace(0, 2 * np.pi, 1000)
x_orbit = a * np.cos(theta)
y_orbit = b * np.sin(theta)
x_orbit -= c  # 평행이동: 항성이 원점에 오도록
# ------------------------

# 평균 근점 이각 -> 편심이각 E 구하고 -> 극좌표 θ 구하기
def solve_kepler(M, e):
    E = M
    for _ in range(10):
        E -= (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
    return E

t = np.linspace(0, 2 * np.pi, 200)
M = t  # 평균 이각
E = np.array([solve_kepler(Mi, e) for Mi in M])
theta_planet = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2),
                              np.sqrt(1 - e) * np.cos(E / 2))
r = a * (1 - e**2) / (1 + e * np.cos(theta_planet))
x_planet = r * np.cos(theta_planet) - c
y_planet = r * np.sin(theta_planet)

# ------------------------
# 시각화
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_aspect('equal')
ax.plot(x_orbit, y_orbit, 'b-', label='타원 궤도')
ax.plot([0], [0], 'yo', markersize=15, label='항성')  # 항성은 원점
planet, = ax.plot([], [], 'ro', markersize=10, label='행성')
ax.legend()
ax.set_xlabel('X (AU)')
ax.set_ylabel('Y (AU)')
ax.set_title('케플러 궤도 시뮬레이션 (항성은 타원의 초점에 위치)')
ax.grid(True)
ax.set_xlim(-1.5 * a, 1.5 * a)
ax.set_ylim(-1.5 * b, 1.5 * b)
# ------------------------

# 애니메이션 업데이트
def update(frame):
    planet.set_data([x_planet[frame]], [y_planet[frame]])
    return planet,

ani = FuncAnimation(fig, update, frames=len(t), interval=50, blit=True)

# GIF로 변환 및 출력
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
        st.error(f"애니메이션 저장 중 오류: {str(e)}")
        return None

# 표시
html = get_animation_html(ani)
if html:
    st.markdown(html, unsafe_allow_html=True)
else:
    st.warning("애니메이션 생성 실패. Pillow와 Matplotlib 버전 확인 필요.")

plt.close(fig)
