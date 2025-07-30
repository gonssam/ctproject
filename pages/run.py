import streamlit as st
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import platform
import os
import numpy as np
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.preprocessing import LabelEncoder


st.set_page_config(page_title="스마트 라이프 어시스턴트", layout="wide")

# 상태 초기화
if "collected_data" not in st.session_state:
    st.session_state.collected_data = []

if "user_algorithm" not in st.session_state:
    st.session_state.user_algorithm = ""

if "ml_model" not in st.session_state:
    st.session_state.ml_model = None

if "ml_ready" not in st.session_state:
    st.session_state.ml_ready = False

tabs = st.tabs([
    "1. 문제 정의", "2. 데이터 수집", "3. 패턴 찾기", 
    "4. 추상화하기", "5. 알고리즘 표현", "6. 자동화 및 디버깅", "7. 요약", "8. 형성평가"
])

# 1. 문제 정의
with tabs[0]:
    st.header("1. 문제 정의")
    st.markdown(
        '''
        <div style='background-color:#fff7e6; border-left:5px solid #ff9900; color:#333 padding:15px; border-radius:8px'>
        비버는 활발하고 호기심 많은 친구예요. 하고 싶은 게 너무 많아서 계획을 세우지 않고 즉흥적으로 움직이곤 해요.<br><br>
        어느 날은 아침에 일어나자마자 갑자기 춤을 추다가 학교에 지각하고, 또 어떤 날은 해야 할 숙제가 있었는데 무슨 과제였는지 기억도 못한 채 게임을 하다가 밤을 새웠어요.<br><br>
        기분이 좋아서 괜히 밖으로 나갔다가 에너지가 바닥나버리기도 하고, 기분이 나빠서 아무것도 안 하고 하루 종일 빈둥거린 적도 많았어요.<br><br>
        이런 비버의 삶은 어지럽고, 해야 할 일들이 점점 쌓였어요. 무엇을 언제 해야 하는지 모르겠고, 지금 내 기분이나 에너지 상태에 맞는 행동이 뭔지도 잘 모르겠어요.<br><br>
        <strong>AI가 상황에 맞는 행동을 추천해준다면 어떨까요?</strong>
        </div>
        ''', unsafe_allow_html=True)
    st.text_area("현재 상태", key="current")
    st.text_area("목표 상태", key="goal")
    st.button("제출하기", key="submit_1")

# 2. 데이터 수집
with tabs[1]:
    st.header("2. 데이터 수집")
    col1, col2 = st.columns(2)
    with col1:
        time = st.text_input("시간대", key="time")
        mood = st.text_input("기분", key="mood")
    with col2:
        energy = st.text_input("에너지 상태", key="energy")
        action = st.text_input("행동", key="action")
    if st.button("제출하기", key="submit_2"):
        if all([time, mood, energy, action]):
            st.session_state.collected_data.append({
                "시간대": time, "기분": mood, "에너지": energy, "행동": action
            })
            st.success("제출되었습니다!")
        else:
            st.warning("모든 항목을 입력해주세요.")

# 3. 패턴 찾기
with tabs[2]:
    st.header("3. 규칙(반복) 패턴 찾기")
    if st.button("2단계 입력 기반 트리 보기"):
        if not st.session_state.collected_data:
            st.warning("⚠️ 2단계에서 데이터를 먼저 입력해주세요.")
        else:
            tree = {}
            for d in st.session_state.collected_data:
                t, e, m, a = d["시간대"], d["에너지"], d["기분"], d["행동"]
                tree.setdefault(t, {}).setdefault(e, {})[m] = a
            for t_k, t_v in tree.items():
                st.markdown(f"**{t_k}**")
                for e_k, e_v in t_v.items():
                    st.markdown(f"- {e_k}")
                    for m_k, a_v in e_v.items():
                        st.markdown(f"  - {m_k} → **{a_v}**")

# 4. 추상화
with tabs[3]:
    st.header("4. 추상화하기")
    if st.button("입력 데이터 보기"):
        for i, d in enumerate(st.session_state.collected_data, 1):
            st.markdown(f"{i}. 시간대: {d['시간대']}, 기분: {d['기분']}, 에너지: {d['에너지']}, 행동: {d['행동']}")
    st.text_input("시간대 추상화", key="abs_time", placeholder="예: 오전")
    st.text_input("기분 추상화", key="abs_mood", placeholder="예: 긍정")
    st.text_input("에너지 추상화", key="abs_energy", placeholder="예: 높음")
    st.text_input("행동 범주", key="abs_action", placeholder="예: 운동")
    st.button("제출하기", key="submit_4")

