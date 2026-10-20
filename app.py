import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="Flappy Bird 120 FPS",
    page_icon="🐦",
    layout="centered"
)

st.title("🐦 Flappy Bird - Custom Graphics & Countdown")
st.markdown("Nhấn **Spacebar**, **Mũi tên lên** hoặc **Click chuột** để bắt đầu và bay!")

# Mã HTML/JS của game Flappy Bird
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

// Trạng thái game: 0: Chờ, 1: Đếm ngược, 2: Đang chơi, 3: Thua
const state = { getReady: 0, countdown: 1, game: 2, over: 3 };
let currentGameState = state.getReady;

let countdownTimer = 3;
let countdownInterval = null;

// Chim (Bird) - Thiết kế đẹp hơn, có má hồng và hiệu ứng cánh
const bird = {
    x: 80,
    y: 250,
    radius: 14,
    gravity: 0.18,
    jump: -4.2,
    speed: 0,
    rotation: 0,
    
    draw: function() {
        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.rotate(this.rotation);
        
        // Thân chim (Gradient vàng-cam bắt mắt)
        let bodyGrad = ctx.createRadialGradient(-3, -3, 2, 0, 0, this.radius);
        bodyGrad.addColorStop(0, '#ffee58');
        bodyGrad.addColorStop(1, '#ffa726');
        
        ctx.fillStyle = bodyGrad;
        ctx.beginPath();
        ctx.arc(0, 0, this.radius, 0, Math.PI * 2);
        ctx.fill();
        ctx.lineWidth = 2;
        ctx.strokeStyle = '#e65100';
        ctx.stroke();

        // Má hồng dễ thương
        ctx.fillStyle = 'rgba(255, 82, 82, 0.5)';
        ctx.beginPath();
        ctx.arc(4, 3, 3.5, 0, Math.PI * 2);
        ctx.fill();

        // Mắt chim (To, long lanh hơn)
        ctx.fillStyle = '#fff';
        ctx.beginPath();
        ctx.arc(5, -4, 4.5, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = '#000';
        ctx.beginPath();
        ctx.arc(6.5, -4, 2, 0, Math.PI * 2);
        ctx.fill();

        // Mỏ chim (3D hơn)
        ctx.fillStyle = '#ff7043';
        ctx.beginPath();
        ctx.moveTo(11, -2);
        ctx.lineTo(20, 2);
        ctx.lineTo(11, 6);
        ctx.closePath();
        ctx.fill();
        ctx.strokeStyle = '#d84315';
        ctx.stroke();

        // Cánh chim vỗ nhẹ theo nhịp frames
        ctx.fillStyle = '#fbc02d';
        ctx.beginPath();
        let wingOffset = Math.sin(frames * 0.3) * 3;
        ctx.ellipse(-3, 2 + wingOffset, 5, 3, Math.PI / 4, 0, Math.PI * 2);
        ctx.fill();
        ctx.stroke();

        ctx.restore();
    },
    
    flap: function() {
        this.speed = this.jump;
    },
    
    update: function() {
        if (currentGameState === state.getReady) {
            this.y = 250 + Math.sin(frames * 0.1) * 8;
            this.rotation = 0;
        } else if (currentGameState === state.countdown) {
            this.y = 250;
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
        this.y = 250;
        this.rotation = 0;
    }
};

// Ống nước (Pipes)
const pipes = {
    position: [],
    w: 60,
    h: 400,
    gap: 165,
    dx: 1.8,

    draw: function() {
        for
