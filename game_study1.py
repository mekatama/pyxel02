import pyxel
WINDOW_H = 120
WINDOW_W = 160

#xy座標用
class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

#Player用
class player:
    def __init__(self):
        #Vec2クラス内でself.x=0 self.y=0と処理されてるっぽい
        self.pos = Vec2(0, 0)
        self.vec = 0    #向き(ベクトル)

    def update(self, x, y, dx):
        self.pos.x = x
        self.pos.y = y
        self.vec = dx

#Elayer用
class enemy:
    def __init__(self):
        #Vec2クラス内でself.x=0 self.y=0と処理されてるっぽい
        self.pos = Vec2(0, 0)
        self.vec = 0    #向き(ベクトル)
        self.speed = 0.02

    def update(self, x, y, dx):
        self.pos.x = x
        self.pos.y = y
        self.vec = dx

#Bullet
class bullet:
    def __init__(self):
        self.pos = Vec2(0, 0)
        self.vec = 0    #向き(ベクトル)
        self.size = 2
        self.speed = 3
        self.color = 10 #colorは0～15

    def update(self, x, y, dx, size, color):
        self.pos.x = x
        self.pos.y = y
        self.vec = dx
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
        self.mPlayer = player()
        #インスタンス入れる用リスト
        self.bullets = []
        self.enemies = []
        #マウスカーソル表示
        pyxel.mouse(False)
        #flag
        self.EnemyFlag = 1
        self.GameOverFlag = 0
        #実行開始 更新関数 描画関数
        pyxel.run(self.update, self.draw)

	#更新
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        #■ player ========================================================
        dx = pyxel.mouse_x - self.mPlayer.pos.x #x軸方向の移動量
        dy = pyxel.mouse_y - self.mPlayer.pos.y #y軸方向の移動量
        #移動量判定
        if dx != 0:
            self.mPlayer.update(pyxel.mouse_x, pyxel.mouse_y, dx)   #移動と向き変更
        elif dy != 0:   #真上or真下に移動
            self.mPlayer.update(pyxel.mouse_x, pyxel.mouse_y, 0)   #移動のみ変更

        #■ enemy ========================================================
        if self.EnemyFlag == 1: #ここで敵を配置
            new_enemy = enemy()
            new_enemy.update(WINDOW_W/2, WINDOW_H/2 + 30, self.mPlayer.vec)
            self.enemies.append(new_enemy)
            self.EnemyFlag = 0

        #enemyとplayの当たり判定
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
                #GameOver判定
                self.GameOverFlag = 1
        #■ bullet ========================================================
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT): #左クリック
            #bulletインスタンス生成
            new_bullet = bullet()
            if self.mPlayer.vec > 0:   #player右向きの場合
                #bulletクラス更新(右に表示)
                new_bullet.update(self.mPlayer.pos.x + 14,
                                  self.mPlayer.pos.y,
                                  self.mPlayer.vec, new_bullet.size, new_bullet.color)
            else:
                #bulletクラス更新(左に表示)
                new_bullet.update(self.mPlayer.pos.x - 14,
                                  self.mPlayer.pos.y,
                                  self.mPlayer.vec, new_bullet.size, new_bullet.color)
            #bulletsリストに追加
            self.bullets.append(new_bullet)
        #リスト要素数を取得
        ball_count = len(self.bullets)
        #bulletsの数分ループする
        for i in range(ball_count):
            if 0 < self.bullets[i].pos.x and self.bullets[i].pos.x < WINDOW_W:  #画面内判定
                #bullets更新
                if self.bullets[i].vec > 0: #右向きなら
                    self.bullets[i].update(self.bullets[i].pos.x + self.bullets[i].speed,
                                           self.bullets[i].pos.y,
                                           self.bullets[i].vec, self.bullets[i].size, self.bullets[i].color)
                else:
                    self.bullets[i].update(self.bullets[i].pos.x - self.bullets[i].speed,
                                           self.bullets[i].pos.y,
                                           self.bullets[i].vec, self.bullets[i].size, self.bullets[i].color)
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
        #画面クリア 0は黒
        pyxel.cls(0)

        # player ===============================================================
        #player向き判定
        if self.mPlayer.vec > 0:    #右向き
            #editorデータ描画(player)
            pyxel.blt(self.mPlayer.pos.x, self.mPlayer.pos.y, 0, 0, 0, 16, 16, 0)
        else:                       #左向き
            pyxel.blt(self.mPlayer.pos.x, self.mPlayer.pos.y, 0, 0, 0, -16, 16, 0)

        # enemy ===============================================================
        for enemy in self.enemies:
            if enemy.vec > 0:   #右向き
                pyxel.blt(enemy.pos.x, enemy.pos.y, 0, 16, 0, 16, 16, 0)
            else:               #左向き
                pyxel.blt(enemy.pos.x, enemy.pos.y, 0, 16, 0, -16, 16, 0)

        # bullet ===============================================================
        for ball in self.bullets:   #リストを指定するとその中身でforできる
            pyxel.circ(ball.pos.x, ball.pos.y, ball.size, ball.color)

            #描画座標(左上のX座標) #描画座標(左上のY座標)
            #画像番号
            #切り出しの左上のX座標 #切り出しの左上のY座標
            #切り出す幅           #切り出す高さ
            #抜き色(パレット番号)

        # GameOver ===============================================================
        if self.GameOverFlag == 1:
            #テキスト表示(colorが周期的に変わる)
            pyxel.text(55, 40, "Game Over", pyxel.frame_count % 16)

App()