# 5. 알고리즘 표현
with tabs[4]:
    st.header("5. 알고리즘 표현")
    st.text_input("조건 1 (예: 기분)", key="cond1_key")
    st.selectbox("조건 1 비교", ["==", "!="], key="cond1_op")
    st.text_input("조건 1 값", key="cond1_val")
    st.text_input("조건 2 (예: 에너지)", key="cond2_key")
    st.selectbox("조건 2 비교", ["==", "!="], key="cond2_op")
    st.text_input("조건 2 값", key="cond2_val")
    st.text_input("추천 행동", key="recommend_action")
    if st.button("if 문 생성하기"):
        if all([st.session_state.cond1_key, st.session_state.cond1_val, st.session_state.cond2_key, st.session_state.cond2_val, st.session_state.recommend_action]):
            code = f"if {st.session_state.cond1_key} {st.session_state.cond1_op} '{st.session_state.cond1_val}' and {st.session_state.cond2_key} {st.session_state.cond2_op} '{st.session_state.cond2_val}':\\n  추천 = '{st.session_state.recommend_action}'"
            st.session_state.user_algorithm = code
            st.code(code, language="python")

# 6. 자동화 및 디버깅 + ML
with tabs[5]:
    st.header("6. 자동화 및 디버깅")
    st.subheader("💡 머신러닝 기반 AI 학습 및 추천")

    if st.button("AI에게 학습시키기"):
        if len(st.session_state.collected_data) >= 3:
            df = pd.DataFrame(st.session_state.collected_data)
            X = df[["시간대", "기분", "에너지"]]
            y = df["행동"]
            encoders = {col: LabelEncoder().fit(X[col]) for col in X.columns}
            for col in X.columns:
                X[col] = encoders[col].transform(X[col])
            action_encoder = LabelEncoder().fit(y)
            y_encoded = action_encoder.transform(y)
            model = DecisionTreeClassifier()
            model.fit(X, y_encoded)
            st.session_state.ml_model = model
            st.session_state.encoders = encoders
            st.session_state.action_encoder = action_encoder
            st.session_state.ml_ready = True
            st.success("AI 학습이 완료되었습니다!")
        else:
            st.warning("최소 3개의 데이터가 필요합니다.")

    if st.session_state.ml_ready:
        with st.form("ml_form"):
            ml_time = st.selectbox("시간대", st.session_state.encoders["시간대"].classes_)
            ml_mood = st.selectbox("기분", st.session_state.encoders["기분"].classes_)
            ml_energy = st.selectbox("에너지", st.session_state.encoders["에너지"].classes_)
            submitted = st.form_submit_button("AI 행동 예측")
            if submitted:
                vec = [
                    st.session_state.encoders["시간대"].transform([ml_time])[0],
                    st.session_state.encoders["기분"].transform([ml_mood])[0],
                    st.session_state.encoders["에너지"].transform([ml_energy])[0]
                ]
                pred = st.session_state.ml_model.predict([vec])
                pred_action = st.session_state.action_encoder.inverse_transform(pred)[0]
                st.success(f"✅ 머신러닝 추천: {pred_action}")

        st.subheader("🧠 AI가 만든 의사결정 규칙 보기")
        rules = export_text(st.session_state.ml_model, feature_names=list(st.session_state.encoders.keys()))
        st.code(rules)

# 7. 요약
with tabs[6]:
    st.header("7. 나의 AI 설계 요약")
    if st.button("요약 보기"):
        summary = f"""🧠 문제 정의:
현재 상태: {st.session_state.get("current")}
목표 상태: {st.session_state.get("goal")}

📊 수집된 데이터 (예시):
{st.session_state.collected_data[0] if st.session_state.collected_data else "없음"}

🧩 추상화:
시간대: {st.session_state.get("abs_time")}
기분: {st.session_state.get("abs_mood")}
에너지: {st.session_state.get("abs_energy")}
행동: {st.session_state.get("abs_action")}

💡 내가 만든 규칙:
{st.session_state.user_algorithm}

🤖 AI가 만든 규칙:
{export_text(st.session_state.ml_model, feature_names=list(st.session_state.encoders.keys())) if st.session_state.ml_ready else "AI가 아직 학습되지 않았습니다."}

🧪 디버깅 소감:
{st.session_state.get("debug_reflection")}
"""
        st.text_area("요약 내용", value=summary, height=400)

