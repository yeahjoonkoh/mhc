import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ----- 기본 설정 -----
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"]
BLOCKS = ["(09:00~10:15)", "(10:30~11:45)", "(12:00~13:15)",
          "(13:30~14:45)", "(15:00~16:15)", "(16:30~17:45)"]
NUM_DAYS = len(DAYS)
NUM_BLOCKS = len(BLOCKS)

# ----- 세션 상태 초기화 -----
if "timetables" not in st.session_state:
    st.session_state.timetables = {}

# ----- 사이드바: 페이지 선택 -----
page = st.sidebar.radio("메뉴", ["시간표 입력", "겹공강 찾기"])

# ----- 시간표 입력 페이지 -----
if page == "시간표 입력":
    st.title("시간표 입력")
    name = st.text_input("사용자 이름을 입력하세요")

    if name:
        st.write(f"{name}님의 시간표")
        timetable = np.zeros((NUM_DAYS, NUM_BLOCKS), dtype=int)

        for i, day in enumerate(DAYS):
            st.markdown(f"**{day}**")
            cols = st.columns(NUM_BLOCKS)
            for j, col in enumerate(cols):
                checked = col.checkbox(BLOCKS[j], key=f"{name}_{day}_{j}")
                if checked:
                    timetable[i, j] = 1

        if st.button("시간표 저장"):
            st.session_state.timetables[name] = timetable
            st.success(f"{name}님의 시간표가 저장되었습니다.")

# ----- 공강 시간 확인 페이지 -----
elif page == "겹공강 찾기":
    st.title("겹공강 찾기")

    if not st.session_state.timetables:
        st.warning("저장된 시간표가 없습니다. 먼저 시간표를 입력하세요.")
    else:
        st.write("저장된 시간표:", list(st.session_state.timetables.keys()))

        all_timetables = list(st.session_state.timetables.values())
        combined = np.array(all_timetables).sum(axis=0)
        free_slots = (combined == 0)

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.imshow(free_slots.T, cmap="Greens", aspect="auto")

        ax.set_xticks(np.arange(NUM_DAYS))
        ax.set_xticklabels(DAYS)
        ax.set_yticks(np.arange(NUM_BLOCKS))
        ax.set_yticklabels(BLOCKS)
        ax.set_title("")

        for i in range(NUM_DAYS):
            for j in range(NUM_BLOCKS):
                text = "-" if free_slots[i, j] else "-"
                ax.text(i, j, text, ha="center", va="center", color="black")

        st.pyplot(fig)
        st.info("녹색 칸이 모든 사용자가 공강인 시간입니다.")
