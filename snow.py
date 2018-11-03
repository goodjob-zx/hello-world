#Draw a snow curve by using recursive method.
#turtle library

from turtle import *
def draw(length, times):
    if(times == 1):
        fd(length)
        left(60)
        fd(length)
        right(120)
        fd(length)
        left(60)
        fd(length)
    else:
        draw(length/3, times-1)
        left(60)
        draw(length/3, times-1)
        right(120)
        draw(length/3, times-1)
        left(60)
        draw(length/3, times-1)
def main():
    setup(1000, 1000)
    penup()
    fd(-300)
    left(90)
    fd(300)
    right(90)
    pensize(2)
    Turtle().screen.delay(0)
    pendown()
    draw(200, 4)
    right(120)
    draw(200, 4)
    right(120)
    draw(200, 4)
    done()
main()
