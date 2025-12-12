import streamlit as st
import streamlit.components.v1 as components

# 페이지 설정
st.set_page_config(page_title="물리 엔진 시뮬레이션", layout="centered")

st.title("🍎 꽉 막힌 물리 엔진 방 (Matter.js)")
st.markdown("---")
st.info("이제 천장도 막혀있습니다! 공을 세게 던져보세요.")

# HTML/JS 코드
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
      let ground, ceiling, leftWall, rightWall;
      let mConstraint;

      function setup() {
        createCanvas(600, 450);

        // 1. 엔진 생성
        engine = Engine.create();
        world = engine.world;
        world.gravity.y = 1; 

        // 2. 사방 벽 생성 (천장 추가됨!)
        // 바닥
        ground = Bodies.rectangle(width / 2, height, width, 50, { isStatic: true });
        // 천장 (y=0 위치에 생성)
        ceiling = Bodies.rectangle(width / 2, 0, width, 50, { isStatic: true });
        // 왼쪽 벽
        leftWall = Bodies.rectangle(0, height/2, 50, height, { isStatic: true });
        // 오른쪽 벽
        rightWall = Bodies.rectangle(width, height/2, 50, height, { isStatic: true });
        
        // 월드에 모든 벽 추가
        World.add(world, [ground, ceiling, leftWall, rightWall]);

        // 3. 마우스 설정
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

        Runner.run(Runner.create(), engine);
      }

      function mouseClicked() {
        if (!mConstraint.body) {
           let r = random(10, 20);
           let newBall = Bodies.circle(mouseX, mouseY, r, {
             restitution: 0.9, // 탄성 (더 잘 튀기게 설정)
             friction: 0.005,
             density: 0.04
           });
           World.add(world, newBall);
        }
      }

      function draw() {
        background(240);

        // 벽 그리기 (회색)
        noStroke();
        fill(100);
        rectMode(CENTER);
        rect(ground.position.x, ground.position.y, width, 50); // 바닥
        rect(ceiling.position.x, ceiling.position.y, width, 50); // 천장
        rect(leftWall.position.x, leftWall.position.y, 50, height); // 왼쪽
        rect(rightWall.position.x, rightWall.position.y, 50, height); // 오른쪽

        // 공 그리기
        let bodies = Composite.allBodies(world);
        for (let i = 0; i < bodies.length; i++) {
          let body = bodies[i];
          if (body.isStatic) continue; // 벽은 위에서 이미 그림

          fill(255, 0, 100);
          push();
          translate(body.position.x, body.position.y);
          rotate(body.angle);
          ellipse(0, 0, body.circleRadius * 2);
          pop();
        }

        // 마우스 드래그 선
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

components.html(html_code, height=500)
