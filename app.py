import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="Flappy Bird 120 FPS - High Graphics",
    page_icon="🐦",
    layout="centered"
)

st.title("🐦 Flappy Bird - High Graphics (120 FPS)")
st.markdown("Nhấn **Spacebar** hoặc **Click chuột** để bay. Cố gắng vượt qua các ống nước nhé!")

# Mã HTML / JavaScript chứa game Flappy Bird đồ họa cao
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
            background: #1a1a1a;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            overflow: hidden;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        canvas {
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            border-radius: 12px;
            background: #70c5ce;
        }
    </style>
</head>
<body>

<canvas id="gameCanvas" width="400" height="600"></canvas>

<script>
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

// Biến game
let frames = 0;
let score = 0;
let highScore = localStorage.getItem("flappyHighScore") || 0;
let state = { current: 0, getReady: 0, game: 1, over: 2 };

// Trạng thái hiện tại
let currentGameState = state.getReady;

// Đối tượng Chim (Bird) với đồ họa cao cấp hơn
const bird = {
    x: 50,
    y: 150,
    w: 34,
    h: 24,
    radius: 12,
    gravity: 0.22,      // Trọng lực tinh chỉnh cho mượt
    jump: -4.6,         // Lực nhảy
    speed: 0,
    rotation: 0,
    
    draw: function() {
        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.rotate(this.rotation);
        
        // Vẽ thân chim (Gradient vàng cam)
        let gradient = ctx.createRadialGradient(-4, -4, 2, 0, 0, this.radius);
        gradient.addColorStop(0, '#ffeb3b');
        gradient.addColorStop(1, '#ff9800');
        
        ctx.fillStyle = gradient;
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
        // Nếu đang ở màn hình chờ, chim bay lên xuống nhẹ nhàng
        if (currentGameState === state.getReady) {
            this.y = 150 + Math.sin(frames * 0.1) * 8;
            this.rotation = 0;
        } else {
            this.speed += this.gravity;
            this.y += this.speed;

            // Giới hạn không cho bay ra khỏi màn hình trên
            if (this.y <= this.radius) {
                this.y = this.radius;
                this.speed = 0;
            }

            // Kiểm tra chạm đất
            if (this.y + this.radius >= canvas.height - 100) {
                this.y = canvas.height - 100 - this.radius;
                if (currentGameState === state.game) {
                    currentGameState = state.over;
                }
            }

            // Góc quay của chim theo vận tốc
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

// Các ống nước (Pipes)
const pipes = {
    position: [],
    w: 65,
    h: 400,
    gap: 130,
    maxYPos: -150,
    dx: 2.2, // Tốc độ di chuyển ống

    draw: function() {
        for (let i = 0; i < this.position.length; i++) {
            let p = this.position[i];
            let topYPos = p.y;
            let bottomYPos = p.y + this.h + this.gap;

            // Ống trên (Gradient xanh lá hiện đại)
            let pipeGradTop = ctx.createLinearGradient(p.x, 0, p.x + this.w, 0);
            pipeGradTop.addColorStop(0, '#2ecc71');
            pipeGradTop.addColorStop(0.5, '#27ae60');
            pipeGradTop.addColorStop(1, '#1e8449');

            ctx.fillStyle = pipeGradTop;
            ctx.fillRect(p.x, topYPos, this.w, this.h);
            // Viền ống
            ctx.lineWidth = 2;
            ctx.strokeStyle = '#145a32';
            ctx.strokeRect(p.x, topYPos, this.w, this.h);
            // Đầu ống trên
            ctx.fillRect(p.x - 4, topYPos + this.h - 25, this.w + 8, 25);
            ctx.strokeRect(p.x - 4, topYPos + this.h - 25, this.w + 8, 25);

            // Ống dưới
            let pipeGradBottom = ctx.createLinearGradient(p.x, 0, p.x + this.w, 0);
            pipeGradBottom.addColorStop(0, '#2ecc71');
            pipeGradBottom.addColorStop(0.5, '#27ae60');
            pipeGradBottom.addColorStop(1, '#1e8449');

            ctx.fillStyle = pipeGradBottom;
            ctx.fillRect(p.x, bottomYPos, this.w, this.h);
            ctx.strokeRect(p.x, bottomYPos, this.w, this.h);
            // Đầu ống dưới
            ctx.fillRect(p.x - 4, bottomYPos, this.w + 8, 25);
            ctx.strokeRect(p.x - 4, bottomYPos, this.w + 8, 25);
        }
    },

    update: function() {
        if (currentGameState !== state.game) return;

        // Sinh ống mới mỗi 100 khung hình
        if (frames % 100 === 0) {
            this.position.push({
                x: canvas.width,
                y: Math.floor(Math.random() * (this.maxYPos - (-320 + 50) + 1)) + (-320 + 50),
                passed: false
            });
        }

        for (let i = 0; i < this.position.length; i++) {
            let p = this.position[i];
            p.x -= this.dx;

            // Kiểm tra va chạm với chim
            let bottomYPos = p.y + this.h + this.gap;
            
            // Va chạm ống trên
            if (bird.x + bird.radius > p.x && bird.x - bird.radius < p.x + this.w &&
                bird.y - bird.radius < p.y + this.h) {
                currentGameState = state.over;
            }
            // Va chạm ống dưới
            if (bird.x + bird.radius > p.x && bird.x - bird.radius < p.x + this.w &&
                bird.y + bird.radius > bottomYPos) {
                currentGameState = state.over;
            }

            // Tính điểm khi vượt qua ống
            if (p.x + this.w < bird.x && !p.passed) {
                score++;
                p.passed = true;
                if (score > highScore) {
                    highScore = score;
                    localStorage.setItem("flappyHighScore", highScore);
                }
            }

            // Xóa ống khi ra khỏi màn hình
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

// Nền phía sau (Background)
const background = {
    draw: function() {
        // Bầu trời chuyển màu gradient
        let bgGrad = ctx.createLinearGradient(0, 0, 0, canvas.height);
        bgGrad.addColorStop(0, '#4fc3f7');
        bgGrad.addColorStop(1, '#81d4fa');
        ctx.fillStyle = bgGrad;
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // Vẽ mây cách điệu
        ctx.fillStyle = 'rgba(255, 255, 255, 0.6)';
        ctx.beginPath();
        ctx.arc(80, 100, 30, 0, Math.PI * 2);
        ctx.arc(110, 90, 40, 0, Math.PI * 2);
        ctx.arc(140, 105, 25, 0, Math.PI * 2);
        ctx.fill();

        ctx.beginPath();
        ctx.arc(280, 200, 25, 0, Math.PI * 2);
        ctx.arc(310, 190, 35, 0, Math.PI * 2);
        ctx.fill();

        // Mặt đất
        ctx.fillStyle = '#deb887';
        ctx.fillRect(0, canvas.height - 100, canvas.width, 100);

        // Lớp cỏ trên mặt đất
        ctx.fillStyle = '#4caf50';
        ctx.fillRect(0, canvas.height - 100, canvas.width, 18);

        // Đất sọc sọc trang trí
        ctx.fillStyle = '#8d6e63';
        for (let i = 0; i < canvas.width; i += 30) {
            ctx.fillRect(i + (frames * 2) % 30, canvas.height - 82, 15, 82);
        }
    }
};

// Xử lý sự kiện bàn phím và chuột
function handleInput() {
    switch (currentGameState) {
        case state.getReady:
            currentGameState = state.game;
            bird.flap();
            break;
        case state.game:
            bird.flap();
            break;
        case state.over:
            // Reset game
            score = 0;
            pipes.reset();
            bird.reset();
            currentGameState = state.getReady;
            break;
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

// Vòng lặp game tối ưu cho tốc độ khung hình cao (hỗ trợ 120 FPS dựa trên requestAnimationFrame)
function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    background.draw();
    pipes.draw();
    bird.draw();

    // Hiển thị giao diện theo trạng thái
    if (currentGameState === state.getReady) {
        ctx.fillStyle = "#fff";
        ctx.font = "bold 30px 'Segoe UI'";
        ctx.textAlign = "center";
        ctx.fillText("NHẤN ĐỂ CHƠI", canvas.width / 2, canvas.height / 2 - 50);
        
        ctx.font = "16px 'Segoe UI'";
        ctx.fillText("Dùng Space hoặc Click chuột", canvas.width / 2, canvas.height / 2 - 10);
    } else if (currentGameState === state.game) {
        ctx.fillStyle = "#fff";
        ctx.font = "bold 40px 'Segoe UI'";
        ctx.textAlign = "center";
        ctx.fillText(score, canvas.width / 2, 70);
    } else if (currentGameState === state.over) {
        // Bảng điểm game over
        ctx.fillStyle = "rgba(0, 0, 0, 0.4)";
        ctx.fillRect(50, 180, 300, 220);
        ctx.strokeStyle = "#fff";
        ctx.lineWidth = 2;
        ctx.strokeRect(50, 180, 300, 220);

        ctx.fillStyle = "#ff5252";
        ctx.font = "bold 35px 'Segoe UI'";
        ctx.textAlign = "center";
        ctx.fillText("THUA RỒI!", canvas.width / 2, 230);

        ctx.fillStyle = "#fff";
        ctx.font = "20px 'Segoe UI'";
        ctx.fillText("Điểm: " + score, canvas.width / 2, 280);
        ctx.fillText("Cao nhất: " + highScore, canvas.width / 2, 320);

        ctx.font = "16px 'Segoe UI'";
        ctx.fillStyle = "#ffeb3b";
        ctx.fillText("Nhấn để chơi lại", canvas.width / 2, 370);
    }
}

function update() {
    bird.update();
    pipes.update();
}

function loop() {
    update();
    draw();
    frames++;
    requestAnimationFrame(loop);
}

loop();
</script>

</body>
</html>
"""

# Hiển thị game vào Streamlit với chiều cao phù hợp
components.html(flappy_bird_html, height=650)
