import turtle
import math

# Set up the turtle
t = turtle.Turtle()
t.speed(8)  # Set drawing speed (1=slowest, 0=fastest)
screen = turtle.Screen()
screen.bgcolor("light gray")  # Match background color of the image

# Function to draw a filled circle
def draw_circle(x, y, radius):
    t.penup()
    t.goto(x, y - radius)  # Position to start drawing circle
    t.pendown()
    t.begin_fill()
    t.circle(radius)
    t.end_fill()

# Set up the drawing
t.pensize(2)  # Set line thickness

# Draw the square
side_length = 200
t.penup()
t.goto(-side_length/2, -side_length/2)  # Start at bottom left
t.pendown()
for _ in range(4):
    t.forward(side_length)
    t.left(90)

line_off = 10
# Draw the diagonal line
t.penup()
t.goto(-side_length/2 - line_off, -side_length/2 - line_off)  # Start at bottom left
t.pendown()
t.goto(side_length/2 + line_off, side_length/2 + line_off)  # Go to top right

# Draw the two filled circles
circle_radius = 20
# First circle - top left quadrant
draw_circle(-side_length/4, side_length/4, circle_radius)
# Second circle - bottom right quadrant
draw_circle(side_length/4, -side_length/4, circle_radius)

# Hide the turtle and display the result
t.hideturtle()
screen.exitonclick()  # Click to close the window