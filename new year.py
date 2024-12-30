from flask import Flask, render_template_string
import time

app = Flask(__name__)

def heart_shape(msg="Merry Christmas"):
    lines = []
    for y in range(15, -15, -1):
        line = ""
        for x in range(-30, 30):
            f = ((x * 0.05) ** 2 + (y * 0.1) ** 2 - 1) ** 3 - (x * 0.05) ** 2 * (y * 0.1) ** 3
            line += msg[(x - y) % len(msg)] if f <= 0 else " "
        lines.append(line)
    return lines

@app.route('/')
def home():
    result = heart_shape()
    # Render the HTML page with a placeholder for the heart shape
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Heart Shape Animation</title>
        <style>
            body {
                font-family: monospace;
                color: red;
                background-color: black;
                text-align: center;
                margin: 0;
                padding: 0;
                overflow: hidden;
            }
            .heart {
                white-space: pre;
                color: red;
                font-size: 16px;
                line-height: 20px;
                display: inline-block;
                margin-top: 20px;
                opacity: 0;
            }
            .message {
                color: green;
                font-size: 20px;
                font-weight: bold;
            }
            canvas {
                position: absolute;
                top: 0;
                left: 0;
                pointer-events: none;
            }
        </style>
    </head>
    <body>
        <h1 class="message">Merry Christmas</h1>
        <div class="heart" id="heart"></div>
        <canvas id="fireworks"></canvas>

        <script>
            const heartLines = {{ heart_lines|tojson }};
            let lineIndex = 0;
            const heartElement = document.getElementById('heart');
            const fireworksCanvas = document.getElementById('fireworks');
            const ctx = fireworksCanvas.getContext('2d');

            // Firework setup
            fireworksCanvas.width = window.innerWidth;
            fireworksCanvas.height = window.innerHeight;

            const particles = [];
            function Particle(x, y) {
                this.x = x;
                this.y = y;
                this.size = Math.random() * 3 + 1;
                this.speedX = Math.random() * 6 - 3;
                this.speedY = Math.random() * 6 - 3;
                this.life = 100;
                this.opacity = 1;
            }

            Particle.prototype.update = function() {
                this.x += this.speedX;
                this.y += this.speedY;
                this.life -= 2;
                this.opacity = this.life / 100;
                this.size = this.life / 20;
            }

            Particle.prototype.draw = function() {
                ctx.fillStyle = `rgba(255, 165, 0, ${this.opacity})`;
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                ctx.fill();
            }

            function createFireworks() {
                for (let i = 0; i < 100; i++) {
                    particles.push(new Particle(Math.random() * fireworksCanvas.width, Math.random() * fireworksCanvas.height));
                }
            }

            function animateFireworks() {
                ctx.clearRect(0, 0, fireworksCanvas.width, fireworksCanvas.height);
                for (let i = 0; i < particles.length; i++) {
                    particles[i].update();
                    particles[i].draw();
                    if (particles[i].life <= 0) {
                        particles.splice(i, 1);
                        i--;
                    }
                }
                requestAnimationFrame(animateFireworks);
            }

            // Function to animate the heart shape
            function animateHeart() {
                if (lineIndex < heartLines.length) {
                    heartElement.textContent += heartLines[lineIndex] + '\\n';
                    lineIndex++;
                    setTimeout(animateHeart, 50); // Adjust the speed here (50 ms between lines)
                } else {
                    setTimeout(startFireworks, 500); // Wait for a moment before starting fireworks
                }
            }

            function startFireworks() {
                createFireworks();
                animateFireworks();
            }

            // Start the heart animation
            animateHeart();
            heartElement.style.opacity = 1; // Fade the heart into view
        </script>
    </body>
    </html>
    ''', heart_lines=heart_shape())

if __name__ == "__main__":
    app.run(debug=True)
