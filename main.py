import streamlit as st
import pandas as pd

# ---------------------------------------
# 기본 설정
# ---------------------------------------
st.set_page_config(
    page_title="대전 연평균 기온 변화",
    page_icon="🌡️",
    layout="wide"
)

# ---------------------------------------
# 제목
# ---------------------------------------
st.title("🌡️ 대전 연평균 기온 변화")
st.subheader("1969년 이후 대전의 연평균 기온은 어떻게 변했을까?")

st.write(
    "대전 기상 관측 자료를 이용하여 1969년부터 최근까지 "
    "연도별 평균기온의 변화를 선그래프로 나타냅니다."
)

# ---------------------------------------
# 데이터 불러오기
# ---------------------------------------
DATA_URL = (
    "https://raw.githubusercontent.com/thinko24/"
    "daejeon_temp/main/data/daejeon.csv"
)


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 날짜를 날짜 형식으로 변환
    df["날짜"] = pd.to_datetime(df["날짜"])

    # 연도 추출
    df["연도"] = df["날짜"].dt.year

    # 평균기온을 숫자로 변환
    df["평균기온"] = pd.to_numeric(
        df["평균기온"],
        errors="coerce"
    )

    return df


try:
    df = load_data()

    # ---------------------------------------
    # 연도별 평균기온 계산
    # ---------------------------------------
    annual_temp = (
        df.groupby("연도")["평균기온"]
        .mean()
        .reset_index()
    )

    annual_temp["평균기온"] = annual_temp["평균기온"].round(2)

    # 1969년 이후 데이터만 사용
    annual_temp = annual_temp[
        annual_temp["연도"] >= 1969
    ]

    # ---------------------------------------
    # 주요 수치
    # ---------------------------------------
    first_year = int(annual_temp.iloc[0]["연도"])
    last_year = int(annual_temp.iloc[-1]["연도"])

    first_temp = annual_temp.iloc[0]["평균기온"]
    last_temp = annual_temp.iloc[-1]["평균기온"]

    change = round(last_temp - first_temp, 2)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "시작 연도",
            f"{first_year}년",
            f"{first_temp:.2f} ℃"
        )

    with col2:
        st.metric(
            "최근 연도",
            f"{last_year}년",
            f"{last_temp:.2f} ℃"
        )

    with col3:
        st.metric(
            "평균기온 변화",
            f"{change:+.2f} ℃",
            "1969년 대비"
        )

    # ---------------------------------------
    # 선그래프
    # ---------------------------------------
    st.markdown("### 📈 연도별 평균기온 변화")

    chart_data = annual_temp.set_index("연도")

    st.line_chart(
        chart_data["평균기온"],
        x_label="연도",
        y_label="평균기온 (℃)",
        height=500
    )

    # ---------------------------------------
    # 데이터 표
    # ---------------------------------------
    with st.expander("📋 연도별 평균기온 데이터 보기"):
        display_data = annual_temp.copy()
        display_data["연도"] = display_data["연도"].astype(str) + "년"
        display_data["평균기온"] = (
            display_data["평균기온"].map(lambda x: f"{x:.2f} ℃")
        )

        display_data.columns = [
            "연도",
            "평균기온"
        ]

        st.dataframe(
            display_data,
            use_container_width=True,
            hide_index=True
        )

    # ---------------------------------------
    # 데이터 설명
    # ---------------------------------------
    st.markdown("### 📌 데이터 분석 방법")

    st.write(
        "하루 단위로 기록된 대전의 평균기온 자료를 연도별로 묶은 뒤, "
        "각 연도의 평균기온을 계산하여 연도에 따른 변화를 나타냈습니다."
    )

    st.caption(
        "자료 출처: 기상 관측 데이터 | "
        "CSV: GitHub daejeon_temp"
    )

except Exception as e:
    st.error("데이터를 불러오는 중 문제가 발생했습니다.")
    st.write("오류 내용:", e)