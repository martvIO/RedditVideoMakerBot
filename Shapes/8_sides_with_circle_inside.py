import turtle
import math

# === Setup ===
def setup_turtle():
    t = turtle.Turtle()
    t.speed(0)  # Fastest drawing speed
    t.pensize(2)  # Line thickness
    screen = turtle.Screen()
    screen.bgcolor("light gray")
    return t, screen

# === Drawing Functions ===
def draw_circle(t, x, y, radius, fill_color="gray"):
    t.penup()
    t.goto(x, y - radius)
    t.pendown()
    t.fillcolor(fill_color)
    t.begin_fill()
    t.circle(radius)
    t.end_fill()

def draw_octagon(t, side_length):
    angle = 360 / 8  # 45 degrees for an octagon
    t.penup()
    t.goto(-side_length / 2, -side_length)
    t.pendown()
    for _ in range(8):
        t.forward(side_length)
        t.left(angle)

# === Main Drawing ===
def main():
    t, screen = setup_turtle()

    # Draw shapes
    draw_octagon(t, side_length=80)
    draw_circle(t, x=0, y=15, radius=30)

    # Finish
    t.hideturtle()
    screen.exitonclick()

if __name__ == "__main__":
    main()