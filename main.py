import tkinter as tk
import random
import math        

class BouncingBallApp:
    def __init__(self, master):
        self.root = master
        self.root.title("Odbijające się piłki")
        
        self.circleCanvas = tk.Canvas(self.root, width=500, height=500, bg="black")
        self.circleCanvas.pack()

        self.buttonAdd = tk.Button(self.root, text="dodaj piłkę", command=lambda: self.createBall())
        self.buttonAdd.pack()
        self.buttonRemove = tk.Button(self.root, text="usuń piłkę", command=lambda: self.removeBall())
        self.buttonRemove.pack()

        self.animateBalls()
    
    class Ball:
        _instances = []

        def __init__(self, appInstance, radius = 15):
            self.vectorX = random.choice([-3, -2, -1, 1, 2, 3])
            self.vectorY = random.choice([-3, -2, -1, 1, 2, 3])

            self.radius = radius
            self.app = appInstance

            positionFound = False

            while not positionFound:
                self.x1 = random.randint(0, 400 - 2 * radius)
                self.y1 = random.randint(0, 400 - 2 * radius)
                self.x2 = self.x1 + radius * 2
                self.y2 = self.y1 + radius * 2

                self.centerX = (self.x1 + self.x2) / 2
                self.centerY = (self.y1 + self.y2) / 2
            
                positionFound = True

                for existingBall in BouncingBallApp.Ball._instances:
                    dx = self.centerX - existingBall.centerX
                    dy = self.centerY - existingBall.centerY
                    distance = math.sqrt(dx**2 + dy**2)

                    if distance <= self.radius + existingBall.radius + 1:
                        positionFound = False
                        break
                
            self.idOf = self.app.circleCanvas.create_oval(self.x1, self.y1, self.x2, self.y2, fill=random.choice(["blue", "red", "green", "yellow"]))
            
            BouncingBallApp.Ball._instances.append(self)

    def createBall(self):
            self.Ball(self)

    def removeBall(self):
        if self.Ball._instances:
            ballRemove = self.Ball._instances.pop()
            self.circleCanvas.delete(ballRemove.idOf)

    def animateBalls(self):
        for ball in BouncingBallApp.Ball._instances:
            self.circleCanvas.move(ball.idOf, ball.vectorX, ball.vectorY)
            
            currentPos = self.circleCanvas.coords(ball.idOf)
            ball.centerX = (currentPos[0] + currentPos[2]) / 2
            ball.centerY = (currentPos[1] + currentPos[3]) / 2
            
            if currentPos[0] <= 0 or currentPos[2] >= 500:
                ball.vectorX = -ball.vectorX
            if currentPos[1] <= 0 or currentPos[3] >= 500:
                ball.vectorY = -ball.vectorY

        self.checkCollisions()
        
        self.root.after(20, self.animateBalls)

    def checkCollisions(self):
        numBalls = len(BouncingBallApp.Ball._instances)
        
        for i in range(numBalls):
            for j in range(i + 1, numBalls):
                ball1 = self.Ball._instances[i]
                ball2 = self.Ball._instances[j]

                dx = ball1.centerX - ball2.centerX
                dy = ball1.centerY - ball2.centerY
                distance = math.sqrt(dx**2 + dy**2)

                if distance <= ball1.radius + ball2.radius:
                    ball1.vectorX, ball2.vectorX = ball2.vectorX, ball1.vectorX
                    ball1.vectorY, ball2.vectorY = ball2.vectorY, ball1.vectorY

rootApp = tk.Tk()
appInit = BouncingBallApp(rootApp)
rootApp.mainloop()