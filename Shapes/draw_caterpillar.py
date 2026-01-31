import turtle

def draw_caterpillar():
    # Set up the turtle
    t = turtle.Turtle()
    t.speed(0)  # Fastest speed
    screen = turtle.Screen()
    screen.bgcolor("light gray")
    
    # Starting position
    t.penup()
    t.goto(-150, 0)
    t.pendown()
    ups = [0,10,5,20,10,15]
    # Draw the body (6 circles)
    for i in range(6):
        t.penup()
        t.goto(-150 + i*50, ups[i])
        t.pendown()
        t.begin_fill()
        t.circle(25)
        t.end_fill()
    
    # Draw the head (one circle with face)
    t.penup()
    t.goto(-150 + 6*50, ups[-1]+0)
    t.pendown()
    t.begin_fill()
    t.circle(25)
    t.end_fill()
    
    # Draw the face
    # Eyes
    t.penup()
    t.goto(-150 + 6*50 - 10, ups[-1]+30)
    t.pendown()
    t.color("white")
    t.begin_fill()
    t.circle(5)
    t.end_fill()
    
    t.penup()
    t.goto(-150 + 6*50 + 10, ups[-1]+30)
    t.pendown()
    t.begin_fill()
    t.circle(5)
    t.end_fill()
    
    # Smile
    t.penup()
    t.goto(-150 + 6*50 - 10, ups[-1]+20)
    t.pendown()
    t.color("white")
    t.right(90)
    t.circle(10, 180)
    
    # Antenna
    t.penup()
    t.goto(-150 + 6*50 - 5, ups[-1]+50)
    t.pendown()
    t.color("black")
    t.left(40)
    t.forward(30)
    
    t.penup()
    t.goto(-150 + 6*50 + 5, ups[-1]+50)
    t.pendown()
    t.setheading(90)  # Reset heading to point up
    t.right(30)
    t.forward(30)
    
    # Hide the turtle and display the result
    t.hideturtle()
    
    # Keep the window open
    turtle.done()

# Run the function
if __name__ == "__main__":
    draw_caterpillar()