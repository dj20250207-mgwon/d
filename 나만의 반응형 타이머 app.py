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

# 타이머 시작 / 시간 세팅 함수
def set_timer(seconds):
    st.session_state.total_duration = seconds
    st.session_state.remaining_seconds = seconds
    st.session_state.end_time = time.monotonic() + seconds
    st.session_state.is_running = True
    st.session_state.is_paused = False
    st.session_state.is_completed = False

# 분 단위 세팅
def set_timer_minutes(minutes):
    set_timer(minutes * 60)

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

# 타이머 카드 렌더링 프래그먼트
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

    # 정확히 남은 시간이 420초(7분) 이하이고 타이머에 남은 시간이 있을 때 스파이더맨 발동
    is_spiderman = (0 < remaining <= 420)

    # 헤더
    if is_spiderman:
        st.markdown("<h1 class='spiderman-title'>🕷️ 스파이더맨 이스터에그 타이머 🕸️</h1>", unsafe_allow_html=True)
    else:
        st.title("⏱️ 스마트 타이머")

    # 분/초 계산
    mins, secs = divmod(max(0, int(remaining)), 60)
    time_str = f"{mins:02d}:{secs:02d}"

    status_label = "🕷️ 친절한 이웃 스파이더맨이 지켜보고 있습니다!" if is_spiderman else (
        "일시정지됨" if st.session_state.is_paused else ("진행 중" if st.session_state.is_running else "남은 시간")
    )

    # 카드 UI
    st.markdown(
        f"""
        <div class="timer-card" style="{'border-color: #e11d48; background-color: #fff1f2;' if is_spiderman else ''}">
            <p class="timer-label">{status_label}</p>
            <div class="timer-display" style="{'color: #e11d48;' if is_spiderman else ''}">{time_str}</div>
        </div>
        """, 
        unsafe_allow_html=True
    )

    # 스파이더맨 이스터에그 GIF (420초 이하일 때만 표시)
    if is_spiderman:
        st.image(
            "https://media.giphy.com/media/SF9Z0sh9uL0lh69L0f/giphy.gif", 
            caption="With Great Power Comes Great Responsibility! 🕸️",
            use_container_width=True
        )

    # 제어 버튼 영역
    _, center_col, _ = st.columns([1, 6, 1])
    with center_col:
        # 게이지 바
        if st.session_state.total_duration > 0:
            progress = max(0.0, min(1.0, remaining / st.session_state.total_duration))
            st.progress(progress)

        # 컨트롤 버튼
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

        # 완료 화면
        if st.session_state.is_completed:
            st.success("🎉 설정한 시간이 완료되었습니다!")
            st.balloons()
            if st.button("확인", use_container_width=True):
                reset_timer()
                st.rerun()

# 1. 사용자 직접 시간 입력 UI
st.subheader("⏱️ 사용자 직접 시간 입력")
input_col1, input_col2, input_col3 = st.columns([2, 2, 1.5])

with input_col1:
    custom_mins = st.number_input("분 (Min)", min_value=0, max_value=300, value=10, step=1)
with input_col2:
    custom_secs = st.number_input("초 (Sec)", min_value=0, max_value=59, value=0, step=1)
with input_col3:
    st.write("") # 마진 정렬용
    st.write("")
    if st.button("시간 설정", use_container_width=True, type="primary"):
        total_custom_seconds = custom_mins * 60 + custom_secs
        if total_custom_seconds > 0:
            set_timer(total_custom_seconds)
            st.rerun()

# 2. 빠른 설정 버튼
st.subheader("빠른 시간 설정")
quick_times = [1, 3, 5, 10, 15, 20]
cols = st.columns(len(quick_times))

for idx, mins in enumerate(quick_times):
    if cols[idx].button(f"{mins}분", use_container_width=True):
        set_timer_minutes(mins)

st.markdown("---")

# 3. 타이머 프래그먼트 호출
render_timer_card()
