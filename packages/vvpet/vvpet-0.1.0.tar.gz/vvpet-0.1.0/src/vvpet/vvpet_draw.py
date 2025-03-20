import turtle

def smile():
    mt = turtle.Turtle()
    mt.down()
    mt.speed(0)
    mt.circle(100)

    et = turtle.Turtle()
    et.left(90)
    et.up()
    et.forward(120)
    et.left(90)
    et.forward(30)

    et.down()
    et.circle(10)

    etr = turtle.Turtle()
    etr.left(90)
    etr.up()
    etr.forward(120)
    etr.right(90)
    etr.forward(30)

    etr.down()
    etr.right(180)
    etr.circle(10)

smile()
input()