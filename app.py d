import time
import streamlit as st

# 페이지 기본 설정 (반응형 레이아웃)
st.set_page_config(
    page_title="반응형 타이머",
    page_icon="⏱️",
    layout="centered"
)

# 커스텀 CSS 적용 (반응형 글자 크기 및 카드 디자인)
st.markdown("""
    <style>
    .timer-card {
        background-color: #f0f2f6;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
    }
    .timer-display {
        font-size: clamp(3rem, 10vw, 6rem);
        font-weight: 700;
        color: #ff4b4b;
        font-family: 'Courier New', Courier, monospace;
    }
    div[data-testid="stHorizontalBlock"] > div {
        flex: 1;
    }
    </style>
""", unsafe_allow_html=True)

# Session State 초기화
if "time_left" not in st.session_state:
    st.session_state.time_left = 60  # 기본값 1분
if "total_time" not in st.session_state:
    st.session_state.total_time = 60
if "is_running" not in st.session_state:
    st.session_state.is_running = False

# 앱 타이틀
st.title("⏱️ 반응형 타이머")
st.caption("모바일과 PC 모두에 최적화된 스트림릿 타이머입니다.")

st.divider()

# 1. 시간 설정 섹션 (반응형 컬럼 적용)
col_m, col_s = st.columns(2)
with col_m:
    minutes = st.number_input("분 (Minutes)", min_value=0, max_value=180, value=1, step=1, disabled=st.session_state.is_running)
with col_s:
    seconds = st.number_input("초 (Seconds)", min_value=0, max_value=59, value=0, step=1, disabled=st.session_state.is_running)

# 설정 시간 업데이트 (타이머가 정지 상태일 때만)
if not st.session_state.is_running and (st.session_state.time_left == st.session_state.total_time):
    st.session_state.time_left = minutes * 60 + seconds
    st.session_state.total_time = minutes * 60 + seconds

# 2. 타이머 디스플레이 UI
timer_container = st.empty()

def render_timer():
    mins, secs = divmod(st.session_state.time_left, 60)
    time_format = f"{mins:02d}:{secs:02d}"
    
    # 진행률 계산
    progress = 0.0
    if st.session_state.total_time > 0:
        progress = st.session_state.time_left / st.session_state.total_time

    with timer_container.container():
        st.markdown(f"""
            <div class="timer-card">
                <div class="timer-display">{time_format}</div>
            </div>
        """, unsafe_allow_html=True)
        st.progress(progress)

# 초기 UI 렌더링
render_timer()

# 3. 제어 버튼 섹션
btn_col1, btn_col2, btn_col3 = st.columns(3)

with btn_col1:
    if st.button("▶️ 시작", use_container_width=True, disabled=st.session_state.is_running or st.session_state.time_left <= 0):
        st.session_state.is_running = True
        st.rerun()

with btn_col2:
    if st.button("⏸️ 일시정지", use_container_width=True, disabled=not st.session_state.is_running):
        st.session_state.is_running = False
        st.rerun()

with btn_col3:
    if st.button("🔄 리셋", use_container_width=True):
        st.session_state.is_running = False
        st.session_state.time_left = minutes * 60 + seconds
        st.session_state.total_time = minutes * 60 + seconds
        st.rerun()

# 4. 타이머 카운트다운 로직 Loop
if st.session_state.is_running and st.session_state.time_left > 0:
    time.sleep(1)
    st.session_state.time_left -= 1
    
    if st.session_state.time_left == 0:
        st.session_state.is_running = False
        render_timer()
        st.balloons()
        st.success("🎉 시간이 다 되었습니다!")
    else:
        st.rerun()
