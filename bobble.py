#coding:utf-8
from Tkinter import *
import math
import random

'''
定义小球类，包含的属性有：
       坐标(x, y)
       速度speed
       方向(用角度表示，范围是0--2*pi )
       颜色
       半径
       生命(用来表示小球是否还存在)
	   Game类 
'''
class Bobble:
        
    def __init__(self, x, y, speed, direction, color, radius, life, game):
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = direction
        self.color = color
        self.radius = radius
        self.life = life
        self.game = game
    
    #根据小球的坐标画出小球    
    def drawBobble(self):
        self.bobble = self.game.canvas.create_oval(self.x-self.radius, self.y-self.radius, self.x+self.radius, self.y+self.radius, fill=self.color)
    
    #根据小球的方向，移动小球，    
    def move(self):
        if self.isLive():
            self.meetWall()
            self.game.canvas.move(self.bobble, self.speed*math.cos(self.direction), self.speed*math.sin(self.direction))
            self.update()
            self.game.canvas.after(10, self.move)
        else:
            self.game.canvas.delete(self.bobble)       
    
    #判断小球是否还存在
    def isLive(self):
        if self.life != 0:
            return True
        else:
            return False
      
    #更新小球的坐标  
    def update(self):
        self.x += self.speed*math.cos(self.direction)
        self.y += self.speed*math.sin(self.direction)
    
    #判断小球小球是否碰到墙壁，如果碰到就改变方向
    def meetWall(self):
        if self.y-self.radius <= 0 or self.y+self.radius >=500:
            self.direction = -self.direction
        if self.x-self.radius <= 0 or self.x+self.radius >=500:
            self.direction = math.pi - self.direction
                  
        
'''
定义Game类，继承Tk类
通过此类创建游戏窗口并运行
'''
class Game(Tk):
    #创建窗口
    def createInterface(self):
        self.geometry('500x550')
        self.resizable(False, False)
        
        self.gameFrame = Frame(height='500', width='500')
        self.gameFrame.pack()
        
        self.controlFrame = Frame(height='50', width='500')
        self.controlFrame.pack()
        
        #start按钮
        self.startButton = Button(self.controlFrame, text='start', command=self.start)
        self.startButton.pack(fill=X,side=LEFT,pady=10)
        
        #quit按钮
        self.quitButton = Button(self.controlFrame, text='quit', command=quit)
        self.quitButton.pack(fill=X,side=LEFT,pady=10,padx=10)
        
        #加速按钮
        self.plusButton = Button(self.controlFrame, text='+', command=self.accelerate)
        self.plusButton.pack(fill=X,side=LEFT,pady=10)
        
        #显示速度的标签
        self.rateLabel = Label(self.controlFrame,text='rate: 2')
        self.rateLabel.pack(fill=X,side=LEFT,pady=10)
        
        #减速按钮
        self.minusButton = Button(self.controlFrame, text='-', command=self.decelerate)
        self.minusButton.pack(fill=X,side=LEFT,pady=10)
        
        #显示得分的标签
        self.pointLabel = Label(self.controlFrame,text='point: 0')
        self.pointLabel.pack(fill=X,side=LEFT,pady=10,padx=10)
        
        #画图板
        self.canvas = Canvas(self.gameFrame, height='500', width='500', bg='#00ffff')
        self.canvas.pack()
        
        #对用户点击鼠标左键，做出响应
        self.bind('<Button-1>', self.bingo)
        
    
        
    
    #初始化游戏
    def init(self):
        self.bobbleList = []
        self.rate = 2
        self.point = 0
        colorList = ['red', 'blue', 'yellow', 'gray', 'green', 'black']
        for i in range(0,10):
            #随机产生小球的坐标，大小，颜色，方向
            x = random.randint(50,450)
            y = random.randint(50,450)
            radius = random.randint(8,15)
            direction = random.uniform(0,2)*math.pi
            color = colorList[random.randint(0,5)]
            self.bobbleList.append(Bobble(x, y, self.rate, direction, color, radius, 1, self))
            
        
    #当用户点击start按钮时，开始
    def start(self):
        self.canvas.destroy()
        self.canvas = Canvas(self.gameFrame, height='500', width='500', bg='#00ffff')
        self.canvas.pack()
        self.init()
        for bobble in self.bobbleList:
            bobble.drawBobble()
            bobble.move()
        self.rateLabel['text'] = 'rate: ' + str(self.rate)
        self.pointLabel['text'] = 'point: ' + str(self.point)
        
    #加速
    def accelerate(self):
        self.rate += 1
        self.rateLabel['text'] = 'rate: ' + str(self.rate)
        for bobble in self.bobbleList:
            bobble.speed = self.rate
            
    #减速
    def decelerate(self):
        if self.rate > 1:
            self.rate -= 1
        self.rateLabel['text'] = 'rate: ' + str(self.rate)
        for bobble in self.bobbleList:
            bobble.speed = self.rate
            
    #判断用户是否点击中小球，并做出响应
    def bingo(self, event):
        for bobble in self.bobbleList:
            if (event.x-bobble.x)**2 + (event.y-bobble.y)**2 <= bobble.radius**2:
                self.bobbleList.remove(bobble)
                bobble.life = 0
                self.point += 1
                self.pointLabel['text'] = 'point: ' + str(self.point)


def main():   
    game = Game()  
    game.createInterface()  
    game.init()
    game.mainloop()  
    
if __name__ == '__main__':
    main()
