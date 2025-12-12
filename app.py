import streamlit as st
import streamlit.components.v1 as components

# 페이지 설정
st.set_page_config(page_title="물리 엔진 시뮬레이션", layout="centered")

st.title("🍎 현실적인 2D 물리 엔진 (Matter.js)")
st.markdown("---")
st.info("화면을 클릭하여 공을 생성하고, 드래그하여 던져보세요!")

# HTML/JS 코드 (물리 엔진을 직접 포함)
html_code = """
<!DOCTYPE html>
<html>
  <head>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.4.0/p5.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/matter-js/0.18.0/matter.min.js"></script>
    <style>
      body { margin: 0; padding: 0; overflow: hidden; }
      canvas { display: block; }
    </style>
  </head>
  <body>
    <script>
      // Matter.js 모듈 별칭
      let Engine = Matter.Engine,
          Render = Matter.Render,
          Runner = Matter.Runner,
          Bodies = Matter.Bodies,
          Composite = Matter.Composite,
          MouseConstraint = Matter.MouseConstraint,
          Mouse = Matter.Mouse,
          World = Matter.World;

      let engine;
      let world;
      let ground;
      let mConstraint;

      function setup() {
        createCanvas(600, 450);

        // 1. 엔진 생성 및 중력 설정
        engine = Engine.create();
        world = engine.world;
        world.gravity.y = 1; 

        // 2. 바닥 및 벽 생성
        ground = Bodies.rectangle(width / 2, height, width, 50, { isStatic: true });
        let leftWall = Bodies.rectangle(0, height/2, 50, height, { isStatic: true });
        let rightWall = Bodies.rectangle(width, height/2, 50, height, { isStatic: true });
        
        World.add(world, [ground, leftWall, rightWall]);

        // 3. 마우스 상호작용 설정
        let canvasmouse = Mouse.create(canvas.elt);
        canvasmouse.pixelRatio = pixelDensity();
        let options = {
          mouse: canvasmouse,
          constraint: {
             stiffness: 0.2,
             render: { visible: false }
          }
        }
        
        mConstraint = MouseConstraint.create(engine, options);
        World.add(world, mConstraint);

        // 4. 물리 시뮬레이션 시작
        Runner.run(Runner.create(), engine);
      }

      function mouseClicked() {
        // 드래그 중이 아닐 때만 공 생성
        if (!mConstraint.body) {
           let r = random(10, 20);
           let newBall = Bodies.circle(mouseX, mouseY, r, {
             restitution: 0.8,
             friction: 0.005,
             density: 0.04,
             render: { fillStyle: '#FF0055' }
           });
           World.add(world, newBall);
        }
      }

      function draw() {
        background(240);

        // 바닥 그리기
        noStroke();
        fill(100);
        rectMode(CENTER);
        rect(ground.position.x, ground.position.y, width, 50);

        // 공 그리기
        let bodies = Composite.allBodies(world);
        for (let i = 0; i < bodies.length; i++) {
          let body = bodies[i];
          if (body.isStatic) continue;

          fill(255, 0, 100);
          push();
          translate(body.position.x, body.position.y);
          rotate(body.angle);
          ellipse(0, 0, body.circleRadius * 2);
          pop();
        }

        // 드래그 선 그리기
        if (mConstraint.body) {
          let pos = mConstraint.body.position;
          let offset = mConstraint.constraint.pointB;
          let m = mConstraint.mouse.position;
          stroke(0, 255, 0);
          line(pos.x + offset.x, pos.y + offset.y, m.x, m.y);
        }
      }
    </script>
  </body>
</html>
"""

# Streamlit 내장 함수로 HTML 실행
components.html(html_code, height=500)