# 8. 형성평가
with tabs[7]:
    st.header("8. 형성평가")

    st.markdown("## ✅ 내가 경험한 CT 사고 과정")
    ct_steps = st.multiselect(
        "이번 활동에서 내가 실제로 해본 사고 과정은 무엇인가요?",
        [
            "문제를 요소로 나누어 보기 (문제 분해)",
            "데이터를 수집하여 특징 보기 (패턴 찾기)",
            "비슷한 것을 묶어 일반화 (추상화)",
            "조건에 따라 동작 표현 (알고리즘)",
            "AI에게 학습시키기 (모델 학습)",
            "AI의 추천을 분석하고 수정 (디버깅)"
        ]
    )

    st.markdown("## 🤖 AI는 데이터를 어떻게 학습할까요?")
   
    # ✅ 한글 폰트 자동 설정 (Windows / macOS / Linux 포함)
    def set_korean_font():
        system = platform.system()
        try:
            if system == 'Windows':
                matplotlib.rcParams['font.family'] = 'Malgun Gothic'
            elif system == 'Darwin':  # macOS
                matplotlib.rcParams['font.family'] = 'AppleGothic'
            else:  # Linux or Streamlit Cloud
                nanum_path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
                if os.path.exists(nanum_path):
                    font_name = fm.FontProperties(fname=nanum_path).get_name()
                    matplotlib.rcParams['font.family'] = font_name
                else:
                    matplotlib.rcParams['font.family'] = 'DejaVu Sans'  # fallback
            matplotlib.rcParams['axes.unicode_minus'] = False
        except Exception as e:
            st.warning(f"폰트 설정 실패: {e}")

    set_korean_font()

    # ✅ 데이터 생성
    data_size = np.linspace(10, 1000, 100)
    accuracy = 1 - np.exp(-data_size / 200)

    # ✅ 그래프 생성
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(data_size, accuracy, color='blue', linewidth=2)
    ax.set_title("AI 학습 곡선 예시")
    ax.set_xlabel("데이터 개수")
    ax.set_ylabel("예측 정확도")
    ax.grid(True)

    # ✅ Streamlit 출력
    st.pyplot(fig)

    ai_q = st.radio("데이터가 많아지면 AI는 어떻게 달라질까요?", [
        "데이터가 많을수록 항상 정확해진다",
        "처음엔 좋아지다가 어느 순간부터는 변화가 적다",
        "너무 많아지면 오히려 정확도가 떨어질 수 있다"
    ])

    if st.button("AI 학습 곡선 정답 확인"):
        if ai_q == "처음엔 좋아지다가 어느 순간부터는 변화가 적다":
            st.success("✅ 정답입니다! 일반적으로 AI 모델은 일정 수준 이상의 데이터 이후엔 성능이 수렴합니다.")
        else:
            st.error("❌ 완전히 정확하지 않아요.")
        with st.expander("💬 해설 보기"):
            st.markdown("""
            - **항상 좋아진다** ❌: 과적합, 품질 불균형 등의 이유로 성능이 떨어질 수도 있어요.
            - **처음엔 좋아지다가 변화가 적다** ✅: 가장 일반적인 AI 학습 곡선 형태입니다.
            - **오히려 나빠진다** 🔁: 특수한 경우(노이즈, 중복, 편향된 데이터)엔 가능하지만 일반적이지 않아요.
            """)

    st.divider()

    st.markdown("## 🔍 AI가 틀린 이유는 무엇일까요?")
    st.markdown(
        "> AI는 기분='무기력', 에너지='보통'일 때 '게임하기'를 추천했지만, 나는 '산책하기'가 더 적절하다고 생각했어요."
    )
    ai_reason_free = st.text_area("❓ 왜 AI가 다르게 추천했을까요? 너의 생각을 자유롭게 적어보세요.")
    if st.button("내 생각 제출하기"):
        st.success("생각이 제출되었습니다. 아래는 AI 오답 가능성에 대한 일반적인 설명이에요:")
        with st.expander("🧠 AI 오답 이유 설명 보기"):
            st.markdown("""
            - **데이터 수가 부족하거나 다양성이 적었다**  
              → 학습한 데이터가 충분히 다양하지 않으면 잘못된 일반화를 할 수 있어요.

            - **AI는 맥락을 이해하지 못한다**  
              → 대부분의 AI는 사용자의 기분, 상황의 뉘앙스를 깊이 있게 이해하지 못해요.

            - **내가 기대한 행동이 정답이라는 보장이 없다**  
              → AI는 '정답'이 아니라 '확률상 가능성이 높은 행동'을 예측할 뿐이에요.
            """)

    st.markdown("---")
    st.markdown("## ✍️ 내가 느낀 점")
    best_skill = st.selectbox(
        "내가 가장 자신 있었던 과정은?",
        [
            "데이터 수집", "패턴 찾기", "알고리즘 작성",
            "AI 학습시키기", "AI 추천 분석", "요약 정리"
        ]
    )
    reflection = st.text_area("이 활동을 통해 새롭게 알게 된 점이나 느낀 점을 자유롭게 적어보세요.")

    if st.button("형성평가 제출하기"):
        st.success("제출이 완료되었습니다. 수고 많았어요! 🎉")
