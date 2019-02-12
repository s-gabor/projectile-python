from math import radians, sin, cos
from graphics import *


class Target:
    def __init__(self, win):
        self.win = win
        self.x = 50
        self.center = center = Point(self.x, 0)
        self.p1 = Point(center.getX()-10, -5)
        self.p2 = Point(center.getX()+10, 5)
        self.target = self.draw()

    def getEdges(self):
        return self.p1.getX(), self.p2.getX()

    def draw(self):
        target = Oval(self.p1, self.p2).draw(self.win)
        target.setFill("lightgrey")
        return target

    def move(self, dx):
        self.x = self.x + dx
        self.target.move(dx,0)

    def getX(self):
        return self.x


class Projectile:
    """object to simulate a projectile."""
    def __init__(self, angle, vel, h0):
        theta = radians(angle)
        self.xpos = 0
        self.ypos = h0
        self.xvel = vel * cos(theta) #constant(no wind resistance)
        self.yvel = vel * sin(theta) #variable(because of gravity)

    def getX(self):
        return self.xpos

    def getY(self):
        return self.ypos

    def update(self, t):
        self.xpos = self.xpos + self.xvel * t
        self.yvel = self.yvel - 9.8 * t
        self.ypos = self.ypos + self.yvel * t


class ShotTracker:
    """sincronize the projectile with a grafic representation of a ball."""
    def __init__(self, win, angle, velocity, height):
        self.proj = Projectile(angle, velocity, height)
        self.marker = Circle(Point(0, height), 2.5).draw(win)
        self.marker.setFill("red")
        self.marker.setOutline("red")

    def update(self, dt):
        self.proj.update(dt)
        center = self.marker.getCenter()
        dx = self.proj.getX() - center.getX()
        dy = self.proj.getY() - center.getY()
        self.marker.move(dx, dy)

    def getX(self):
        return self.proj.getX()

    def getY(self):
        return self.proj.getY()

    def undraw(self):
        self.marker.undraw()


class Launcher:
    """Launcher object represented by an arrow and a ball.
    The ball is only a dummy display. The real ball is from ShotTracker,
    which appears when the fire method is called.
    The arrow will adjust dynamically with user interaction.
    Methods: adjAngle(), adjVel(), redraw()."""
    def __init__(self, win):
        """Creates the launcher(the ball and the arrow)."""
        self.height = 0
        self.win = win
        self.angle = 45  # degrees
        self.vel = 35
        # create the representation for the launcher(a vector)
        self.arrow = Line(Point(0,0), Point(0, 0)).draw(win)
        self.base = Circle(Point(0,0), 3).draw(win)
        self.redraw()

    def adjAngle(self, amt):
        self.angle = self.angle + amt
        self.redraw()

    def adjVel(self, amt):
        self.vel = self.vel + amt
        self.redraw()

    def adjHeight(self, amt):
        self.height = max(self.height + amt, 0)            
        self.redraw()

    def redraw(self):
        self.arrow.undraw()
        self.base.undraw()
        p1 = Point(0,self.height)
        p2 = Point(self.vel * cos(radians(self.angle)), self.vel * sin(radians(self.angle)) + self.height)
        self.arrow = Line(p1, p2).draw(self.win)
        self.arrow.setArrow("last")
        self.arrow.setWidth(3)
        self.base = Circle(Point(0,self.height), 2.5).draw(self.win)
        self.base.setFill("red")
        self.base.setOutline("red")

    def fire(self):
        return ShotTracker(self.win, self.angle, self.vel, self.height)


class ProjectileApp:
    """This acts like the main program.
    Contains the window, the launcher and 2 methods:
    - updateShots() -> bacically updates the list of shots(which ones are still active)
    - run() -> has 2 parts: update the list of shots and interact with the user
    by checking the keys pressed."""
    def __init__(self):
        self.win = win = GraphWin("Projectile App", 1000, 800, autoflush=False)
        win.setCoords(-10, -10, 210, 210)
        Line(Point(-5, 0), Point(205, 0)).draw(win)
        for i in range(0, 210, 50):
            Line(Point(i, 0), Point(i, 2.5)).draw(win)
            Text(Point(i,-6), i).draw(win)
        self.launcher = Launcher(win)
        self.target = Target(win)
        self.shots = []
        Text(Point(100,185), "HIT THE MOVING TARGET\n\nf = fire\ne & d = adjust initial height\nUp & Down = adjust the angle\nLeft & Right = adjust velocity\nq to quit").draw(win)
        # self.score.setWidth()

    def updateShots(self, dt):
        alive = []
        for shot in self.shots:
            shot.update(dt)
            if shot.getY() >= 0 and shot.getX() < 200:
                alive.append(shot)
            else:
                shot.undraw()
        self.shots = alive

    def run(self):
        dx = 0.1
        scoreText = Text(Point(100,150), "SCORE = 0").draw(self.win)
        scoreText.setSize(25)
        scoreText.setStyle("bold")
        score = 0
        while True:
            if self.target.getX() > 170 or self.target.getX() < 50:
                dx = -dx
            self.target.move(dx)
            self.updateShots(1/30)
            key = self.win.checkKey()
            if key == "q":
                break
            if key == "Up":
                self.launcher.adjAngle(5)
            elif key == "Down":
                self.launcher.adjAngle(-5)
            elif key == "Right":
                self.launcher.adjVel(5)
            elif key == "Left":
                self.launcher.adjVel(-5)
            elif key == "e":
                self.launcher.adjHeight(5)
            elif key == "d":
                self.launcher.adjHeight(-5)
            elif key == "f":
                self.shots.append(self.launcher.fire())
            left = self.target.getX() - 10
            right = self.target.getX() + 10
            for shot in self.shots:
                # print(left, right, shot.getX(), shot.getY())
                if left < shot.getX() < right and shot.getY() < 0.75:
                    score = score + 1
                    text = "Score = " + str(score)
                    scoreText.setText(text)
            update(30)
        self.win.close()


if __name__ == "__main__":
    ProjectileApp().run()
