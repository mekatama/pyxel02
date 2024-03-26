#砲台で迎撃
import pyxel
import math
#画面遷移用の変数
SCENE_TITLE = 0	    #タイトル画面
SCENE_PLAY = 1	    #ゲーム画面
SCENE_GAMEOVER = 2  #ゲームオーバー画面
#定数
WINDOW_H = 128
WINDOW_W = 128
PLAYER_HW = 8
PLAYER_HP = 1
PLAYER_BULLET_SPEED = 8
BOM_TIME = 30
#list用意
bullets = []
enemies = []
enemiesUI = []
blasts = []
items = []

#関数(List実行)
def update_list(list):
    for elem in list:
        elem.update()   #listの各要素に対してupdate()実行
#関数(List描画)
def draw_list(list):
    for elem in list:
        elem.draw()     #listの各要素に対してdraw()実行
#関数(List更新)
def cleanup_list(list):
    i = 0
    while i < len(list):        #listに要素が入っている間loops
        elem = list[i]          #要素取得
        if not elem.is_alive:   #死亡の場合
            list.pop(i)         #要素削除
        else:                   #生存の場合
            i += 1              #スルー

#■Player
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.x3 = x
        self.y3 = y
        self.hp = PLAYER_HP
        self.speed = 0.05   #速度
        self.intensity = 40 #揺れ幅
        self.timer = 0
        self.aim = 0        #攻撃角度
        self.countStop = 0  #攻撃時の往復移動停止用
        self.isPlus = True  #反転flag
        self.isShot = False #弾発射flag
        self.isStop = False #照準停止用
        self.isBom = False  #bom発射flag
        self.is_alive = True
    def update(self):
        #debug
        if pyxel.btn(pyxel.KEY_LEFT):
            self.speed -= 0.001 #速度down
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.speed += 0.001 #速度up
        if pyxel.btn(pyxel.KEY_UP):
            self.intensity += 0.4 #揺れ幅up
        if pyxel.btn(pyxel.KEY_DOWN):
            self.intensity -= 0.4 #揺れ幅down
        #照準一時停止制御
        if self.isStop == True:
            self.countStop += 1
            if self.countStop > 15:
                self.isStop = False
                self.countStop = 0
        #角度で反転判定
        if self. timer < 0 and self.isPlus == False:
            self.timer = 0
            self.isPlus = True
        if self.timer > math.pi and self.isPlus == True:
            self.timer = math.pi
            self.isPlus = False
        #照準の往復移動
        if self.isStop == False:
            if self.isPlus == True:
                self.timer += self.speed
            else:
                self.timer -= self.speed
        #円周上の座標
        ##マイナスかけるのは、下方向がプラスだから
        self.x3 = self.x + self.intensity * math.cos(self.timer)
        self.y3 = self.y + self.intensity * -math.sin(self.timer)

        #Aボタン入力で角度決定→弾生成
        if pyxel.btnr(pyxel.KEY_A):
            dx = self.x3 - self.x
            dy = self.y3 - self.y
            self.aim = math.atan2(-dy, dx)
            self.isShot = True
            self.isStop = True
            print(self.aim)
            Bullet(self.x + PLAYER_HW / 2, self.y, self.x3 + PLAYER_HW / 2, self.y3, PLAYER_BULLET_SPEED, self.aim)
        #debug
        #Zボタン入力で一時停止ボム
        if pyxel.btnp(pyxel.KEY_Z):
            self.isBom = True
        if pyxel.btnr(pyxel.KEY_Z):
            self.isBom = False

    def draw(self):
        #editorデータ描画(player)
        pyxel.blt(self.x, self.y, 0, 8, 0, 8, 8, 0)
        #debugg
        pyxel.circ(self.x + PLAYER_HW / 2, self.y, 1, 8)
        pyxel.circ(self.x3 + PLAYER_HW / 2, self.y3, 1, 7)
        pyxel.line(self.x + PLAYER_HW / 2, self.y, self.x3 + PLAYER_HW / 2, self.y3, 8)

class Bullet:
    def __init__(self, x, y, x3, y3, speed, aim):
        self.x = x
        self.y = y
        self.speed = speed
        self.aim = aim
        self.size = 1
        self.color = 10 #colorは0～15
        self.count = 0
        self.is_alive = True
        bullets.append(self)
    def update(self):
        #弾用座標
        self.x += self.speed * math.cos(self.aim)
        self.y += self.speed * -math.sin(self.aim)
    def draw(self):
        pyxel.circ(self.x, self.y, self.size, self.color)

