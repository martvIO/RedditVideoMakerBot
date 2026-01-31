import turtle

def draw_nested_squares():
    # Set up the turtle
    t = turtle.Turtle()
    t.speed(0)  # Fastest speed
    t.pensize(2)
    
    # Set up the screen
    screen = turtle.Screen()
    screen.bgcolor("light gray")
    
    # Starting position - slightly left and down to center the drawing
    t.penup()
    t.goto(-150, -150)
    t.pendown()
    
    # Draw outer square
    t.color("black")
    for _ in range(4):
        t.forward(300)
        t.left(90)
    
    # Move to position for middle square
    t.penup()
    t.goto(-50, -50)
    t.pendown()
    
    # Draw middle square
    for _ in range(4):
        t.forward(150)
        t.left(90)
    
    # Move to position for inner square
    t.penup()
    t.goto(0, 0)
    t.pendown()
    
    # Draw inner square
    for _ in range(4):
        t.forward(75)
        t.left(90)
    
    # Move to position for inner square
    t.penup()
    t.goto(20, 20)
    t.pendown()
    
    # Draw inner square
    t.begin_fill()  # Fill the inner square with black
    for _ in range(4):
        t.forward(45)
        t.left(90)
    t.end_fill()
    
    # Move to position for inner square
    t.penup()
    t.goto(150, 150)
    t.pendown()
    
    # Draw inner square
    t.begin_fill()  # Fill the inner square with black
    t.goto(20,20)
    t.end_fill()
    # Hide the turtle and display the result
    t.hideturtle()
    
    # Keep the window open
    turtle.done()

# Run the function
if __name__ == "__main__":
    draw_nested_squares()