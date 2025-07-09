import stream

lit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import io
import base64

# Streamlit 앱 제목
st.title("케플러 법칙에 따른 행성 운동 시뮬레이션")

# 사용자 입력: 긴반지름(a)과 짧은반지름(b)
st.write("타원 궤도의 긴반지름(a)과 짧은반지름(b)을 입력하세요 (단위: 천문단위, AU):")
a = st.number_input("긴반지름 (a)", min_value=0.1, max_value=10.0, value=1.0, step=0.1)
b = st.number_input("짧은반지름 (b)", min_value=0.1, max_value=a, value=0.5, step=0.1)

# 케플러 제2법칙을 위한 설정
e = np.sqrt(1 - (b**2 / a**2))  # 이심률
c = a * e  # 초점 거리

# 타원 궤도 계산
theta = np.linspace(0, 2 * np.pi, 100)
x_orbit = a * np.cos(theta)
y_orbit = b * np.sin(theta)

# 행성 운동 계산 (케플러 제2법칙)
def get_r(theta, a, e):
    return a * (1 - e**2) / (1 + e * np.cos(theta))

t = np.linspace(0, 2 * np.pi, 100)
r = get_r(t, a, e)
x_planet = r * np.cos(t)
y_planet = r * np.sin(t)

# 애니메이션 생성
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_aspect('equal')
ax.plot(x_orbit, y_orbit, 'b-', label='타원 궤도')
ax.plot([0], [0], 'yo', markersize=15, label='항성')
planet, = ax.plot([], [], 'ro', markersize=10, label='행성')
ax.legend()
ax.set_xlabel('X (AU)')
ax.set_ylabel('Y (AU)')
ax.set_title('케플러 법칙에 따른 행성 운동')
ax.grid(True)

# 애니메이션 업데이트 함수
def update(frame):
    planet.set_data([x_planet[frame]], [y_planet[frame]])
    return planet,

# 애니메이션 생성
ani = FuncAnimation(fig, update, frames=len(t), interval=50, blit=True)

# 애니메이션을 GIF로 변환하여 Streamlit에 표시
def get_animation_html(ani):
    buf = io.BytesIO()
    try:
        writer = PillowWriter(fps=20)
        ani.save(buf, writer=writer)
        buf.seek(0)
        video = buf.getvalue()
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
    st.write("애니메이션을 생성할 수 없습니다. pillow>=9.0.0과 matplotlib>=3.5.0이 설치되어 있는지 확인하세요.")

plt.close(fig)