#■Enemy
class Enemy:
    def __init__(self, x, y, speed, type, hp):
        self.x = x
        self.y = y
        self.x3 = x
        self.y3 = y
        self.speed = speed
        self.type = type        #移動type 0:停止　1:円運動 2:往復
        self.hp = hp
        self.timer = 0          #円運動の半径
        self.r = 20             #円運動の半径
        self.countStop = 0      #一時停止count
        self.isStop = False     #一時停止flag
        self.is_alive = True
        enemies.append(self)
    def update(self):
        if self.isStop == False:
            if self.type == 1:
                #type=1円移動
                ##マイナスかけるのは、下方向がプラスだから
                self.timer += self.speed
                self.x3 = self.x + self.r * math.cos(self.timer)
                self.y3 = self.y + self.r * -math.sin(self.timer)
            elif self.type == 2:
                #type=2横往復移動
                ##マイナスかけるのは、下方向がプラスだから
                self.timer += self.speed
                self.x3 = self.x + self.r * math.cos(self.timer)
        else:
            #一時停止
            self.countStop += 1
            if self.countStop > BOM_TIME:
                self.countStop = 0
                self.isStop = False

    def draw(self):
        if self.type == 0:
            pyxel.blt(self.x, self.y, 0, 24, 0, 8, 8, 0)
        elif self.type == 1:
            pyxel.blt(self.x3, self.y3, 0, 24, 0, 8, 8, 0)
        elif self.type == 2:
            pyxel.blt(self.x3, self.y, 0, 24, 0, 8, 8, 0)

#■Enemy_UI
class EnemyUI:
    def __init__(self, x, y, score):
        self.x = x
        self.y = y
        self.score = score
        self.count = 0
        self.is_alive = True
        enemiesUI.append(self)
    def update(self):
        self.count += 1
        if self.count < 10:
            self.y -= 1
        elif self.count >= 10:
            self.is_alive = False
    def draw(self):
        pyxel.text(self.x, self.y, f"+{self.score:2}", 13)

#■Blust
class Blast:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.count = 0
        self.motion = 0         #アニメ切り替え用
        self.is_alive = True
        blasts.append(self)
    def update(self):
        self.count += 1
        if self.count >= 5 and self.count < 10:
            self.motion = 1
        elif self.count >= 10:
            self.is_alive = False
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 16, 0 + (8 * self.motion), 8, 8, 0)

#■Item
class Item:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vec = 0
        self.count = 0
        self.motion = 0         #アニメ切り替え用
        self.is_alive = True
        blasts.append(self)
    def update(self):
        self.x = self.x
        self.y = self.y
        self.count += 1
        if self.count >= 5 and self.count < 10:
            self.motion = 1
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 32, 0, 8, 8, 0)

class App:
    def __init__(self):
        #画面サイズの設定　titleはwindow枠にtext出せる
        pyxel.init(WINDOW_W, WINDOW_H, title="Pyxel Base")
        #editorデータ読み込み(コードと同じフォルダにある)
        pyxel.load("my_resource10.pyxres")
        self.score = 0
        self.highScore = 0
        #画面遷移の初期化
        self.scene = SCENE_TITLE
        #Playerインスタンス生成
        self.player = Player(pyxel.width / 2 - 4, pyxel.height - 16)

        #実行開始 更新関数 描画関数
        pyxel.run(self.update, self.draw)

	#更新関数
    def update(self):
        #処理の画面分岐
        if self.scene == SCENE_TITLE:
            self.update_title_scene()
        elif self.scene == SCENE_PLAY:
            self.update_play_scene()
        elif self.scene == SCENE_GAMEOVER:
            self.update_gameover_scene()

    #タイトル画面処理用update
    def update_title_scene(self):
        #ENTERでゲーム画面に遷移
        if pyxel.btnr(pyxel.KEY_RETURN):
#            pyxel.playm(0, loop = True)    #BGM再生
            self.scene = SCENE_PLAY

    #ゲーム画面処理用update
    def update_play_scene(self):
        #enemyのtype設定
        #debug
        enemyType = 0
#        enemyType = pyxel.rndi(0, 2)
        spawntime = 60

        #一定時間でenemy出現判定
        if pyxel.frame_count % spawntime == 0:
            #enemy生成
            Enemy(pyxel.rndi(8, 112), pyxel.rndi(20, 60), 0.1, enemyType,3)

        '''
        #scoreで生成間隔を制御
        if self.score < 30:
            spawntime = 30
        elif self.score >= 30 and self.score < 70:
            spawntime = 25
        elif self.score >= 70:
            spawntime = 20
        '''

        #Player制御
        self.player.update()
        #一時停止処理
        if self.player.isBom == True:
            #Enemy全部処理
            for enemy in enemies:
                enemy.isStop = True

        #EnemyとBulletの当たり判定
        for enemy in enemies:
            for bullet in bullets:
                if((enemy.x + 8    > bullet.x - 1 and
                    enemy.x        < bullet.x + 1 and
                    enemy.y + 8    > bullet.y - 1 and
                    enemy.y        < bullet.y + 1 and enemy.type == 0) or
                   (enemy.x3 + 8   > bullet.x - 1 and
                    enemy.x3       < bullet.x + 1 and
                    enemy.y3 + 8   > bullet.y - 1 and
                    enemy.y3       < bullet.y + 1 and enemy.type == 1) or
                   (enemy.x3 + 8   > bullet.x - 1 and
                    enemy.x3       < bullet.x + 1 and
                    enemy.y + 8    > bullet.y - 1 and
                    enemy.y        < bullet.y + 1 and enemy.type == 2)):
                    #Hit時の処理
                    enemy.hp -= 1
                    bullet.is_alive = False
                    #残りHP判定
                    if enemy.hp <= 0:
                        enemy.is_alive = False
                        enemiesUI.append(
                            EnemyUI(enemy.x, enemy.y, 10)
                        )
                        blasts.append(
                            Blast(enemy.x, enemy.y)
                        )
                        items.append(
                            Item(enemy.x, enemy.y)
                        )
                        self.score += 10
