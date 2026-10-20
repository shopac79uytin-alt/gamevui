import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="Flappy Bird 120 FPS",
    page_icon="🐦",
    layout="centered"
)

st.title("🐦 Flappy Bird - Phiên bản dễ chơi hơn")
st.markdown("Nhấn **Spacebar**, **Mũi tên lên** hoặc **Click chuột** vào màn hình game để bay!")

# Mã HTML/JS của game Flappy Bird đã chỉnh sửa độ khó
flappy_bird_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flappy Bird 120 FPS</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            background: #111;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            overflow: hidden;
            font-family: Arial, sans-serif;
        }
        canvas {
            box-shadow: 0 10px 25px rgba(0,0,0,0.6);
            border-radius: 10px;
            background: #70c5ce;
        }
    </style>
</head>
<body>

<canvas id="gameCanvas" width="400" height="600"></canvas>

<script>
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

let frames = 0;
let score = 0;
let highScore = localStorage.getItem("flappyHighScore") || 0;

// Trạng thái game: 0: Chờ, 1: Đang chơi, 2: Thua
const state = { getReady: 0, game: 1, over: 2 };
let currentGameState = state.getReady;

// Chim (Bird) - Đã chỉnh nhẹ nhàng hơn
const bird = {
    x: 50,
    y: 150,
    radius: 12,
    gravity: 0.18,   // Giảm trọng lực để chim rơi chậm, dễ kiểm soát
    jump: -4.2,      // Lực nhảy vừa phải
    speed: 0,
    rotation: 0,
    
    draw: function() {
        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.rotate(this.rotation);
        
        // Thân chim
        ctx.fillStyle = '#f1c40f';
        ctx.beginPath();
        ctx.arc(0, 0, this.radius, 0, Math.PI * 2);
        ctx.fill();
        ctx.lineWidth = 2;
        ctx.strokeStyle = '#d35400';
        ctx.stroke();

        // Mắt chim
        ctx.fillStyle = '#fff';
        ctx.beginPath();
        ctx.arc(4, -4, 4, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = '#000';
        ctx.beginPath();
        ctx.arc(5, -4, 1.5, 0, Math.PI * 2);
        ctx.fill();

        // Mỏ chim
        ctx.fillStyle = '#e67e22';
        ctx.beginPath();
        ctx.moveTo(10, -2);
        ctx.lineTo(18, 2);
        ctx.lineTo(10, 6);
        ctx.closePath();
        ctx.fill();

        ctx.restore();
    },
    
    flap: function() {
        this.speed = this.jump;
    },
    
    update: function() {
        if (currentGameState === state.getReady) {
            this.y = 150 + Math.sin(frames * 0.1) * 8;
            this.rotation = 0;
        } else {
            this.speed += this.gravity;
            this.y += this.speed;

            if (this.y <= this.radius) {
                this.y = this.radius;
                this.speed = 0;
            }

            if (this.y + this.radius >= canvas.height - 100) {
                this.y = canvas.height - 100 - this.radius;
                if (currentGameState === state.game) {
                    currentGameState = state.over;
                }
            }

            if (this.speed >= this.jump) {
                this.rotation = Math.min(Math.PI / 2, Math.max(-Math.PI / 4, this.rotation + 0.1));
            }
        }
    },
    
    reset: function() {
        this.speed = 0;
        this.y = 150;
        this.rotation = 0;
    }
};

// Ống nước (Pipes) - Đã mở rộng khe hở và làm chậm tốc độ
const pipes = {
    position: [],
    w: 60,
    h: 400,
    gap: 165,       // Tăng khoảng cách giữa ống trên và dưới (cũ là 130)
    dx: 1.8,        // Giảm tốc độ di chuyển ống để có thời gian nhìn trước (cũ là 2.2)

    draw: function() {
        for (let i = 0; i < this.position.length; i++) {
            let p = this.position[i];
            let topY = p.y;
            let bottomY = p.y + this.h + this.gap;

            // Ống trên
            ctx.fillStyle = '#2ecc71';
            ctx.fillRect(p.x, topY, this.w, this.h);
            ctx.lineWidth = 2;
            ctx.strokeStyle = '#145a32';
            ctx.strokeRect(p.x, topY, this.w, this.h);
            ctx.fillRect(p.x - 3, topY + this.h - 24, this.w + 6, 24);
            ctx.strokeRect(p.x - 3, topY + this.h - 24, this.w + 6, 24);

            // Ống dưới
            ctx.fillStyle = '#2ecc71';
            ctx.fillRect(p.x, bottomY, this.w, this.h);
            ctx.strokeRect(p.x, bottomY, this.w, this.h);
            ctx.fillRect(p.x - 3, bottomY, this.w + 6, 24);
            ctx.strokeRect(p.x - 3, bottomY, this.w + 6, 24);
        }
    },

    update: function() {
        if (currentGameState !== state.game) return;

        if (frames % 120 === 0) { // Tăng khoảng thời gian giữa các ống xuất hiện
            this.position.push({
                x: canvas.width,
                y: Math.floor(Math.random() * -150) - 120,
                passed: false
            });
        }

        for (let i = 0; i < this.position.length; i++) {
            let p = this.position[i];
            p.x -= this.dx;

            let bottomY = p.y + this.h + this.gap;

            // Va chạm ống trên
            if (bird.x + bird.radius > p.x && bird.x - bird.radius < p.x + this.w &&
                bird.y - bird.radius < p.y + this.h) {
                currentGameState = state.over;
            }
            // Va chạm ống dưới
            if (bird.x + bird.radius > p.x && bird.x - bird.radius < p.x + this.w &&
                bird.y + bird.radius > bottomY) {
                currentGameState = state.over;
            }

            // Tính điểm
            if (p.x + this.w < bird.x && !p.passed) {
                score++;
                p.passed = true;
                if (score > highScore) {
                    highScore = score;
                    localStorage.setItem("flappyHighScore", highScore);
                }
            }

            if (p.x + this.w <= 0) {
                this.position.shift();
                i--;
            }
        }
    },
    
    reset: function() {
        this.position = [];
    }
};

// Nền (Background)
const background = {
    draw: function() {
        ctx.fillStyle = '#4fc3f7';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.fillStyle = '#deb887';
        ctx.fillRect(0, canvas.height - 100, canvas.width, 100);
        ctx.fillStyle = '#4caf50';
        ctx.fillRect(0, canvas.height - 100, canvas.width, 16);
    }
};

// Điều khiển
function handleInput() {
    if (currentGameState === state.getReady) {
        currentGameState = state.game;
        bird.flap();
    } else if (currentGameState === state.game) {
        bird.flap();
    } else if (currentGameState === state.over) {
        score = 0;
        pipes.reset();
        bird.reset();
        currentGameState = state.getReady;
    }
}

window.addEventListener("keydown", function(e) {
    if (e.code === "Space" || e.code === "ArrowUp") {
        e.preventDefault();
        handleInput();
    }
});

canvas.addEventListener("click", function() {
    handleInput();
});

// Vòng lặp game
function loop() {
    bird.update();
    pipes.update();
    frames++;

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    background.draw();
    pipes.draw();
    bird.draw();

    if (currentGameState === state.getReady) {
        ctx.fillStyle = "#fff";
        ctx.font = "bold 28px Arial";
        ctx.textAlign = "center";
        ctx.fillText("NHẤN ĐỂ CHƠI", canvas.width / 2, canvas.height / 2 - 40);
    } else if (currentGameState === state.game) {
        ctx.fillStyle = "#fff";
        ctx.font = "bold 35px Arial";
        ctx.textAlign = "center";
        ctx.fillText(score, canvas.width / 2, 70);
    } else if (currentGameState === state.over) {
        ctx.fillStyle = "rgba(0, 0, 0, 0.5)";
        ctx.fillRect(60, 180, 280, 200);
        ctx.strokeStyle = "#fff";
        ctx.strokeRect(60, 180, 280, 200);

        ctx.fillStyle = "#ff5252";
        ctx.font = "bold 30px Arial";
        ctx.textAlign = "center";
        ctx.fillText("THUA RỒI!", canvas.width / 2, 230);

        ctx.fillStyle = "#fff";
        ctx.font = "18px Arial";
        ctx.fillText("Điểm: " + score, canvas.width / 2, 275);
        ctx.fillText("Cao nhất: " + highScore, canvas.width / 2, 310);

        ctx.font = "14px Arial";
        ctx.fillStyle = "#ffeb3b";
        ctx.fillText("Click để chơi lại", canvas.width / 2, 350);
    }

    requestAnimationFrame(loop);
}

loop();
</script>

</body>
</html>
"""

components.html(flappy_bird_html, height=650)
