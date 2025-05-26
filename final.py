import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 시간표기준
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"]
BLOCKS = ["(09:00~10:15)", "(10:30~11:45)", "(12:00~13:15)",
          "(13:30~14:45)", "(15:00~16:15)", "(16:30~17:45)"]
NUM_DAYS = len(DAYS)
NUM_BLOCKS = len(BLOCKS)

# 세션리셋
if "timetables" not in st.session_state:
    st.session_state.timetables = {}

# 메뉴패이지
page = st.sidebar.radio("메뉴", ["시간표 입력", "겹공강 찾기"])

# 시간표입력
if page == "시간표 입력":
    st.title("시간표 입력")
    name = st.text_input("이름을 입력하세요")

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
            st.success(f"{name}의 시간표 저장완료")

# 겹공강
elif page == "겹공강 찾기":
    st.title("겹공강 찾기")

    if not st.session_state.timetables:
        st.warning("저장된 시간표가 없습니다. 시간표를 입력하세요")
    else:
        st.write("저장된 시간표:", list(st.session_state.timetables.keys()))

        all_timetables = list(st.session_state.timetables.values())
        combined = np.array(all_timetables).sum(axis=0)
        free_slots = (combined == 0)

        color_array = np.full(free_slots.shape, '#FFCCCC')  # 연한 빨강 기본
        color_array[free_slots] = '#CCFFCC'  # 연한 초록으로 덮어쓰기
        
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.imshow([[0 for _ in range(NUM_DAYS)] for _ in range(NUM_BLOCKS)], alpha=0)

        for i in range(NUM_DAYS):
            for j in range(NUM_BLOCKS):
                ax.add_patch(plt.Rectangle((i - 0.5, j - 0.5), 1, 1, color=color_array[i, j]))

        for i in range(NUM_DAYS + 1):
            ax.axvline(i - 0.5, color='black', linewidth=0.1)
        for j in range(NUM_BLOCKS + 1):
            ax.axhline(j - 0.5, color='black', linewidth=0.1)

        ax.set_xticks(np.arange(NUM_DAYS))
        ax.set_xticklabels(DAYS)
        ax.set_yticks(np.arange(NUM_BLOCKS))
        ax.set_yticklabels(BLOCKS)
        ax.set_title("")

        for i in range(NUM_DAYS):
            for j in range(NUM_BLOCKS):
                text = "" if free_slots[i, j] else "-"
                ax.text(i, j, text, ha="center", va="center", color="black")

        st.pyplot(fig)
        st.info("겹공강은 초록색으로 표시됩니다.")
