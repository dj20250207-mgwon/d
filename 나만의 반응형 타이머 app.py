import streamlit as st
import time

# 웹 페이지 기본 설정
st.set_page_config(page_title="반응형 타이머", page_icon="⏱️", layout="centered")

# CSS 스타일링 (`clamp()` 활용 반응형 디자인 & 스파이더맨 테마)
st.markdown("""
    <style>
    .timer-card {
        background-color: #f8f9fa;
        border: 2px solid #e9ecef;
        border-radius: 20px;
        width: clamp(280px, 80vw, 450px);
        padding: clamp(15px, 4vw, 35px);
        margin: 0 auto 20px auto;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
    }
    .timer-label {
        color: #6b7280;
        font-size: clamp(0.875rem, 2.5vw, 1.125rem);
        margin: 0;
    }
    .timer-display {
        font-size: clamp(2.5rem, 10vw, 5rem);
        font-weight: 800;
        color: #1f2937;
        font-family: 'Courier New', Courier, monospace;
        letter-spacing: 2px;
        margin: clamp(5px, 2vw, 15px) 0;
    }
    .spiderman-title {
        color: #e11d48;
        font-weight: 900;
        text-shadow: 2px 2px #1e3a8a;
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
if "remaining_seconds" not in st.session_state:
    st.session_state.remaining_seconds = 0
if "is_running" not in st.session_state:
    st.session_state.is_running = False
if "is_paused" not in st.session_state:
    st.session_state.is_paused = False
if "is_completed" not in st.session_state:
    st.session_state.is_completed = False
if "is_spiderman" not in st.session_state:
    st.session_state.is_spiderman = False

# 타이머 시작 / 시간 세팅 함수
def set_timer(seconds, spiderman_mode=False):
    st.session_state.total_duration = seconds
    st.session_state.remaining_seconds = seconds
    st.session_state.end_time = time.monotonic() + seconds
    st.session_state.is_running = True
    st.session_state.is_paused = False
    st.session_state.is_completed = False
    st.session_state.is_spiderman = spiderman_mode

# 일반 분 단위 세팅
def set_timer_minutes(minutes):
    set_timer(minutes * 60, spiderman_mode=False)

# 시작 / 재개 함수
def start_or_resume_timer():
    if st.session_state.is_paused:
        st.session_state.end_time = time.monotonic() + st.session_state.remaining_seconds
        st.session_state.is_paused = False
        st.session_state.is_running = True
    elif not st.session_state.is_running and st.session_state.remaining_seconds > 0:
        st.session_state.end_time = time.monotonic() + st.session_state.remaining_seconds
        st.session_state.is_running = True

# 일시정지 함수
def pause_timer():
    if st.session_state.is_running:
        st.session_state.remaining_seconds = max(0, st.session_state.end_time - time.monotonic())
        st.session_state.is_running = False
        st.session_state.is_paused = True

# 리셋 함수
def reset_timer():
    st.session_state.end_time = None
    st.session_state.total_duration = 0
    st.session_state.remaining_seconds = 0
    st.session_state.is_running = False
    st.session_state.is_paused = False
    st.session_state.is_completed = False
    st.session_state.is_spiderman = False

# 헤더
if st.session_state.is_spiderman:
    st.markdown("<h1 class='spiderman-title'>🕷️ 스파이더맨 이스터에그 타이머 🕸️</h1>", unsafe_allow_html=True)
else:
    st.title("⏱️ 스마트 타이머")

# 1. 빠른 설정 버튼 (1, 2, 3, 4, 5, 10분)
st.subheader("빠른 시간 설정")
cols = st.columns(6)
quick_times = [1, 2, 3, 4, 5, 10]

for idx, mins in enumerate(quick_times):
    if cols[idx].button(f"{mins}분", use_container_width=True):
        set_timer_minutes(mins)

st.markdown("---")

# 2. st.fragment 기반 타이머 카드 및 제어 버튼
@st.fragment(run_every=1.0 if st.session_state.is_running else None)
def render_timer_card():
    # 진행 중일 때 남은 시간 계산
    if st.session_state.is_running and st.session_state.end_time:
        remaining = st.session_state.end_time - time.monotonic()
        if remaining <= 0:
            remaining = 0
            st.session_state.remaining_seconds = 0
            st.session_state.is_running = False
            st.session_state.is_completed = True
        else:
            st.session_state.remaining_seconds = remaining
    else:
        remaining = st.session_state.remaining_seconds

    # 분/초 계산
    mins, secs = divmod(max(0, int(remaining)), 60)
    time_str = f"{mins:02d}:{secs:02d}"

    # 카드 UI & 스파이더맨 이스터에그 연출
    status_label = "🕷️ 친절한 이웃 스파이더맨과 함께하는 시간" if st.session_state.is_spiderman else ("일시정지됨" if st.session_state.is_paused else ("진행 중" if st.session_state.is_running else "남은 시간"))
    
    st.markdown(
        f"""
        <div class="timer-card" style="{'border-color: #e11d48; background-color: #fff1f2;' if st.session_state.is_spiderman else ''}">
            <p class="timer-label">{status_label}</p>
            <div class="timer-display" style="{'color: #e11d48;' if st.session_state.is_spiderman else ''}">{time_str}</div>
        </div>
        """, 
        unsafe_allow_html=True
    )

    # 스파이더맨 모드일 때 스파이더맨 이미지/GIF 등장!
    if st.session_state.is_spiderman:
        st.image(
            "https://media.giphy.com/media/SF9Z0sh9uL0lh69L0f/giphy.gif", 
            caption="With Great Power Comes Great Responsibility! 🕸️",
            use_container_width=True
        )

    # 제어 버튼 및 상태 영역
    _, center_col, _ = st.columns([1, 6, 1])
    with center_col:
        # 게이지 바 (Progress Bar)
        if st.session_state.total_duration > 0:
            progress = max(0.0, min(1.0, remaining / st.session_state.total_duration))
            st.progress(progress)

        # 버튼 그룹
        btn_col1, btn_col2 = st.columns(2)

        with btn_col1:
            if st.session_state.is_running:
                if st.button("⏸️ 일시정지", use_container_width=True):
                    pause_timer()
                    st.rerun()
            else:
                is_disabled = (st.session_state.remaining_seconds <= 0) and not st.session_state.is_paused
                btn_label = "▶️ 재개" if st.session_state.is_paused else "▶️ 시작"
                if st.button(btn_label, type="primary", disabled=is_disabled, use_container_width=True):
                    start_or_resume_timer()
                    st.rerun()

        with btn_col2:
            if st.button("🔄 리셋", use_container_width=True):
                reset_timer()
                st.rerun()

        # 완료 처리 (성공 메시지 및 풍선 애니메이션)
        if st.session_state.is_completed:
            if st.session_state.is_spiderman:
                st.error("🕸️ 🕷️ 스파이더맨 미션 완료! 세상을 구했습니다! 🕷️ 🕸️")
            else:
                st.success("🎉 설정한 시간이 완료되었습니다!")
            st.balloons()
            if st.button("확인", use_container_width=True):
                reset_timer()
                st.rerun()

# 타이머 프래그먼트 호출
render_timer_card()
