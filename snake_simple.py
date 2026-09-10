"""
Simple Zero-Dependency Snake Game in Python
Uses Python's built-in `turtle` library (no pip install required!).

Controls:
- Arrow keys or W/A/S/D to move
- Space to pause/resume
- R to restart
"""

import turtle
import time
import random

# Game settings
DELAY = 0.1          # Speed of the game (lower is faster)
SCORE = 0
HIGH_SCORE = 0
IS_PAUSED = False

# Screen setup
wn = turtle.Screen()
wn.title("Simple Snake Game (Zero-Install)")
wn.bgcolor("#121620")
wn.setup(width=800, height=600)
wn.tracer(0)  # Turns off screen animation updates for smooth rendering

# Snake Head
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("#2ecc71")
head.penup()
head.goto(0, 0)
head.direction = "stop"

# Snake Body segments
segments = []

# Food
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("#e74c3c")
food.penup()
food.goto(0, 100)

# Score Pen
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("#f0f3f6")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)


def update_score_display():
    pen.clear()
    pen.write(f"Score: {SCORE}   High Score: {HIGH_SCORE}", align="center", font=("Arial", 16, "bold"))


update_score_display()


# Movement Functions
def go_up():
    if head.direction != "down" and not IS_PAUSED:
        head.direction = "up"


def go_down():
    if head.direction != "up" and not IS_PAUSED:
        head.direction = "down"


def go_left():
    if head.direction != "right" and not IS_PAUSED:
        head.direction = "left"


def go_right():
    if head.direction != "left" and not IS_PAUSED:
        head.direction = "right"


def toggle_pause():
    global IS_PAUSED
    IS_PAUSED = not IS_PAUSED


def reset_game():
    global SCORE, DELAY
    time.sleep(0.5)
    head.goto(0, 0)
    head.direction = "stop"

    # Hide segments off screen
    for segment in segments:
        segment.goto(1000, 1000)
    segments.clear()

    SCORE = 0
    DELAY = 0.1
    update_score_display()


def move():
    if head.direction == "up":
        head.sety(head.ycor() + 20)
    elif head.direction == "down":
        head.sety(head.ycor() - 20)
    elif head.direction == "left":
        head.setx(head.xcor() - 20)
    elif head.direction == "right":
        head.setx(head.xcor() + 20)


# Keyboard Bindings
wn.listen()
# Arrow Keys
wn.onkeypress(go_up, "Up")
wn.onkeypress(go_down, "Down")
wn.onkeypress(go_left, "Left")
wn.onkeypress(go_right, "Right")
# WASD
wn.onkeypress(go_up, "w")
wn.onkeypress(go_down, "s")
wn.onkeypress(go_left, "a")
wn.onkeypress(go_right, "d")
# Special Keys
wn.onkeypress(toggle_pause, "space")
wn.onkeypress(reset_game, "r")

# Main Game Loop
try:
    while True:
        wn.update()

        if not IS_PAUSED:
            # Check for border collision
            if abs(head.xcor()) > 390 or abs(head.ycor()) > 290:
                reset_game()

            # Check for collision with food
            if head.distance(food) < 20:
                # Move food to random spot
                x = random.randint(-18, 18) * 20
                y = random.randint(-13, 13) * 20
                food.goto(x, y)

                # Add a new segment
                new_segment = turtle.Turtle()
                new_segment.speed(0)
                new_segment.shape("square")
                new_segment.color("#27ae60")
                new_segment.penup()
                segments.append(new_segment)

                # Increase score
                SCORE += 10
                if SCORE > HIGH_SCORE:
                    HIGH_SCORE = SCORE

                # Slightly increase speed
                if DELAY > 0.04:
                    DELAY -= 0.002

                update_score_display()

            # Move body segments in reverse order
            for index in range(len(segments) - 1, 0, -1):
                x = segments[index - 1].xcor()
                y = segments[index - 1].ycor()
                segments[index].goto(x, y)

            # Move segment 0 to head
            if len(segments) > 0:
                segments[0].goto(head.xcor(), head.ycor())

            move()

            # Check for head collision with body segments
            for segment in segments:
                if segment.distance(head) < 20:
                    reset_game()

        time.sleep(DELAY)

except (turtle.Terminator, KeyboardInterrupt):
    pass
