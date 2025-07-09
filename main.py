```python
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

# 애니메이션을 MP4로 변환하여 Streamlit에 표시
def get_animation_html(ani):
    buf = io.BytesIO()
    try:
        ani.save(buf, format='mp4', writer='ffmpeg', fps=20)
        buf.seek(0)
        video = buf.getvalue()
        video_base64 = base64.b64encode(video).decode()
        return f'<video width="600" controls><source src="data:video/mp4;base64,{video_base64}" type="video/mp4"></video>'
    except Exception as e:
        st.error(f"애니메이션 저장 중 오류 발생: {str(e)}")
        return None

# 애니메이션 표시
html = get_animation_html(ani)
if html:
    st.markdown(html, unsafe_allow_html=True)
else:
    st.write("애니메이션을 생성할 수 없습니다. ffmpeg 또는 pillow가 설치되어 있는지 확인하세요.")

plt.close(fig)
```

#### `requirements.txt`
```
streamlit>=1.24.0
numpy>=1.21.0
matplotlib>=3.5.0
pillow>=9.0.0
ffmpeg-python>=0.2.0
```

### 변경사항
1. **GIF → MP4로 전환**:
   - `ani.save`를 MP4 형식으로 변경하고, `writer='ffmpeg'`를 사용하여 HTML5 비디오로 렌더링.
   - MP4는 Streamlit에서 `<video>` 태그로 표시되며, GIF보다 호환성이 좋고 파일 크기가 작음.
2. **오류 처리 추가**:
   - `try-except` 블록을 추가하여 애니메이션 저장 중 발생하는 오류를 캐치하고, 사용자에게 친화적인 메시지를 표시.
3. **종속성 업데이트**:
   - `requirements.txt`에 `ffmpeg-python`을 추가하여 MP4 저장을 지원.
   - Streamlit Cloud에서는 `ffmpeg` 바이너리가 시스템에 설치되어 있어야 하므로, Streamlit Cloud의 패키지 관리 설정을 확인.
4. **Pyodide 고려**:
   - Pyodide에서는 `ffmpeg`이 지원되지 않을 가능성이 높으므로, 이 코드는 Streamlit Cloud 또는 로컬 Python 환경에 최적화됨.
   - Pyodide에서 실행하려면 정적 프레임 렌더링(예: 여러 정적 플롯)을 대안으로 고려해야 함.

### 실행 방법
1. **Streamlit Cloud**:
   - `kepler_orbit_app.py`와 `requirements.txt`를 프로젝트 디렉토리에 업로드.
   - Streamlit Cloud에서 앱을 재배포.
   - `Manage app`에서 로그를 확인하여 `ffmpeg` 설치 여부를 점검. Streamlit Cloud에서 `ffmpeg`이 기본적으로 설치되지 않을 수 있으므로, 커뮤니티 포럼 또는 Streamlit 지원팀에 문의.
2. **로컬 환경**:
   - 종속성 설치:
     ```bash
     pip install -r requirements.txt
     ```
   - `ffmpeg` 설치 (시스템별):
     - **Ubuntu/Debian**:
       ```bash
       sudo apt-get install ffmpeg
       ```
     - **macOS**:
       ```bash
       brew install ffmpeg
       ```
     - **Windows**:
       - `ffmpeg` 바이너리를 다운로드하고, 시스템 PATH에 추가.
   - 앱 실행:
     ```bash
     streamlit run kepler_orbit_app.py
     ```
3. **Pyodide 환경**:
   - Pyodide에서는 MP4 렌더링이 제한적일 수 있으므로, 대안으로 정적 플롯을 여러 프레임으로 나누어 표시하는 코드를 요청하면 제공 가능.

### Pyodide 대안 (정적 플롯)
Pyodide 환경에서 애니메이션이 작동하지 않을 경우, 아래는 정적 플롯을 여러 프레임으로 나누어 표시하는 간단한 대체 코드입니다:

#### `kepler_orbit_static.py`
<xaiArtifact artifact_id="d0d9b7d3-5b37-4392-a17c-7ebc9b864b9d" artifact_version_id="604a62f0-427b-4949-96f2-acb3f8abfbb1" title="kepler_orbit_static.py" contentType="text/python">
```python
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("케플러 법칙에 따른 행성 운동 시뮬레이션 (정적)")

# 사용자 입력
st.write("타원 궤도의 긴반지름(a)과 짧은반지름(b)을 입력하세요 (단위: 천문단위, AU):")
a = st.number_input("긴반지름 (a)", min_value=0.1, max_value=10.0, value=1.0, step=0.1)
b = st.number_input("짧은반지름 (b)", min_value=0.1, max_value=a, value=0.5, step=0.1)
frame = st.slider("프레임 선택", 0, 99, 0)

# 케플러 제2법칙 설정
e = np.sqrt(1 - (b**2 / a**2))
c = a * e

# 타원 궤도
theta = np.linspace(0, 2 * np.pi, 100)
x_orbit = a * np.cos(theta)
y_orbit = b * np.sin(theta)

# 행성 위치
def get_r(theta, a, e):
    return a * (1 - e**2) / (1 + e * np.cos(theta))

t = np.linspace(0, 2 * np.pi, 100)
r = get_r(t, a, e)
x_planet = r * np.cos(t)
y_planet = r * np.sin(t)

# 플롯 생성
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_aspect('equal')
ax.plot(x_orbit, y_orbit, 'b-', label='타원 궤도')
ax.plot([0], [0], 'yo', markersize=15, label='항성')
ax.plot([x_planet[frame]], [y_planet[frame]], 'ro', markersize=10, label='행성')
ax.legend()
ax.set_xlabel('X (AU)')
ax.set_ylabel('Y (AU)')
ax.set_title('케플러 법칙에 따른 행성 운동 (프레임 {})'.format(frame))
ax.grid(True)

# Streamlit에 플롯 표시
st.pyplot(fig)
plt.close(fig)
```

#### `requirements.txt` (정적 버전)
```
streamlit>=1.24.0
numpy>=1.21.0
matplotlib>=3.5.0
