#角度方向へ弾を飛ばす
import pyxel
import math

BASE_X = 80
BASE_Y = 60

class App:
    def __init__(self):
        #画面サイズの設定　titleはwindow枠にtext出せる
        pyxel.init(160, 120, fps = 60)
        self.x = BASE_X
        self.y = BASE_Y
        self.x3 = BASE_X    #円周上の座標
        self.y3 = BASE_Y    #円周上の座標
        self.timer = 0
        self.count = 0
        self.speed = 0.05   #速度
        self.bulletSpeed = 1   #速度
        self.intensity = 40 #揺れ幅
        self.isPlus = True
        self.aim = 0
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
        
        #逆転判定
        if self. timer < 0 and self.isPlus == False:
            self.timer = 0
            self.isPlus = True
        if self.timer > math.pi and self.isPlus == True:
            self.timer = math.pi
            self.isPlus = False

        if self.isPlus == True:
            self.timer += self.speed
        else:
            self.timer -= self.speed

        #円運動
        ##マイナスかけるのは、下方向がプラスだから
        self.x3 = BASE_X + self.intensity * math.cos(self.timer)
        self.y3 = BASE_Y + self.intensity * -math.sin(self.timer)

        #
        if pyxel.btnr(pyxel.KEY_A):
            dx = self.x3 - BASE_X
            dy = self.y3 - BASE_Y
            self.aim = math.atan2(-dy, dx)
            print(self.aim)

        '''
        #狙い撃ち角度を求める(ラジアン)
        self.count += self.speed
        if self.count > 2:
            dx = self.x3 - BASE_X
            dy = self.y3 - BASE_Y
            self.aim = math.atan2(-dy, dx)
            self.count = 0
        
            #
            self.bulletSpeed += self.speed
        '''

        #弾用座標
        self.x += self.bulletSpeed * math.cos(self.aim)
        self.y += self.bulletSpeed * -math.sin(self.aim)

#        self.x += self.direction[0] * self.speed

#        self.x += self.x3 + self.intensity * self.bulletSpeed * math.cos(self.aim)
#        self.y += self.y3 + self.intensity * self.bulletSpeed * -math.sin(self.aim)
#        self.x = BASE_X + self.intensity * self.count * math.cos(self.aim)
#        self.y = BASE_Y + self.intensity * self.count * -math.sin(self.aim)
                

	#描画関数
    def draw(self):
        pyxel.cls(0)
        pyxel.circ(self.x, self.y, 3, 8)
        pyxel.circ(self.x3, self.y3, 1, 7)
        pyxel.line(BASE_X, BASE_Y, self.x3,self.y3, 8)

        pyxel.text(0,  0, "SPEED:%f" %self.speed, 7)
        pyxel.text(0,  8, "intensity:%f" %self.intensity, 7)
        pyxel.text(0,  16, "self.x:%f" %self.x, 7)

App()