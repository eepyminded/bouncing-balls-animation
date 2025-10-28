import tkinter as tk
import random
import math

class BouncingBallApp:
    def __init__(self, master):
        self.root = master
        self.root.title("Odbijające się piłki")
        
        self.circleCanvas = tk.Canvas(self.root, width=500, height=500, bg="black")
        self.circleCanvas.pack()
        
        self.ballsList = []
        self.createBall(3)  

        self.buttonAdd = tk.Button(self.root, text="dodaj piłkę", command=lambda: self.createBall(1))
        self.buttonAdd.pack()
        self.buttonRemove = tk.Button(self.root, text="usuń piłkę", command=lambda: self.removeBall())
        self.buttonRemove.pack()

        self.animateBalls()
    
    def removeBall(self):
        if self.ballsList:
            someBall = self.ballsList.pop()
            self.circleCanvas.delete(someBall["idOf"])

    def createBall(self, amountOf):
        for current in range(amountOf):
            self.x1 = random.randint(0, 400)
            self.y1 = random.randint(0, 400)
            self.x2 = self.x1 + 30
            self.y2 = self.y1 + 30
            vectorX = random.choice([-3, -2, -1, 1, 2, 3])
            vectorY = random.choice([-3, -2, -1, 1, 2, 3])
        
            ball = self.circleCanvas.create_oval(self.x1, self.y1, self.x2, self.y2, fill=random.choice(["blue", "red", "green", "yellow"]))
            self.ballsList.append(
                {
                "idOf": ball,
                "vectorX": vectorX,
                "vectorY": vectorY,
                "radius": 15,
                }
                )
    
    def animateBalls(self):
        for ball in self.ballsList:
            self.circleCanvas.move(ball["idOf"], ball["vectorX"], ball["vectorY"])
            
            currentPos = self.circleCanvas.coords(ball["idOf"])
            ball["centerX"] = (currentPos[0] + currentPos[2]) / 2
            ball["centerY"] = (currentPos[1] + currentPos[3]) / 2
            
            if currentPos[0] <= 0 or currentPos[2] >= 500:
                ball["vectorX"] = -ball["vectorX"]
            if currentPos[1] <= 0 or currentPos[3] >= 500:
                ball["vectorY"] = -ball["vectorY"]

        self.checkCollisions()
        
        self.root.after(20, self.animateBalls)

    def checkCollisions(self):
        numBalls = len(self.ballsList)
        for i in range(numBalls):
            for j in range(i + 1, numBalls):
                ball1 = self.ballsList[i]
                ball2 = self.ballsList[j]

                dx = ball1["centerX"] - ball2["centerX"]
                dy = ball1["centerY"] - ball2["centerY"]
                distance = math.sqrt(dx**2 + dy**2)

                if distance <= ball1["radius"] + ball2["radius"]:
                    ball1["vectorX"], ball2["vectorX"] = ball2["vectorX"], ball1["vectorX"]
                    ball1["vectorY"], ball2["vectorY"] = ball2["vectorY"], ball1["vectorY"]

rootApp = tk.Tk()
appInit = BouncingBallApp(rootApp)
rootApp.mainloop()