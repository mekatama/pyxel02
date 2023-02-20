import pyxel
from random import randint  #ランダム使用
#定数
WINDOW_H = 160
WINDOW_W = 120

#xy座標用class
class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

#Player用
class Player:
    def __init__(self):
        #Vec2クラス内でself.x=0 self.y=0と処理されてるっぽい
        self.pos = Vec2(0, 0)
        self.isRight = True #playerの移動方向flag
        self.isStop = False #playerの停止flag
    def update(self):
        self.pos.y = 144        #初期y座標
        #key入力(player停止)
        if pyxel.btn(pyxel.KEY_A):
            self.isStop = True  #押したら
        elif pyxel.btnr(pyxel.KEY_A):
            self.isStop = False #離したら
        #playerの移動方向判定
        if self.pos.x <= 0:
            self.isRight = True     #右移動
        elif self.pos.x >= 104:
            self.isRight = False    #左移動
	    #playerの往復移動
        if self.isStop == False:
            if self.isRight == True:
                self.pos.x = (self.pos.x + 5)
            elif self.isRight == False:
                self.pos.x = (self.pos.x - 5)

#Enemy用
class Enemy:
    def __init__(self):
        #Vec2クラス内でself.x=0 self.y=0と処理されてるっぽい
        self.pos = Vec2(0, 0)
        self.speed = 0.02
    def update(self, x, y):
        self.pos.x = x
        self.pos.y = y

#Bullet
class Bullet:
    def __init__(self):
        self.pos = Vec2(0, 0)
        self.size = 2
        self.speed = 3
        self.color = 10 #colorは0～15
    def update(self, x, y, size, color):
        self.pos.x = x
        self.pos.y = y
        self.size = size
        self.color = color

#ゲーム管理
class App:
    def __init__(self):
        #画面サイズの設定　titleはwindow枠にtext出せる
        pyxel.init(WINDOW_W, WINDOW_H, title="Pyxel Base")
        #editorデータ読み込み(コードと同じフォルダにある)
        pyxel.load("my_resource.pyxres")
        #インスタンス生成
        self.mPlayer = Player()
        #インスタンス入れる用リスト
        self.bullets = []
        self.enemies = []
        #flag
        self.EnemyFlag = 1
        #実行開始 更新関数 描画関数
        pyxel.run(self.update, self.draw)

    #更新
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        #■ Player ========================================================
        #Playerの仮配置
        self.mPlayer.update()

        #■ Enemy ========================================================
        #敵の仮配置
        if self.EnemyFlag == 1: #ここで敵を配置
            new_enemy = Enemy()
            new_enemy.update(WINDOW_W/2, WINDOW_H/2 + 30)
            self.enemies.append(new_enemy)
            self.EnemyFlag = 0  #配置終了

        #EnemyとPlayの当たり判定
        enemy_count = len(self.enemies)
        for i in range(enemy_count):
            if ((self.mPlayer.pos.x         < self.enemies[i].pos.x + 16) and   #enemy右下座標とplayer原点
                (self.mPlayer.pos.x + 16    > self.enemies[i].pos.x + 16) and
                (self.mPlayer.pos.y         < self.enemies[i].pos.y + 16) and 
                (self.mPlayer.pos.y + 16    > self.enemies[i].pos.y + 16)
                or
                (self.mPlayer.pos.x         < self.enemies[i].pos.x) and        #enemy左下座標とplayer右上
                (self.mPlayer.pos.x + 16    > self.enemies[i].pos.x) and
                (self.mPlayer.pos.y         < self.enemies[i].pos.y + 16) and
                (self.mPlayer.pos.y + 16    > self.enemies[i].pos.y + 16)
                or
                (self.mPlayer.pos.x         < self.enemies[i].pos.x + 16) and   #enemy右上座標とplayer左下
                (self.mPlayer.pos.x +16     > self.enemies[i].pos.x + 16) and
                (self.mPlayer.pos.y         < self.enemies[i].pos.y) and
                (self.mPlayer.pos.y + 16    > self.enemies[i].pos.y)
                or
                (self.mPlayer.pos.x         < self.enemies[i].pos.x) and        #enemy原点とplayer右下下
                (self.mPlayer.pos.x + 16    > self.enemies[i].pos.x) and
                (self.mPlayer.pos.y         < self.enemies[i].pos.y) and
                (self.mPlayer.pos.y + 16    > self.enemies[i].pos.y)):
                #hit時の処理
                print("hit!!")

        #■ bullet ========================================================
        #key入力
        if pyxel.btnp(pyxel.KEY_S):
            #bulletインスタンス生成
            new_bullet = Bullet()
            #bulletクラス更新
            new_bullet.update(  self.mPlayer.pos.x + 6,
                                self.mPlayer.pos.y + 6,
                                new_bullet.size, new_bullet.color)
            #bulletsリストに追加
            self.bullets.append(new_bullet)
        #リスト要素数を取得
        bullet_count = len(self.bullets)
        #bulletsの数分ループする
        for i in range(bullet_count):
            if 0 < self.bullets[i].pos.y and self.bullets[i].pos.y < WINDOW_H:  #画面内判定
                #bullets更新
                self.bullets[i].update( self.bullets[i].pos.x,
                                        self.bullets[i].pos.y - self.bullets[i].speed,
                                        self.bullets[i].size, self.bullets[i].color)
                #enemyとbulletの当たり判定
                enemy_count = len(self.enemies) #リスト要素数を取得
                for j in range(enemy_count):
                    #bulletは小さいので１点で判定
                    if((self.enemies[j].pos.x < self.bullets[i].pos.x) and
                       (self.bullets[i].pos.x < self.enemies[j].pos.x + 16) and
                       (self.enemies[j].pos.y < self.bullets[i].pos.y) and
                       (self.bullets[i].pos.y < self.enemies[j].pos.y + 16)):
                        #消す
                        del self.enemies[j]
                        del self.bullets[i]
                        break
            else:   #画面外判定
                del self.bullets[i] #削除
                break

	#描画
    def draw(self):
        pyxel.cls(0)    #画面クリア 0は黒

        # player ===============================================================
        #editorデータ描画(player)
        pyxel.blt(self.mPlayer.pos.x, self.mPlayer.pos.y, 0, 0, 0, 16, 16, 0)
        # enemy ===============================================================
        for enemy in self.enemies:
            pyxel.blt(enemy.pos.x, enemy.pos.y, 0, 16, 0, 16, 16, 0)
        # bullet ===============================================================
        for ball in self.bullets:   #リストを指定するとその中身でforできる
            pyxel.circ(ball.pos.x, ball.pos.y, ball.size, ball.color)

            #描画座標(左上のX座標) #描画座標(左上のY座標)
            #画像番号
            #切り出しの左上のX座標 #切り出しの左上のY座標
            #切り出す幅           #切り出す高さ
            #抜き色(パレット番号)
App()