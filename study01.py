import pyxel
import math

BASE_X = 80
BASE_Y = 60

class App:
    def __init__(self):
        #画面サイズの設定　titleはwindow枠にtext出せる
        pyxel.init(160, 120, fps = 60)
        self.x = BASE_X
        self.x3 = BASE_X
        self.y = BASE_Y
        self.y2 = BASE_Y
        self.y3 = BASE_Y
        self.timer = 0
        self.speed = 0.05   #速度
        self.intensity = 40 #揺れ幅

        #実行開始 更新関数 描画関数
        pyxel.run(self.update, self.draw)

	#更新関数
    def update(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.speed -= 0.001 #速度down
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.speed += 0.001 #速度up
        if pyxel.btn(pyxel.KEY_UP):
            self.intensity += 0.4 #揺れ幅up
        if pyxel.btn(pyxel.KEY_DOWN):
            self.intensity -= 0.4 #揺れ幅down
        
        self.timer += self.speed
        #上下往復
        self.y = BASE_Y + self.intensity * math.sin(self.timer)
        #バウンド
        self.y2 = BASE_Y + self.intensity * math.sin(self.timer % math.pi) * -1
        #円運動
        ##マイナスかけるのは、下方向がプラスだから
        self.x3 = BASE_X + self.intensity * math.cos(self.timer)
        self.y3 = BASE_Y + self.intensity * -math.sin(self.timer)

	#描画関数
    def draw(self):
        pyxel.cls(0)
        pyxel.circ(self.x, self.y, 8, 9)
        pyxel.circ(self.x + 20, self.y2, 8, 8)
        pyxel.circ(self.x3, self.y3, 1, 7)
        pyxel.line(BASE_X, BASE_Y, self.x3,self.y3, 8)

        pyxel.text(0, 0, "SPEED:%f" %self.speed, 7)
        pyxel.text(0, 8, "intensity:%f" %self.intensity, 7)

App()