#                        pyxel.play(1, 0, loop=False)    #SE再生

        #EnemyとPlayerの当たり判定
        for enemy in enemies:
            if (self.player.x + 12  > enemy.x + 4 and
                self.player.x + 4   < enemy.x + 12 and
                self.player.y + 12  > enemy.y + 4 and
                self.player.y + 4   < enemy.y + 12):
                #Hit時の処理
                self.player.hp -= 1
                enemy.is_alive = False
#                pyxel.play(3, 1, loop=False)    #SE再生
                #player残りHP判定
                if self.player.hp <= 0:
                    blasts.append(
                        Blast(enemy.x, enemy.y)
                    )
                    pyxel.stop()
                    self.scene = SCENE_GAMEOVER

        #ItemとPlayerの処理
        for item in items:
            #Itemの動き
            ex = (self.player.x - item.x)
            ey = (self.player.y - item.y)
            Kp = 0.2
            if ex != 0 or ey != 0:
                item.x = item.x + ex * Kp
                item.y = item.y + ey * Kp

            #ItemとPlayerの当たり判定
            if (self.player.x + 12  > item.x + 4 and
                self.player.x + 4   < item.x + 12 and
                self.player.y + 12  > item.y + 4 and
                self.player.y + 4   < item.y + 12):
                #Hit時の処理
                self.score += 10
                item.is_alive = False
#                pyxel.play(3, 1, loop=False)    #SE再生

        #High Score
        if self.score >= self.highScore:
            self.highScore = self.score

        #list実行
        update_list(bullets)
        update_list(enemies)
        update_list(enemiesUI)
        update_list(blasts)
        update_list(items)
        #list更新
        cleanup_list(bullets)
        cleanup_list(enemies)
        cleanup_list(enemiesUI)
        cleanup_list(blasts)
        cleanup_list(items)

    #ゲームオーバー画面処理用update
    def update_gameover_scene(self):
        #list実行
        #list更新
        #ENTERでタイトル画面に遷移
        if pyxel.btnr(pyxel.KEY_RETURN):
#            pyxel.playm(0, loop = True)         #BGM再生
            self.score = 0
            self.scene = SCENE_TITLE
            #list全要素削除
            bullets.clear()                     #list全要素削除
            enemies.clear()                     #list全要素削除
            enemiesUI.clear()                     #list全要素削除
            blasts.clear()                     #list全要素削除
            items.clear()                     #list全要素削除

	#描画関数
    def draw(self):
        #画面クリア 0は黒
        pyxel.cls(0)
        #描画の画面分岐
        if self.scene == SCENE_TITLE:
            self.draw_title_scene()
        elif self.scene == SCENE_PLAY:
            self.draw_play_scene()
        elif self.scene == SCENE_GAMEOVER:
            self.draw_gameover_scene()

        #score表示(f文字列的な)
        pyxel.text(4, 4, f"SCORE {self.score:5}", 7)
        pyxel.text(60, 4, f"HIGH SCORE {self.highScore:5}", 6)

    #タイトル画面描画用update
    def draw_title_scene(self):
        pyxel.text(0, 20, "01234567890123456789012345678901", 7)
        pyxel.text(48, 28, "________", 7)
        pyxel.text(32, 58, "- PRESS  ENTER -", 7)
        pyxel.text(0, 76, "--------------------------------", 7)
        pyxel.text(40, 82, "HOW TO PLAY", 7)

    #ゲーム画面描画用update
    def draw_play_scene(self):
        pyxel.text(4, 26, "STOP", 7)
        pyxel.rect(20, 26, 100, 5, 7)
#        pyxel.rect(20, 16, self.player.fuel, 5, 7)
        self.player.draw()
        draw_list(bullets)
        draw_list(enemies)
        draw_list(enemiesUI)
        draw_list(blasts)
        draw_list(items)
        #debug
        pyxel.text(0,  10, "SPEED:%f" %self.player.speed, 7)
        pyxel.text(0,  18, "intensity:%f" %self.player.intensity, 7)

    #ゲームオーバー画面描画用update
    def draw_gameover_scene(self):
        pyxel.text(0, 20, "01234567890123456789012345678901", 7)
        pyxel.text(44, 40, "GAME OVER", 7)
        pyxel.text(32, 80, "- PRESS ENTER -", 7)
App()