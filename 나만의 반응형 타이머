import streamlit as st
import time

# 웹 페이지 기본 설정
st.set_page_config(page_title="반응형 타이머", page_icon="⏱️", layout="centered")

# CSS 스타일링 (중앙 카드가 반응형으로 동작하도록 설정)
st.markdown("""
    <style>
    .timer-card {
        background-color: #f8f9fa;
        border: 2px solid #e9ecef;
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        margin-bottom: 25px;
    }
    .timer-display {
        font-size: clamp(2.5rem, 8vw, 4.5rem);
        font-weight: 800;
        color: #1f2937;
        font-family: 'Courier New', Courier, monospace;
        letter-spacing: 2px;
        margin: 10px 0;
    }
    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# 세션 상태(st.session_state) 초기화
if "end_time" not in st.session_state:
    st.session_state.end_time = None
if "total_duration" not in st.session_state:
    st.session_state.total_duration = 0
if "is_running" not in st.session_state:
    st.session_state.is_running = False
if "is_completed" not in st.session_state:
    st.session_state.is_completed = False

# 타이머 시작 함수
def start_timer(minutes):
    duration_seconds = minutes * 60
    st.session_state.total_duration = duration_seconds
    st.session_state.end_time = time.monotonic() + duration_seconds
    st.session_state.is_running = True
    st.session_state.is_completed = False

# 타이머 리셋 함수
def reset_timer():
    st.session_state.end_time = None
    st.session_state.total_duration = 0
    st.session_state.is_running = False
    st.session_state.is_completed = False

st.title("⏱️ 스마트 타이머")

# 1. 빠른 설정 버튼 (1, 2, 3, 4, 5, 10분)
st.subheader("빠른 시간 설정")
cols = st.columns(6)
quick_times = [1, 2, 3, 4, 5, 10]

for idx, mins in enumerate(quick_times):
    if cols[idx].button(f"{mins}분", use_container_width=True):
        start_timer(mins)

st.markdown("---")

# 2. st.fragment 및 run_every를 활용한 부분 새로고침 타이머 영역
@st.fragment(run_every=1.0 if st.session_state.is_running else None)
def render_timer_card():
    # 카드가 화면 중앙에 배치되도록 컬럼 사용
    left_pad, center_card, right_pad = st.columns([1, 4, 1])
    
    with center_card:
        remaining = 0
        if st.session_state.is_running and st.session_state.end_time:
            # time.monotonic()을 이용한 정확한 남은 시간 계산
            remaining = st.session_state.end_time - time.monotonic()
            
            # 시간이 종료되었을 때 처리
            if remaining <= 0:
                remaining = 0
                st.session_state.is_running = False
                st.session_state.is_completed = True
        
        # 분/초 계산
        mins, secs = divmod(max(0, int(remaining)), 60)
        time_str = f"{mins:02d}:{secs:02d}"
        
        # 카드 형태로 UI 렌더링
        st.markdown(
            f"""
            <div class="timer-card">
                <p style="color: #6b7280; font-size: 1rem; margin: 0;">남은 시간</p>
                <div class="timer-display">{time_str}</div>
            </div>
            """, 
            unsafe_allow_html=True
        )

        # 게이지 바 (Progress Bar)
        if st.session_state.total_duration > 0 and st.session_state.is_running:
            progress = max(0.0, min(1.0, remaining / st.session_state.total_duration))
            st.progress(progress)
            
        # 정지 / 초기화 버튼
        if st.session_state.is_running:
            if st.button("⏹️ 타이머 중지", type="primary", use_container_width=True):
                reset_timer()
                st.rerun()

        # 완료 이벤트 (성공 메시지 및 풍선 효과)
        if st.session_state.is_completed:
            st.success("🎉 설정한 시간이 완료되었습니다!")
            st.balloons()
            if st.button("확인", use_container_width=True):
                reset_timer()
                st.rerun()

# 타이머 카트 프래그먼트 호출
render_timer_card()
