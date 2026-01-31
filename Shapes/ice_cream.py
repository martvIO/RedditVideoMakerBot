import turtle

def draw_circle(t, x, y, radius):
    """Draw a filled circle at the specified position"""
    t.penup()
    t.goto(x, y - radius)  # Position at bottom of circle
    t.pendown()
    t.begin_fill()
    t.circle(radius)
    t.end_fill()

# Setup the turtle
t = turtle.Turtle()
t.speed(8)
screen = turtle.Screen()
screen.bgcolor("white")
t.color("black")
t.fillcolor("gray")

# Draw the triangle (body)
t.penup()
t.goto(100, 100)  # Bottom left of the triangle
t.pendown()
t.begin_fill()
t.goto(-100, 100)  # Bottom right of the triangle
t.goto(0, -100)     # Top of the triangle
t.goto(100, 100)  # Back to start
t.end_fill()

# Draw the three circles (head and shoulders)
draw_circle(t, 0, 200, 30)     # Top center circle
draw_circle(t, -40, 130, 30)   # Left circle
draw_circle(t, 40, 130, 30)    # Right circle

# Hide the turtle and display the result
t.hideturtle()
turtle.done()