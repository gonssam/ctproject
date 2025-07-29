import streamlit as st
import streamlit.components.v1 as htmlviewer

# 페이지 설정
st.set_page_config(layout='wide', page_title='비버랑 CT하자!!')

# 🦫 타이틀 영역
st.title("🦫 비버랑 CT하자!")
st.subheader("💡 Computational Thinking + AI 문제 해결 실습실")
st.markdown("---")

# HTML 문제 불러오기
with open('ct_problem1.html', 'r', encoding='utf-8') as f:
    html1 = f.read()

with open('ct_problem2.html', 'r', encoding='utf-8') as f:
    html2 = f.read()

with open('ai_ct.html', 'r', encoding='utf-8') as f:
    html3 = f.read()

# 본문 레이아웃: 좌측 문제 영역 / 우측 팁 영역
col1, col2 = st.columns((4, 1))

with col1:
    with st.expander('🐝 CT문항 #1: 꿀벌의 꿀 모으기'):
        htmlviewer.html(html1, height=1000)

    with st.expander('🔮 CT문항 #2: 마법 주문 찾기'):
        htmlviewer.html(html2, height=1000)

    with st.expander('🤖 AI기반 CT문항 #3: 스마트 라이프 어시스턴트'):
        htmlviewer.html(html3, height=1100)

with col2:
    with st.expander('🧭 Tips'):
        st.markdown("""
        - 각 문항은 **탭을 따라가며 단계별로 해결**하세요.
        - 입력 예시가 제공되니, 따라하며 실습해보세요.
        - 조건 입력 시 공백을 꼭 확인하세요!
        - **AI 추천이 안 뜰 땐**, 조건문 구문을 다시 확인해보세요.
        - [문제 해결 전략 참고하기](https://csunplugged.org/en/) 🌐
        """)

# 하단 저작권
st.markdown('<hr>', unsafe_allow_html=True)
st.write('<font color="BLUE">(c)copyrighst. all rights reserved by goeunkim', unsafe_allow_html=True)
