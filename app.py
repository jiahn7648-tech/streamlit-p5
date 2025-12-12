import streamlit as st
import pymunk
import matplotlib.pyplot as plt
import numpy as np

# --- 1. 물리 공간(Pymunk Space) 설정 ---
def setup_physics_space():
    space = pymunk.Space()
    space.gravity = (0, 0)  # 중력 비활성화 (당구공 시뮬레이션처럼)
    return space

# --- 2. 공(Circle) 생성 함수 ---
def create_ball(space, position, radius=10, mass=1, elasticity=0.9):
    # Body: 물리적인 속성 (질량, 속도 등)
    moment = pymunk.moment_for_circle(mass, 0, radius)
    body = pymunk.Body(mass, moment)
    body.position = position

    # Shape: 충돌 감지 모양 (원)
    shape = pymunk.Circle(body, radius)
    shape.elasticity = elasticity  # 탄성 계수 (0: 완벽한 비탄성, 1: 완벽한 탄성)
    shape.density = 1

    space.add(body, shape)
    return body

# --- 3. 시뮬레이션 실행 및 시각화 ---
def run_simulation(space, num_balls, initial_impulse_index):
    # 공 리스트 초기화 (Streamlit 세션 상태에 저장)
    if 'balls' not in st.session_state or len(st.session_state.balls) != num_balls:
        st.session_state.balls = []
        for i in range(num_balls):
            # 랜덤 위치에 공 생성 (충돌을 피하기 위해 조금씩 간격 두기)
            pos = (np.random.rand() * 400 + 50, np.random.rand() * 400 + 50)
            ball = create_ball(space, pos)
            st.session_state.balls.append(ball)

    # --- 초기 충격 적용 ---
    if initial_impulse_index >= 0 and initial_impulse_index < len(st.session_state.balls):
        # 첫 번째 공(index 0)에 오른쪽으로 초기 속도 부여 (원하는 대로 인덱스 변경 가능)
        ball_to_hit = st.session_state.balls[initial_impulse_index]
        if ball_to_hit.velocity == (0, 0): # 이미 움직이고 있지 않을 때만 적용
            # 충격량 (Impulse) 적용: 힘 * 시간
            ball_to_hit.apply_impulse_at_local_point((4000, 0), (0, 0))


    # --- 시뮬레이션 루프 ---
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(0, 500)
    ax.set_ylim(0, 500)
    ax.set_aspect('equal')
    ax.set_title("Pymunk 충돌 시뮬레이션 (Streamlit)")
    
    # 500번의 물리 프레임을 계산 (충돌 및 움직임)
    for _ in range(500):
        space.step(0.02)  # 0.02초 간격으로 시뮬레이션 진행

    # --- 시각화 ---
    for i, body in enumerate(st.session_state.balls):
        x, y = body.position
        radius = 10 # Pymunk에서 설정한 공의 반지름
        
        # Matplotlib을 사용하여 원 그리기
        circle = plt.Circle((x, y), radius, color='blue' if i != initial_impulse_index else 'red', fill=True)
        ax.add_artist(circle)
        
    st.pyplot(fig)
    
    # 디버깅 정보
    st.write(f"첫 번째 공 속도: {st.session_state.balls[0].velocity}")
    st.button("시뮬레이션 재시작", on_click=reset_simulation)

def reset_simulation():
    if 'balls' in st.session_state:
        del st.session_state.balls
        
# --- 4. Streamlit UI 구성 ---
st.title("🎱 Streamlit & Pymunk 기반 충돌 시뮬레이션")

num_balls = st.slider("공의 개수", 2, 10, 5)
hit_ball_index = st.number_input("충격을 가할 공 번호 (0부터 시작)", 0, num_balls - 1, 0)
st.markdown("---")

if st.button("시뮬레이션 시작"):
    st.session_state.simulation_started = True

if 'simulation_started' in st.session_state and st.session_state.simulation_started:
    
    # 물리 공간 초기화 및 실행
    space = setup_physics_space()
    run_simulation(space, num_balls, hit_ball_index)

else:
    st.info("위 설정을 완료하고 '시뮬레이션 시작' 버튼을 눌러주세요.")
